# 🏥 Health Monitor — Système Distribué de Surveillance des Maladies Chroniques

![Architecture](https://img.shields.io/badge/Architecture-Microservices-blue)
![Kafka](https://img.shields.io/badge/Kafka-Streaming-orange)
![ML](https://img.shields.io/badge/ML-Isolation%20Forest-green)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D)
![Next.js](https://img.shields.io/badge/Next.js-15-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6)

Système temps réel de surveillance de patients atteints de maladies chroniques (diabète, hypertension, risque cardiaque). Les données de capteurs IoT sont collectées, traitées via un pipeline Kafka, scorées par un modèle de Machine Learning et visualisées sur **deux dashboards** : Vue.js 3 et Next.js 15 + TypeScript.

---

## 🎯 Fonctionnalités

- **Simulation IoT** — génération de données médicales réalistes pour N patients (fréquence cardiaque, glycémie, tension artérielle, SpO2, température)
- **Pipeline temps réel** — ingestion et distribution via Apache Kafka
- **Détection d'anomalies ML** — modèle Isolation Forest entraîné sur 5000 lectures simulées
- **Stockage hybride** — PostgreSQL pour les alertes et profils patients, InfluxDB pour les séries temporelles
- **Deux dashboards** — Vue.js 3 (port 3000) et Next.js 15 + TypeScript (port 3001), tous deux rafraîchis toutes les 2 secondes
- **API REST** — FastAPI exposant les données aux clients

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        COLLECTE IoT                             │
│   ┌──────────────┐                                              │
│   │ IoT Simulator│  5 patients · 5 métriques · toutes les 2s    │
│   └──────┬───────┘                                              │
└──────────┼──────────────────────────────────────────────────────┘
           │ Kafka Producer
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MESSAGERIE DISTRIBUÉE                        │
│   ┌─────────────────────────────────────────┐                   │
│   │      Apache Kafka + Zookeeper           │                   │
│   │      Topic: health-data                 │                   │
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
│   ┌─────────────────────────────────────────┐                   │
│   │           API Gateway (FastAPI)         │                   │
│   │   GET /patients/latest                  │                   │
│   │   GET /alerts/recent                    │                   │
│   │   GET /stats                            │                   │
│   └──────────────────┬──────────────────────┘                   │
└──────────────────────┼──────────────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌──────────────────┐     ┌──────────────────────┐
│ Dashboard Vue.js │     │ Dashboard Next.js    │
│ Vue 3 + Vite     │     │ Next.js 15+TypeScript│
│ Port 3000        │     │ Port 3001            │
└──────────────────┘     └──────────────────────┘
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
| Frontend v1 | Vue.js 3 + Vite | Dashboard temps réel (port 3000) |
| Frontend v2 | Next.js 15 + TypeScript | Dashboard dark theme (port 3001) |
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
| **Dashboard Vue.js** | http://localhost:3000 | Interface Vue.js 3 + Vite |
| **Dashboard Next.js** | http://localhost:3001 | Interface Next.js 15 + TypeScript (dark theme) |
| **API Gateway** | http://localhost:5000 | API REST (patients, alertes, stats) |
| **ML Service** | http://localhost:8000 | Endpoint de prédiction |
| **Kafka UI** | http://localhost:8080 | Interface Kafka |
| **InfluxDB** | http://localhost:8086 | UI time-series (admin/health123) |

---

## 🖥️ Les deux dashboards

### Dashboard Vue.js 3 — port 3000

Interface légère construite avec Vue.js 3 (Options API + Composables) et Vite.

```
dashboard/
├── src/
│   ├── App.vue                   # Layout + stats header
│   ├── components/
│   │   ├── PatientCard.vue       # Carte patient + métriques + badge risque
│   │   └── AlertsFeed.vue        # Fil alertes temps réel
│   └── composables/
│       └── useHealthData.js      # Polling API toutes les 2s
├── vite.config.js                # Proxy /api → api-gateway:5000
└── Dockerfile
```

### Dashboard Next.js 15 — port 3001

Interface dark theme construite avec Next.js 15 App Router et TypeScript strict.

```
dashboard-nextjs/
├── app/
│   ├── layout.tsx                # Layout global dark theme
│   └── page.tsx                  # Page principale → <Dashboard />
├── components/
│   ├── Dashboard.tsx             # Client component — polling toutes les 2s
│   ├── StatsBar.tsx              # Header avec KPIs et statut connexion
│   ├── PatientCard.tsx           # Carte patient typée TypeScript
│   ├── MetricTile.tsx            # Tuile individuelle d'une métrique
│   └── AlertsFeed.tsx            # Fil d'alertes temps réel
├── lib/
│   ├── types.ts                  # Types TypeScript (Patient, Alert, Stats...)
│   ├── api.ts                    # Fonctions fetch vers l'API Gateway
│   └── utils.ts                  # Helpers (couleurs, labels, formatage)
├── next.config.mjs               # Proxy /api/gateway/* → api-gateway:5000
└── Dockerfile
```

**Comparaison des deux dashboards :**

| Critère | Vue.js (port 3000) | Next.js (port 3001) |
|---|---|---|
| Langage | JavaScript | TypeScript strict |
| Framework | Vue 3 + Vite | Next.js 15 App Router |
| Thème | Clair | Sombre |
| Typage | Dynamique | Statique (compile-time) |
| Proxy | Vite dev server | Next.js rewrites |

---

## 🤖 Modèle ML — Isolation Forest

Le service ML utilise un **Isolation Forest** — algorithme non supervisé de détection d'anomalies. Il est entraîné sur 5000 lectures simulées (95% normales, 5% anomalies) et score chaque nouvelle lecture en temps réel.

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
├── kafka-consumer/         # Consumer console (alertes)
├── storage-service/        # Persistance PostgreSQL + InfluxDB
├── ml-service/             # Détection d'anomalies (Isolation Forest)
├── api-gateway/            # API REST exposée aux dashboards
├── dashboard/              # Frontend Vue.js 3 — port 3000
├── dashboard-nextjs/       # Frontend Next.js 15 + TypeScript — port 3001
└── docker-compose.yml      # Orchestration complète (10 services)
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