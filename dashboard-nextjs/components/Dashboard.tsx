"use client";
import { useState, useEffect, useCallback } from "react";
import { PatientsMap, Alert, Stats } from "@/lib/types";
import PatientCard from "./PatientCard";
import AlertsFeed from "./AlertsFeed";
import StatsBar from "./StatsBar";
import { formatTime } from "@/lib/utils";

const POLL_INTERVAL = 2000;

const DEFAULT_STATS: Stats = { total_patients: 0, alerts_last_hour: 0, high_risk_count: 0 };

export default function Dashboard() {
  const [patients, setPatients]     = useState<PatientsMap>({});
  const [alerts, setAlerts]         = useState<Alert[]>([]);
  const [stats, setStats]           = useState<Stats>(DEFAULT_STATS);
  const [lastUpdate, setLastUpdate] = useState<string>("");
  const [connected, setConnected]   = useState(false);

  const fetchAll = useCallback(async () => {
    try {
      const [pRes, aRes, sRes] = await Promise.all([
        fetch("/api/gateway/patients/latest"),
        fetch("/api/gateway/alerts/recent"),
        fetch("/api/gateway/stats"),
      ]);

      if (!pRes.ok || !aRes.ok || !sRes.ok) throw new Error("API error");

      const [p, a, s] = await Promise.all([pRes.json(), aRes.json(), sRes.json()]);

      setPatients(p);
      setAlerts(a);
      setStats(s);
      setLastUpdate(formatTime(new Date().toISOString()));
      setConnected(true);
    } catch {
      setConnected(false);
    }
  }, []);

  useEffect(() => {
    fetchAll();
    const interval = setInterval(fetchAll, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [fetchAll]);

  const patientList = Object.values(patients);

  return (
    <div className="min-h-screen flex flex-col bg-[#0a0f1e]">
      <StatsBar stats={stats} lastUpdate={lastUpdate} connected={connected} />

      <div className="flex-1 flex overflow-hidden">
        {/* Patients grid */}
        <main className="flex-1 overflow-y-auto p-6">
          <h2 className="text-xs font-semibold uppercase tracking-widest text-slate-500 mb-4">
            Patients surveillés
          </h2>

          {patientList.length === 0 ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-center">
                <div className="w-8 h-8 border-2 border-slate-600 border-t-emerald-400 rounded-full animate-spin mx-auto mb-3" />
                <p className="text-slate-500 text-sm">Connexion à l'API...</p>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {patientList.map((patient) => (
                <PatientCard key={patient.patient_id} patient={patient} />
              ))}
            </div>
          )}
        </main>

        {/* Alerts sidebar */}
        <aside className="w-80 flex-shrink-0 border-l border-slate-700/50 overflow-hidden flex flex-col">
          <AlertsFeed alerts={alerts} />
        </aside>
      </div>
    </div>
  );
}
