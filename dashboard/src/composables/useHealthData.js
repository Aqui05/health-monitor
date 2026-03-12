import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

export function useHealthData() {
  const patients = ref({})
  const alerts = ref([])
  const connected = ref(false)
  const lastUpdate = ref(null)
  let interval = null

  async function fetchLatest() {
    try {
      const [patientsRes, alertsRes] = await Promise.all([
        axios.get('/api/patients/latest'),
        axios.get('/api/alerts/recent')
      ])
      patients.value = patientsRes.data
      alerts.value = alertsRes.data
      connected.value = true
      lastUpdate.value = new Date().toLocaleTimeString()
    } catch (e) {
      connected.value = false
    }
  }

  onMounted(() => {
    fetchLatest()
    interval = setInterval(fetchLatest, 2000)
  })

  onUnmounted(() => clearInterval(interval))

  return { patients, alerts, connected, lastUpdate }
}
