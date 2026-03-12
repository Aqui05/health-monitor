"""
IoT Simulator — Health Monitoring System
Simule des capteurs de santé pour N patients et publie les données sur Kafka.
Métriques : fréquence cardiaque, glycémie, tension artérielle, SpO2, température.
"""

import json
import os
import random
import time
import uuid
from datetime import datetime

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = os.getenv("TOPIC", "health-data")
NUM_PATIENTS = int(os.getenv("PATIENTS", 5))
INTERVAL = float(os.getenv("INTERVAL", 2))

PATIENTS = [
    {
        "id": f"patient-{i+1}",
        "name": f"Patient {i+1}",
        "age": random.randint(40, 80),
        "condition": random.choice(["diabetes", "hypertension", "healthy", "cardiac_risk"])
    }
    for i in range(NUM_PATIENTS)
]


def generate_reading(patient: dict) -> dict:
    condition = patient["condition"]

    # Frequence cardiaque (bpm) — normale: 60-100
    hr_base = 75
    if condition == "cardiac_risk":
        hr_base = random.choice([45, 130])
    heart_rate = hr_base + random.gauss(0, 8)

    # Glycemie (mg/dL) — normale: 70-140
    glucose_base = 100
    if condition == "diabetes":
        glucose_base = random.choice([180, 250, 60])
    glucose = glucose_base + random.gauss(0, 15)

    # Tension systolique (mmHg) — normale: 90-140
    bp_base = 120
    if condition == "hypertension":
        bp_base = random.choice([160, 180, 200])
    blood_pressure = bp_base + random.gauss(0, 10)

    # SpO2 % — normale: 95-100
    spo2 = 98 + random.gauss(0, 1)
    if condition == "cardiac_risk" and random.random() < 0.1:
        spo2 = random.uniform(88, 93)

    # Temperature corporelle (C) — normale: 36.1-37.2
    temperature = 36.6 + random.gauss(0, 0.3)

    return {
        "event_id": str(uuid.uuid4()),
        "patient_id": patient["id"],
        "patient_name": patient["name"],
        "age": patient["age"],
        "condition": condition,
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": {
            "heart_rate": round(heart_rate, 1),
            "glucose": round(glucose, 1),
            "blood_pressure_systolic": round(blood_pressure, 1),
            "spo2": round(min(100, spo2), 1),
            "temperature": round(temperature, 2),
        }
    }


def wait_for_kafka(broker: str, retries: int = 10, delay: int = 5) -> KafkaProducer:
    for attempt in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=broker,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                acks="all",
            )
            print(f"[IoT Simulator] Connecte a Kafka ({broker})")
            return producer
        except NoBrokersAvailable:
            print(f"[IoT Simulator] Kafka non disponible, tentative {attempt+1}/{retries}...")
            time.sleep(delay)
    raise RuntimeError("Impossible de se connecter a Kafka.")


def main():
    print(f"[IoT Simulator] Demarrage — {NUM_PATIENTS} patients, intervalle {INTERVAL}s")
    producer = wait_for_kafka(KAFKA_BROKER)

    while True:
        for patient in PATIENTS:
            reading = generate_reading(patient)
            producer.send(TOPIC, value=reading)
            print(
                f"[IoT] {reading['patient_id']} | "
                f"HR: {reading['metrics']['heart_rate']} bpm | "
                f"Glucose: {reading['metrics']['glucose']} mg/dL | "
                f"BP: {reading['metrics']['blood_pressure_systolic']} mmHg"
            )
        producer.flush()
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
