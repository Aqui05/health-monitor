# 🏥 Health Monitor — Dashboard Next.js

Frontend Next.js 15 + TypeScript du système distribué de surveillance des maladies chroniques.
Remplace / complète le dashboard Vue.js en consommant la même API Gateway (port 5000).

## 🚀 Lancement

> Le backend Health Monitor doit être démarré au préalable :
> ```bash
> cd ~/health-monitor && docker compose up
> ```

```bash
cd ~/health-monitor-dashboard
npm install
npm run dev   # démarre sur le port 3001
```

Ouvrir [http://localhost:3001](http://localhost:3001)

| Vue | URL | Stack |
|---|---|---|
| Dashboard Vue.js (original) | http://localhost:3000 | Vue 3 + Vite |
| Dashboard Next.js (nouveau) | http://localhost:3001 | Next.js 15 + TypeScript |

## 🏗️ Architecture

```
app/
├── layout.tsx          # Layout global dark
└── page.tsx            # Page principale → <Dashboard />

components/
├── Dashboard.tsx       # Client component — polling toutes les 2s
├── StatsBar.tsx        # Header avec KPIs et statut connexion
├── PatientCard.tsx     # Carte patient avec métriques et score ML
├── MetricTile.tsx      # Tuile individuelle d'une métrique
└── AlertsFeed.tsx      # Fil d'alertes temps réel

lib/
├── types.ts            # Types TypeScript (Patient, Alert, Stats...)
├── api.ts              # Fonctions fetch vers l'API Gateway
└── utils.ts            # Helpers (couleurs, labels, formatage)
```

## 🛠️ Stack

- **Next.js 15** App Router
- **TypeScript** strict
- **Tailwind CSS** dark theme
- **Polling** toutes les 2 secondes via `setInterval`
- **Proxy Next.js** → redirige `/api/gateway/*` vers `localhost:5000`

## 👤 Auteur

**Aquilas KIKISSAGBE** — [GitHub](https://github.com/Aqui05)
