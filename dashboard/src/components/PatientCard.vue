<template>
  <div class="patient-card" :class="riskClass">
    <div class="card-header">
      <div class="patient-info">
        <span class="patient-id">{{ patient.patient_id }}</span>
        <span class="condition-badge">{{ patient.condition }}</span>
      </div>
      <div class="risk-badge" :class="riskClass">
        {{ riskLevel }}
      </div>
    </div>

    <div class="metrics-grid">
      <div class="metric" :class="{ alert: isAlert(patient.metrics?.heart_rate, 50, 120) }">
        <span class="metric-icon">❤️</span>
        <span class="metric-value">{{ patient.metrics?.heart_rate ?? '—' }}</span>
        <span class="metric-unit">bpm</span>
        <span class="metric-label">Freq. cardiaque</span>
      </div>

      <div class="metric" :class="{ alert: isAlert(patient.metrics?.glucose, 70, 180) }">
        <span class="metric-icon">🩸</span>
        <span class="metric-value">{{ patient.metrics?.glucose ?? '—' }}</span>
        <span class="metric-unit">mg/dL</span>
        <span class="metric-label">Glycemie</span>
      </div>

      <div class="metric" :class="{ alert: isAlert(patient.metrics?.blood_pressure_systolic, 90, 160) }">
        <span class="metric-icon">💉</span>
        <span class="metric-value">{{ patient.metrics?.blood_pressure_systolic ?? '—' }}</span>
        <span class="metric-unit">mmHg</span>
        <span class="metric-label">Tension</span>
      </div>

      <div class="metric" :class="{ alert: isAlert(patient.metrics?.spo2, 94, 100, true) }">
        <span class="metric-icon">🫁</span>
        <span class="metric-value">{{ patient.metrics?.spo2 ?? '—' }}</span>
        <span class="metric-unit">%</span>
        <span class="metric-label">SpO2</span>
      </div>

      <div class="metric" :class="{ alert: isAlert(patient.metrics?.temperature, 35.5, 38.5) }">
        <span class="metric-icon">🌡️</span>
        <span class="metric-value">{{ patient.metrics?.temperature ?? '—' }}</span>
        <span class="metric-unit">°C</span>
        <span class="metric-label">Temperature</span>
      </div>

      <div class="metric ml-score" :class="riskClass">
        <span class="metric-icon">🤖</span>
        <span class="metric-value">{{ patient.anomaly_score ?? '—' }}</span>
        <span class="metric-unit">score</span>
        <span class="metric-label">Score ML</span>
      </div>
    </div>

    <div class="card-footer">
      <span class="timestamp">{{ patient.timestamp ? new Date(patient.timestamp).toLocaleTimeString() : '' }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  patient: { type: Object, required: true }
})

const riskLevel = computed(() => props.patient.risk_level ?? 'LOW')

const riskClass = computed(() => ({
  'risk-low': riskLevel.value === 'LOW',
  'risk-medium': riskLevel.value === 'MEDIUM',
  'risk-high': riskLevel.value === 'HIGH',
}))

function isAlert(value, min, max, invertMin = false) {
  if (value == null) return false
  return value < min || value > max
}
</script>

<style scoped>
.patient-card {
  background: #1e2130;
  border-radius: 12px;
  padding: 1.2rem;
  border-left: 4px solid #4ade80;
  transition: all 0.3s ease;
}
.patient-card.risk-medium { border-left-color: #facc15; }
.patient-card.risk-high   { border-left-color: #f87171; animation: pulse 1.5s infinite; }

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(248, 113, 113, 0.3); }
  50%       { box-shadow: 0 0 0 8px rgba(248, 113, 113, 0); }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.patient-id { font-weight: 700; color: #e2e8f0; font-size: 1rem; }
.condition-badge {
  margin-left: 0.5rem;
  font-size: 0.7rem;
  background: #2d3748;
  color: #94a3b8;
  padding: 2px 8px;
  border-radius: 999px;
}
.risk-badge {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 999px;
}
.risk-badge.risk-low    { background: #14532d; color: #4ade80; }
.risk-badge.risk-medium { background: #713f12; color: #facc15; }
.risk-badge.risk-high   { background: #7f1d1d; color: #f87171; }

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.6rem;
}
.metric {
  background: #2d3748;
  border-radius: 8px;
  padding: 0.6rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 0.85rem;
}
.metric.alert { background: #450a0a; }
.metric-icon  { font-size: 1rem; margin-bottom: 2px; }
.metric-value { font-weight: 700; color: #f1f5f9; font-size: 1rem; }
.metric-unit  { font-size: 0.65rem; color: #64748b; }
.metric-label { font-size: 0.65rem; color: #94a3b8; text-align: center; margin-top: 2px; }
.ml-score.risk-high   .metric-value { color: #f87171; }
.ml-score.risk-medium .metric-value { color: #facc15; }
.ml-score.risk-low    .metric-value { color: #4ade80; }

.card-footer { margin-top: 0.8rem; text-align: right; }
.timestamp { font-size: 0.7rem; color: #475569; }
</style>
