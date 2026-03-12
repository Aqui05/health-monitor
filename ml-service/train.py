"""
Entrainement du modele de detection d'anomalies.
Utilise Isolation Forest — algorithme non supervise ideal pour
detecter des valeurs aberrantes sans avoir besoin de donnees labelisees.
"""

import json
import os
import pickle
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Parametres
N_SAMPLES = 5000
CONTAMINATION = 0.05  # 5% d'anomalies estimees dans les donnees reelles
MODEL_PATH = "/app/model.pkl"
SCALER_PATH = "/app/scaler.pkl"
FEATURES = ["heart_rate", "glucose", "blood_pressure_systolic", "spo2", "temperature"]


def generate_training_data(n=N_SAMPLES):
    """
    Genere des donnees d'entrainement realistes.
    Majorite de donnees normales + quelques anomalies.
    """
    np.random.seed(42)

    # Donnees normales (95%)
    n_normal = int(n * 0.95)
    normal = np.column_stack([
        np.random.normal(75, 10, n_normal),    # heart_rate
        np.random.normal(100, 20, n_normal),   # glucose
        np.random.normal(120, 12, n_normal),   # blood_pressure
        np.random.normal(97.5, 1, n_normal),   # spo2
        np.random.normal(36.6, 0.3, n_normal), # temperature
    ])

    # Anomalies (5%) — valeurs extremes
    n_anomaly = n - n_normal
    anomalies = np.column_stack([
        np.random.choice([30, 160], n_anomaly),   # bradycardie ou tachycardie
        np.random.choice([40, 280], n_anomaly),   # hypoglycemie ou hyperglycemie
        np.random.choice([70, 200], n_anomaly),   # hypotension ou hypertension severe
        np.random.uniform(80, 92, n_anomaly),     # desaturation
        np.random.choice([35.0, 39.5], n_anomaly),# hypothermie ou fievre
    ])

    data = np.vstack([normal, anomalies])
    np.random.shuffle(data)
    return data


def train():
    print("[ML] Generation des donnees d'entrainement...")
    X = generate_training_data()

    print("[ML] Normalisation des features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("[ML] Entrainement Isolation Forest...")
    model = IsolationForest(
        n_estimators=100,
        contamination=CONTAMINATION,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_scaled)

    print("[ML] Sauvegarde du modele...")
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    # Test rapide
    test_normal = np.array([[75, 100, 120, 98, 36.6]])
    test_anomaly = np.array([[160, 280, 200, 85, 39.5]])

    pred_normal = model.predict(scaler.transform(test_normal))
    pred_anomaly = model.predict(scaler.transform(test_anomaly))

    print(f"[ML] Test normal (attendu: 1)  -> {pred_normal[0]}")
    print(f"[ML] Test anomalie (attendu: -1) -> {pred_anomaly[0]}")
    print("[ML] Modele pret.")


if __name__ == "__main__":
    train()
