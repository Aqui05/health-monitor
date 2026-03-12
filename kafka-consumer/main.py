"""
Kafka Consumer — Health Monitoring System
Consomme les donnees de sante depuis Kafka, detecte les anomalies simples
et affiche les alertes en temps reel.
"""

import json
import os
import time

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = os.getenv("TOPIC", "health-data")

# Seuils d'alerte cliniques
THRESHOLDS = {
    "heart_rate":              {"min": 50,  "max": 120},
    "glucose":                 {"min": 70,  "max": 180},
    "blood_pressure_systolic": {"min": 90,  "max": 160},
    "spo2":                    {"min": 94,  "max": 100},
    "temperature":             {"min": 35.5,"max": 38.5},
}

ALERT_LABELS = {
    "heart_rate":              "Frequence cardiaque",
    "glucose":                 "Glycemie",
    "blood_pressure_systolic": "Tension arterielle",
    "spo2":                    "Saturation O2",
    "temperature":             "Temperature",
}

UNITS = {
    "heart_rate": "bpm",
    "glucose": "mg/dL",
    "blood_pressure_systolic": "mmHg",
    "spo2": "%",
    "temperature": "C",
}


def check_anomalies(metrics: dict) -> list:
    alerts = []
    for key, limits in THRESHOLDS.items():
        value = metrics.get(key)
        if value is None:
            continue
        if value < limits["min"]:
            alerts.append(f"  ⚠ {ALERT_LABELS[key]}: {value} {UNITS[key]} — TROP BAS (seuil: {limits['min']})")
        elif value > limits["max"]:
            alerts.append(f"  ⚠ {ALERT_LABELS[key]}: {value} {UNITS[key]} — TROP ELEVE (seuil: {limits['max']})")
    return alerts


def wait_for_kafka(broker: str, topic: str, retries: int = 10, delay: int = 5) -> KafkaConsumer:
    for attempt in range(retries):
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=broker,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                auto_offset_reset="latest",
                group_id="health-monitor-group",
            )
            print(f"[Consumer] Connecte a Kafka ({broker}), ecoute le topic '{topic}'")
            return consumer
        except NoBrokersAvailable:
            print(f"[Consumer] Kafka non disponible, tentative {attempt+1}/{retries}...")
            time.sleep(delay)
    raise RuntimeError("Impossible de se connecter a Kafka.")


def main():
    consumer = wait_for_kafka(KAFKA_BROKER, TOPIC)

    print("[Consumer] En attente de donnees...\n")
    for message in consumer:
        data = message.value
        pid = data.get("patient_id", "?")
        condition = data.get("condition", "?")
        ts = data.get("timestamp", "?")
        metrics = data.get("metrics", {})

        print(f"[{ts}] {pid} ({condition})")
        print(f"  HR: {metrics.get('heart_rate')} bpm | "
              f"Glucose: {metrics.get('glucose')} mg/dL | "
              f"BP: {metrics.get('blood_pressure_systolic')} mmHg | "
              f"SpO2: {metrics.get('spo2')}% | "
              f"Temp: {metrics.get('temperature')}C")

        alerts = check_anomalies(metrics)
        if alerts:
            print("  --- ALERTES DETECTEES ---")
            for alert in alerts:
                print(alert)
        print()


if __name__ == "__main__":
    main()
