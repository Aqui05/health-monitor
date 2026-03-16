import { metricIcon, metricLabel, metricUnit } from "@/lib/utils";

interface Props {
  metricKey: string;
  value: number | undefined;
}

export default function MetricTile({ metricKey, value }: Props) {
  return (
    <div className="bg-slate-800/60 rounded-xl border border-slate-700/50 p-3 flex flex-col items-center gap-1">
      <span className="text-lg">{metricIcon(metricKey)}</span>
      <span className="metric-val text-slate-100">
        {value !== undefined ? value.toFixed(1) : "—"}
      </span>
      <span className="text-xs text-slate-500">{metricUnit(metricKey)}</span>
      <span className="text-xs text-slate-400 font-medium">{metricLabel(metricKey)}</span>
    </div>
  );
}
