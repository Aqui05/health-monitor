import json
import os
import threading
import time

import psycopg2
import psycopg2.extras
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

PG_HOST      = os.getenv("PG_HOST", "postgres")
PG_PORT      = int(os.getenv("PG_PORT", 5432))
PG_DB        = os.getenv("PG_DB", "healthdb")
PG_USER      = os.getenv("PG_USER", "health")
PG_PASSWORD  = os.getenv("PG_PASSWORD", "health123")
ML_SERVICE   = os.getenv("ML_SERVICE", "http://ml-service:8000")

app = FastAPI(title="Health Monitor API Gateway")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def get_db():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT, dbname=PG_DB,
        user=PG_USER, password=PG_PASSWORD
    )


def score_patient(metrics: dict) -> dict:
    """Appelle le ml-service pour scorer les metriques d'un patient."""
    try:
        response = requests.post(
            f"{ML_SERVICE}/predict",
            json=metrics,
            timeout=1.0
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return {"is_anomaly": False, "anomaly_score": None, "risk_level": "LOW"}


@app.get("/patients/latest")
def get_latest_patients():
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, condition, latest_metrics, last_seen FROM patients")
            rows = cur.fetchall()
    finally:
        conn.close()

    result = {}
    for row in rows:
        pid = row["id"]
        metrics = row["latest_metrics"] if row["latest_metrics"] else {}
        ml_result = score_patient(metrics) if metrics else {"is_anomaly": False, "anomaly_score": None, "risk_level": "LOW"}
        result[pid] = {
            "patient_id": pid,
            "condition": row["condition"],
            "timestamp": row["last_seen"].isoformat() if row["last_seen"] else None,
            "metrics": metrics,
            "risk_level": ml_result.get("risk_level", "LOW"),
            "anomaly_score": ml_result.get("anomaly_score"),
            "is_anomaly": ml_result.get("is_anomaly", False),
        }

    return result


@app.get("/alerts/recent")
def get_recent_alerts():
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT id, patient_id, metric, value, severity, timestamp
                FROM alerts ORDER BY timestamp DESC LIMIT 50
            """)
            rows = cur.fetchall()
    finally:
        conn.close()

    return [
        {**dict(row), "timestamp": row["timestamp"].isoformat() if row["timestamp"] else None}
        for row in rows
    ]


@app.get("/stats")
def get_stats():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM patients")
            total_patients = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM alerts WHERE timestamp > NOW() - INTERVAL '1 hour'")
            alerts_last_hour = cur.fetchone()[0]
    finally:
        conn.close()
    return {"total_patients": total_patients, "alerts_last_hour": alerts_last_hour}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=False)
