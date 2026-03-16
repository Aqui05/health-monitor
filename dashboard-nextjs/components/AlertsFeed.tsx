import { Alert } from "@/lib/types";
import { severityColor, metricLabel, formatTime } from "@/lib/utils";
import clsx from "clsx";

interface Props {
  alerts: Alert[];
}

export default function AlertsFeed({ alerts }: Props) {
  return (
    <div className="bg-slate-900/60 rounded-2xl border border-slate-700/50 flex flex-col h-full">
      <div className="px-5 py-4 border-b border-slate-700/50 flex items-center gap-2">
        <span className="text-amber-400 text-lg">⚠️</span>
        <h2 className="font-display text-lg font-semibold text-slate-100">Alertes récentes</h2>
      </div>

      <div className="flex-1 overflow-y-auto divide-y divide-slate-800/60">
        {alerts.length === 0 ? (
          <p className="text-center text-slate-500 py-10 text-sm">Aucune alerte</p>
        ) : (
          alerts.map((alert) => (
            <div key={alert.id} className="px-4 py-3 flex items-center gap-3 hover:bg-slate-800/30 transition-colors">
              <span
                className={clsx(
                  "text-xs font-bold px-2 py-0.5 rounded border flex-shrink-0",
                  severityColor(alert.severity)
                )}
              >
                {alert.severity}
              </span>
              <div className="flex-1 min-w-0">
                <p className="text-xs text-slate-300 truncate">
                  <span className="font-medium">{alert.patient_id}</span>
                  {" — "}
                  {metricLabel(alert.metric)}
                </p>
                <p className="text-xs text-slate-500">
                  {alert.value.toFixed(1)}
                </p>
              </div>
              <span className="text-xs text-slate-600 flex-shrink-0 font-mono">
                {formatTime(alert.timestamp)}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
