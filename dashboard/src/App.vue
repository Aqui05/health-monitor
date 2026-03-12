<template>
  <div class="app">
    <header>
      <div class="logo">🏥 Health Monitor</div>
      <div class="status">
        <span class="dot" :class="{ online: connected }"></span>
        <span>{{ connected ? 'Connecté' : 'Déconnecté' }}</span>
        <span v-if="lastUpdate" class="update-time">· Màj {{ lastUpdate }}</span>
      </div>
      <div class="stats">
        <div class="stat">
          <span class="stat-value">{{ patientList.length }}</span>
          <span class="stat-label">Patients</span>
        </div>
        <div class="stat">
          <span class="stat-value red">{{ highRiskCount }}</span>
          <span class="stat-label">Risque élevé</span>
        </div>
        <div class="stat">
          <span class="stat-value yellow">{{ alerts.length }}</span>
          <span class="stat-label">Alertes</span>
        </div>
      </div>
    </header>

    <main>
      <section class="patients-section">
        <h2>Patients surveillés</h2>
        <div class="patients-grid">
          <PatientCard
            v-for="patient in patientList"
            :key="patient.patient_id"
            :patient="patient"
          />
          <div v-if="patientList.length === 0" class="no-data">
            En attente de données...
          </div>
        </div>
      </section>

      <section class="alerts-section">
        <AlertsFeed :alerts="alerts" />
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import PatientCard from './components/PatientCard.vue'
import AlertsFeed from './components/AlertsFeed.vue'
import { useHealthData } from './composables/useHealthData.js'

const { patients, alerts, connected, lastUpdate } = useHealthData()

const patientList = computed(() => Object.values(patients.value))
const highRiskCount = computed(() =>
  patientList.value.filter(p => p.risk_level === 'HIGH').length
)
</script>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: #0f1117;
  color: #e2e8f0;
  font-family: 'Segoe UI', system-ui, sans-serif;
  min-height: 100vh;
}

.app { max-width: 1400px; margin: 0 auto; padding: 1.5rem; }

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  padding: 1rem 1.5rem;
  background: #1e2130;
  border-radius: 12px;
  flex-wrap: wrap;
  gap: 1rem;
}

.logo { font-size: 1.3rem; font-weight: 700; color: #4ade80; }

.status { display: flex; align-items: center; gap: 0.4rem; font-size: 0.85rem; color: #94a3b8; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: #475569; }
.dot.online { background: #4ade80; box-shadow: 0 0 6px #4ade80; }
.update-time { color: #475569; }

.stats { display: flex; gap: 1.5rem; }
.stat { text-align: center; }
.stat-value { display: block; font-size: 1.5rem; font-weight: 700; color: #f1f5f9; }
.stat-value.red    { color: #f87171; }
.stat-value.yellow { color: #facc15; }
.stat-label { font-size: 0.7rem; color: #64748b; }

main { display: grid; grid-template-columns: 1fr 380px; gap: 1.5rem; }

.patients-section h2 { color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em; }
.patients-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; }

.no-data { color: #475569; text-align: center; padding: 2rem; grid-column: 1/-1; }

@media (max-width: 900px) {
  main { grid-template-columns: 1fr; }
}
</style>
