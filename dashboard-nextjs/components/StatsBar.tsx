import { Stats } from "@/lib/types";

interface Props {
  stats: Stats;
  lastUpdate: string;
  connected: boolean;
}

export default function StatsBar({ stats, lastUpdate, connected }: Props) {
  return (
    <header className="bg-slate-900/80 backdrop-blur border-b border-slate-700/50 px-6 py-3 flex items-center justify-between flex-wrap gap-3">
      {/* Logo */}
      <div className="flex items-center gap-3">
        <span className="text-2xl">🏥</span>
        <div>
          <h1 className="font-display text-xl font-semibold text-slate-100 leading-none">
            Health Monitor
          </h1>
          <p className="text-xs text-slate-500">Surveillance temps réel</p>
        </div>
      </div>

      {/* Stats */}
      <div className="flex items-center gap-6">
        <div className="text-center">
          <p className="text-2xl font-bold font-mono text-slate-100">{stats.total_patients}</p>
          <p className="text-xs text-slate-500">Patients</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-bold font-mono text-red-400">{stats.high_risk_count}</p>
          <p className="text-xs text-slate-500">Risque élevé</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-bold font-mono text-amber-400">{stats.alerts_last_hour}</p>
          <p className="text-xs text-slate-500">Alertes / heure</p>
        </div>
      </div>

      {/* Status */}
      <div className="flex items-center gap-2 text-sm">
        <span className={`w-2 h-2 rounded-full ${connected ? "bg-emerald-400 animate-pulse" : "bg-red-500"}`} />
        <span className="text-slate-400">
          {connected ? "Connecté" : "Déconnecté"}
        </span>
        {lastUpdate && (
          <span className="text-slate-600 font-mono text-xs">· Màj {lastUpdate}</span>
        )}
      </div>
    </header>
  );
}
