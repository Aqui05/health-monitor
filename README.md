# 🏥 Health Monitor — Système Distribué de Surveillance des Maladies Chroniques

![Architecture](https://img.shields.io/badge/Architecture-Microservices-blue)
![Kafka](https://img.shields.io/badge/Kafka-Streaming-orange)
![ML](https://img.shields.io/badge/ML-Isolation%20Forest-green)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D)

Système temps réel de surveillance de patients atteints de maladies chroniques (diabète, hypertension, risque cardiaque). Les données de capteurs IoT sont collectées, traitées via un pipeline Kafka, scorées par un modèle de Machine Learning et visualisées sur un dashboard Vue.js.

---

## 🎯 Fonctionnalités

- **Simulation IoT** — génération de données médicales réalistes pour N patients (fréquence cardiaque, glycémie, tension artérielle, SpO2, température)
- **Pipeline temps réel** — ingestion et distribution via Apache Kafka
- **Détection d'anomalies ML** — modèle Isolation Forest entraîné sur 5000 lectures simulées
- **Stockage hybride** — PostgreSQL pour les alertes et profils patients, InfluxDB pour les séries temporelles
- **Dashboard interactif** — Vue.js avec rafraîchissement automatique toutes les 2 secondes
- **API REST** — FastAPI exposant les données aux clients

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        COLLECTE IoT                             │
│                                                                 │
│   ┌──────────────┐                                              │
│   │ IoT Simulator│  5 patients · 5 métriques · toutes les 2s    │
│   │   (Python)   │                                              │
│   └──────┬───────┘                                              │
└──────────┼──────────────────────────────────────────────────────┘
           │ Kafka Producer
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MESSAGERIE DISTRIBUÉE                        │
│                                                                 │
│   ┌─────────────────────────────────────────┐                   │
│   │         Apache Kafka + Zookeeper        │                   │
│   │         Topic: health-data              │                   │
│   └────┬──────────────┬──────────────┬──────┘                   │
└────────┼──────────────┼──────────────┼──────────────────────────┘
         │              │              │
         ▼              ▼              ▼
  ┌──────────┐  ┌──────────────┐  ┌──────────┐
  │  Console │  │   Storage    │  │    ML    │
  │ Consumer │  │   Service    │  │ Service  │
  │ (alertes)│  │ (PostgreSQL  │  │(Isolation│
  │          │  │ + InfluxDB)  │  │ Forest)  │
  └──────────┘  └──────────────┘  └────┬─────┘
                                        │ HTTP /predict
                                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                       EXPOSITION API                            │
│                                                                 │
│   ┌─────────────────────────────────────────┐                   │
│   │           API Gateway (FastAPI)         │                   │
│   │   GET /patients/latest                  │                   │
│   │   GET /alerts/recent                    │                   │
│   └──────────────────┬──────────────────────┘                   │
└──────────────────────┼──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      VISUALISATION                              │
│                                                                 │
│   ┌─────────────────────────────────────────┐                   │
│   │         Dashboard Vue.js 3 + Vite       │                   │
│   │   • Cartes patients temps réel          │                   │
│   │   • Scores ML (LOW / MEDIUM / HIGH)     │                   │
│   │   • Fil d'alertes cliniques             │                   │
│   └─────────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Stack Technique

| Composant | Technologie | Rôle |
|---|---|---|
| Messagerie | Apache Kafka 7.5 + Zookeeper | Transport des événements IoT |
| Simulation IoT | Python 3.11 | Génération de données patients |
| Stockage relationnel | PostgreSQL 15 | Profils patients + alertes |
| Stockage temporel | InfluxDB 2.7 | Métriques time-series |
| Machine Learning | scikit-learn (Isolation Forest) | Détection d'anomalies |
| API | FastAPI + Uvicorn | Exposition REST |
| Frontend | Vue.js 3 + Vite | Dashboard temps réel |
| Conteneurisation | Docker + Docker Compose | Orchestration |

---

## 🚀 Lancement

### Prérequis

- Docker >= 24.0
- Docker Compose >= 2.0
- 4 Go de RAM disponibles

### Démarrage

```bash
git clone https://github.com/Aqui05/health-monitor.git
cd health-monitor
docker compose up --build
```

> ⚠️ Premier lancement : ~3-5 minutes (téléchargement des images Kafka/InfluxDB)

### Arrêt et nettoyage complet

```bash
# Arrêt simple
docker compose down

# Arrêt + suppression des volumes (repart de zéro)
docker compose down -v
```

---

## 🌐 Services disponibles

| Service | URL | Description |
|---|---|---|
| **Dashboard** | http://localhost:3000 | Interface de visualisation |
| **API Gateway** | http://localhost:5000 | API REST (patients, alertes) |
| **ML Service** | http://localhost:8000 | Endpoint de prédiction |
| **Kafka UI** | http://localhost:8080 | Interface Kafka |
| **InfluxDB** | http://localhost:8086 | UI time-series (admin/health123) |

---

## 🤖 Modèle ML — Isolation Forest

Le service ML utilise un **Isolation Forest** — algorithme non supervisé de détection d'anomalies. Il est entraîné sur 5000 lectures simulées (95% normales, 5% anomalies) et scorer chaque nouvelle lecture en temps réel.

**Métriques surveillées et seuils cliniques :**

| Métrique | Unité | Normal | Alerte |
|---|---|---|---|
| Fréquence cardiaque | bpm | 60 – 100 | < 50 ou > 120 |
| Glycémie | mg/dL | 70 – 140 | < 70 ou > 180 |
| Tension systolique | mmHg | 90 – 140 | < 90 ou > 160 |
| SpO2 | % | 95 – 100 | < 94 |
| Température | °C | 36.1 – 37.2 | < 35.5 ou > 38.5 |

**Niveaux de risque :**
- 🟢 **LOW** — métriques normales, modèle ne détecte pas d'anomalie
- 🟡 **MEDIUM** — anomalie détectée, légèrement au-delà du seuil appris
- 🔴 **HIGH** — anomalie sévère, bien au-delà du seuil

**Tester le modèle manuellement :**

```bash
# Patient normal
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"heart_rate": 75, "glucose": 100, "blood_pressure_systolic": 120, "spo2": 98, "temperature": 36.6}'

# Patient en crise
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"heart_rate": 160, "glucose": 280, "blood_pressure_systolic": 200, "spo2": 85, "temperature": 39.5}'
```

---

## 🗄️ Structure du projet

```
health-monitor/
├── iot-simulator/          # Simulateur de capteurs IoT
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── kafka-consumer/         # Consumer console (alertes)
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── storage-service/        # Persistance PostgreSQL + InfluxDB
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── ml-service/             # Détection d'anomalies (Isolation Forest)
│   ├── train.py            # Entraînement du modèle
│   ├── main.py             # API FastAPI + scoring Kafka
│   ├── requirements.txt
│   └── Dockerfile
├── api-gateway/            # API REST exposée au dashboard
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── dashboard/              # Frontend Vue.js 3
│   ├── src/
│   │   ├── App.vue
│   │   ├── components/
│   │   │   ├── PatientCard.vue
│   │   │   └── AlertsFeed.vue
│   │   └── composables/
│   │       └── useHealthData.js
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml      # Orchestration complète
```

---

## 💡 Choix d'architecture

**Pourquoi Kafka ?**
Kafka découple les producteurs des consommateurs. Le simulateur IoT publie sans se soucier de qui lit — le storage-service, le kafka-consumer et le ml-service lisent tous le même topic indépendamment. Ajouter un nouveau consommateur (ex: un service d'alerting SMS) ne nécessite aucune modification du simulateur.

**Pourquoi PostgreSQL + InfluxDB ?**
PostgreSQL stocke les données structurées avec relations (profils patients, alertes avec sévérité). InfluxDB est optimisé pour les requêtes temporelles — "évolution de la glycémie sur 24h" — ce que PostgreSQL ferait difficilement à grande échelle.

**Pourquoi Isolation Forest ?**
Algorithme non supervisé — pas besoin de données labelisées "normal/anomalie". Il apprend la distribution des données normales et détecte ce qui s'en écarte. Idéal pour la surveillance médicale où les cas anormaux sont rares et variés.

---

## 👤 Auteur

- GitHub: [@Aqui05](https://github.com/Aqui05)
