import { Patient } from "@/lib/types";
import { riskBadge, riskBg, riskColor, formatTime } from "@/lib/utils";
import MetricTile from "./MetricTile";
import clsx from "clsx";

const METRIC_KEYS = [
  "heart_rate",
  "glucose",
  "blood_pressure_systolic",
  "spo2",
  "temperature",
];

interface Props {
  patient: Patient;
}

export default function PatientCard({ patient }: Props) {
  const isHigh = patient.risk_level === "HIGH";

  return (
    <div
      className={clsx(
        "rounded-2xl border p-5 flex flex-col gap-4 transition-all",
        riskBg(patient.risk_level),
        isHigh && "ring-pulse"
      )}
    >
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-display text-lg font-semibold text-slate-100">
            {patient.patient_id}
          </h3>
          <span className="text-xs text-slate-400 bg-slate-800/60 px-2 py-0.5 rounded-full border border-slate-700/50">
            {patient.condition}
          </span>
        </div>
        <span className={clsx("text-xs font-bold px-3 py-1 rounded-full", riskBadge(patient.risk_level))}>
          {patient.risk_level}
        </span>
      </div>

      {/* Metrics grid */}
      <div className="grid grid-cols-3 gap-2">
        {METRIC_KEYS.map((k) => (
          <MetricTile
            key={k}
            metricKey={k}
            value={patient.metrics?.[k as keyof typeof patient.metrics]}
          />
        ))}
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between text-xs text-slate-500 border-t border-slate-700/30 pt-3">
        <span>
          Score ML:{" "}
          <span className={clsx("font-mono font-medium", riskColor(patient.risk_level))}>
            {patient.anomaly_score !== null ? patient.anomaly_score.toFixed(4) : "—"}
          </span>
        </span>
        <span>{patient.timestamp ? formatTime(patient.timestamp) : "—"}</span>
      </div>
    </div>
  );
}
