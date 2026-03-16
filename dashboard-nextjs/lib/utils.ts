import { RiskLevel } from "./types";

export function riskColor(level: RiskLevel): string {
  return level === "HIGH"   ? "text-red-500"
       : level === "MEDIUM" ? "text-amber-500"
       :                      "text-emerald-500";
}

export function riskBg(level: RiskLevel): string {
  return level === "HIGH"   ? "bg-red-500/10   border-red-500/30"
       : level === "MEDIUM" ? "bg-amber-500/10 border-amber-500/30"
       :                      "bg-emerald-500/10 border-emerald-500/30";
}

export function riskBadge(level: RiskLevel): string {
  return level === "HIGH"   ? "bg-red-500   text-white"
       : level === "MEDIUM" ? "bg-amber-500 text-white"
       :                      "bg-emerald-500 text-white";
}

export function severityColor(s: string): string {
  return s === "CRITICAL" ? "bg-red-500/20 text-red-400 border-red-500/30"
                           : "bg-amber-500/20 text-amber-400 border-amber-500/30";
}

export function metricLabel(key: string): string {
  const map: Record<string, string> = {
    heart_rate:                "FC",
    glucose:                   "Glycémie",
    blood_pressure_systolic:   "Tension",
    spo2:                      "SpO2",
    temperature:               "Temp.",
  };
  return map[key] ?? key;
}

export function metricUnit(key: string): string {
  const map: Record<string, string> = {
    heart_rate:                "bpm",
    glucose:                   "mg/dL",
    blood_pressure_systolic:   "mmHg",
    spo2:                      "%",
    temperature:               "°C",
  };
  return map[key] ?? "";
}

export function metricIcon(key: string): string {
  const map: Record<string, string> = {
    heart_rate:                "❤️",
    glucose:                   "🩸",
    blood_pressure_systolic:   "💉",
    spo2:                      "🫁",
    temperature:               "🌡️",
  };
  return map[key] ?? "📊";
}

export function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString("fr-FR", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}
