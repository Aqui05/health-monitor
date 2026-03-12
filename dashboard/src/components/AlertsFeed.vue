<template>
  <div class="alerts-feed">
    <h3>⚠️ Alertes récentes</h3>
    <div v-if="alerts.length === 0" class="empty">Aucune alerte</div>
    <div
      v-for="alert in alerts.slice(0, 15)"
      :key="alert.id"
      class="alert-item"
      :class="severityClass(alert.severity)"
    >
      <span class="alert-severity">{{ alert.severity }}</span>
      <span class="alert-patient">{{ alert.patient_id }}</span>
      <span class="alert-metric">{{ metricLabel(alert.metric) }}</span>
      <span class="alert-value">{{ alert.value }}</span>
      <span class="alert-time">{{ formatTime(alert.timestamp) }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({ alerts: { type: Array, default: () => [] } })

function severityClass(s) {
  return { critical: s === 'CRITICAL', warning: s === 'WARNING' }
}

const LABELS = {
  heart_rate: 'FC',
  glucose: 'Glycémie',
  blood_pressure_systolic: 'Tension',
  spo2: 'SpO2',
  temperature: 'Temp.'
}

function metricLabel(m) { return LABELS[m] || m }
function formatTime(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleTimeString()
}
</script>

<style scoped>
.alerts-feed { background: #1e2130; border-radius: 12px; padding: 1.2rem; }
h3 { color: #e2e8f0; margin: 0 0 1rem; font-size: 1rem; }
.empty { color: #475569; font-size: 0.85rem; text-align: center; padding: 1rem; }
.alert-item {
  display: grid;
  grid-template-columns: 80px 90px 80px 60px 1fr;
  gap: 0.5rem;
  align-items: center;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  margin-bottom: 0.3rem;
  font-size: 0.78rem;
}
.alert-item.critical { background: #450a0a; }
.alert-item.warning  { background: #3d2a00; }
.alert-severity { font-weight: 700; }
.critical .alert-severity { color: #f87171; }
.warning  .alert-severity { color: #facc15; }
.alert-patient { color: #94a3b8; }
.alert-metric  { color: #cbd5e1; }
.alert-value   { color: #f1f5f9; font-weight: 600; }
.alert-time    { color: #475569; text-align: right; }
</style>
