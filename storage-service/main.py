import json
import os
import time

import psycopg2
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER  = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC         = os.getenv("TOPIC", "health-data")
PG_HOST       = os.getenv("PG_HOST", "postgres")
PG_PORT       = int(os.getenv("PG_PORT", 5432))
PG_DB         = os.getenv("PG_DB", "healthdb")
PG_USER       = os.getenv("PG_USER", "health")
PG_PASSWORD   = os.getenv("PG_PASSWORD", "health123")
INFLUX_URL    = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN  = os.getenv("INFLUX_TOKEN", "health-token-123")
INFLUX_ORG    = os.getenv("INFLUX_ORG", "health-org")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "health-bucket")

THRESHOLDS = {
    "heart_rate":              {"min": 50,  "max": 120},
    "glucose":                 {"min": 70,  "max": 180},
    "blood_pressure_systolic": {"min": 90,  "max": 160},
    "spo2":                    {"min": 94,  "max": 100},
    "temperature":             {"min": 35.5,"max": 38.5},
}


def wait_for_postgres(retries=15, delay=5):
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                host=PG_HOST, port=PG_PORT, dbname=PG_DB,
                user=PG_USER, password=PG_PASSWORD
            )
            print("[Storage] PostgreSQL connecte")
            return conn
        except Exception as e:
            print(f"[Storage] PostgreSQL non disponible ({attempt+1}/{retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("Impossible de se connecter a PostgreSQL.")


def wait_for_influx(retries=15, delay=5):
    for attempt in range(retries):
        try:
            client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
            client.ping()
            print("[Storage] InfluxDB connecte")
            return client
        except Exception as e:
            print(f"[Storage] InfluxDB non disponible ({attempt+1}/{retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("Impossible de se connecter a InfluxDB.")


def wait_for_kafka(broker, topic, retries=10, delay=5):
    for attempt in range(retries):
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=broker,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                auto_offset_reset="earliest",
                group_id="storage-service-group",
            )
            print("[Storage] Kafka connecte")
            return consumer
        except NoBrokersAvailable:
            print(f"[Storage] Kafka non disponible ({attempt+1}/{retries})...")
            time.sleep(delay)
    raise RuntimeError("Impossible de se connecter a Kafka.")


def init_postgres(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                condition VARCHAR(50),
                latest_metrics JSONB,
                last_seen TIMESTAMP,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id SERIAL PRIMARY KEY,
                patient_id VARCHAR(50) REFERENCES patients(id),
                metric VARCHAR(50),
                value FLOAT,
                threshold_min FLOAT,
                threshold_max FLOAT,
                severity VARCHAR(20),
                timestamp TIMESTAMP
            );
        """)
        conn.commit()
    print("[Storage] Tables PostgreSQL initialisees")


def upsert_patient(conn, data):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO patients (id, name, age, condition, latest_metrics, last_seen)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                latest_metrics = EXCLUDED.latest_metrics,
                last_seen = EXCLUDED.last_seen;
        """, (
            data["patient_id"], data["patient_name"], data["age"], data["condition"],
            json.dumps(data["metrics"]), data["timestamp"]
        ))
        conn.commit()


def save_alerts(conn, data):
    metrics = data["metrics"]
    alerts = []
    for key, limits in THRESHOLDS.items():
        value = metrics.get(key)
        if value is None:
            continue
        if value < limits["min"]:
            alerts.append((key, value, limits["min"], limits["max"], "CRITICAL"))
        elif value > limits["max"]:
            alerts.append((key, value, limits["min"], limits["max"], "WARNING"))

    if alerts:
        with conn.cursor() as cur:
            for metric, value, tmin, tmax, severity in alerts:
                cur.execute("""
                    INSERT INTO alerts (patient_id, metric, value, threshold_min, threshold_max, severity, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (data["patient_id"], metric, value, tmin, tmax, severity, data["timestamp"]))
        conn.commit()
        print(f"[Storage] {len(alerts)} alerte(s) sauvegardee(s) pour {data['patient_id']}")


def save_metrics_influx(write_api, data):
    metrics = data["metrics"]
    timestamp = data["timestamp"]
    patient_id = data["patient_id"]
    condition = data["condition"]

    points = []
    for metric_name, value in metrics.items():
        point = (
            Point("health_metrics")
            .tag("patient_id", patient_id)
            .tag("condition", condition)
            .field(metric_name, float(value))
            .time(timestamp, WritePrecision.S)
        )
        points.append(point)

    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=points)


def main():
    print("[Storage] Demarrage...")
    pg_conn   = wait_for_postgres()
    influx    = wait_for_influx()
    write_api = influx.write_api(write_options=SYNCHRONOUS)
    consumer  = wait_for_kafka(KAFKA_BROKER, TOPIC)

    init_postgres(pg_conn)

    print("[Storage] En ecoute...\n")
    for message in consumer:
        data = message.value
        try:
            upsert_patient(pg_conn, data)
            save_alerts(pg_conn, data)
            save_metrics_influx(write_api, data)
            print(f"[Storage] {data['patient_id']} @ {data['timestamp']} — OK")
        except Exception as e:
            print(f"[Storage] Erreur: {e}")
            pg_conn.rollback()


if __name__ == "__main__":
    main()
