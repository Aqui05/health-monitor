import { PatientsMap, Alert, Stats } from "./types";

const BASE = "/api/gateway";

export async function fetchPatients(): Promise<PatientsMap> {
  const res = await fetch(`${BASE}/patients/latest`, { cache: "no-store" });
  if (!res.ok) throw new Error("Erreur patients");
  return res.json();
}

export async function fetchAlerts(): Promise<Alert[]> {
  const res = await fetch(`${BASE}/alerts/recent`, { cache: "no-store" });
  if (!res.ok) throw new Error("Erreur alertes");
  return res.json();
}

export async function fetchStats(): Promise<Stats> {
  const res = await fetch(`${BASE}/stats`, { cache: "no-store" });
  if (!res.ok) throw new Error("Erreur stats");
  return res.json();
}
