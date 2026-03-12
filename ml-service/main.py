"""
ML Service — Health Monitoring System
- Expose une API FastAPI /predict pour scorer des lectures
- Consomme Kafka en temps reel et publie les scores sur le topic 'health-scores'
"""

import json
import os
import pickle
import threading
import time

import numpy as np
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable
from pydantic import BaseModel

KAFKA_BROKER    = os.getenv("KAFKA_BROKER", "localhost:9092")
INPUT_TOPIC     = os.getenv("INPUT_TOPIC", "health-data")
OUTPUT_TOPIC    = os.getenv("OUTPUT_TOPIC", "health-scores")
MODEL_PATH      = "/app/model.pkl"
SCALER_PATH     = "/app/scaler.pkl"
FEATURES        = ["heart_rate", "glucose", "blood_pressure_systolic", "spo2", "temperature"]

app = FastAPI(title="Health ML Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Chargement du modele au demarrage
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)

print("[ML Service] Modele charge.")


class HealthReading(BaseModel):
    heart_rate: float
    glucose: float
    blood_pressure_systolic: float
    spo2: float
    temperature: float


def score_reading(metrics: dict) -> dict:
    """Retourne le score d'anomalie et la prediction."""
    X = np.array([[metrics[f] for f in FEATURES]])
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)[0]       # 1 = normal, -1 = anomalie
    score = model.score_samples(X_scaled)[0]      # Plus le score est bas, plus c'est anormal

    is_anomaly = bool(prediction == -1)
    threshold = model.offset_
    margin = score - threshold

    if is_anomaly and margin < -0.05:
        risk = "HIGH"
    elif is_anomaly:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "is_anomaly": is_anomaly,
        "anomaly_score": round(float(score), 4),
        "risk_level": risk
    }


@app.get("/health")
def health():
    return {"status": "ok", "model": "IsolationForest"}


@app.post("/predict")
def predict(reading: HealthReading):
    result = score_reading(reading.dict())
    return result


@app.post("/predict/batch")
def predict_batch(readings: list[HealthReading]):
    return [score_reading(r.dict()) for r in readings]


def kafka_scoring_loop():
    """Thread qui consomme Kafka et publie les scores en temps reel."""
    time.sleep(5)
    try:
        consumer = KafkaConsumer(
            INPUT_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="latest",
            group_id="ml-service-group",
        )
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        print("[ML Service] Kafka connecte — scoring en temps reel actif")

        for message in consumer:
            data = message.value
            metrics = data.get("metrics", {})
            try:
                result = score_reading(metrics)
                output = {
                    "patient_id": data["patient_id"],
                    "timestamp": data["timestamp"],
                    "condition": data["condition"],
                    "metrics": metrics,
                    **result,
                }
                producer.send(OUTPUT_TOPIC, value=output)

                if result["is_anomaly"]:
                    print(f"[ML] ANOMALIE {result['risk_level']} — {data['patient_id']} "
                          f"| score: {result['anomaly_score']}")
            except Exception as e:
                print(f"[ML] Erreur scoring: {e}")

    except Exception as e:
        print(f"[ML] Kafka non disponible: {e}")


# Lancement du thread Kafka en arriere-plan
threading.Thread(target=kafka_scoring_loop, daemon=True).start()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
