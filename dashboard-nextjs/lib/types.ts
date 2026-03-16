export type RiskLevel = "LOW" | "MEDIUM" | "HIGH";

export interface PatientMetrics {
  heart_rate?: number;
  glucose?: number;
  blood_pressure_systolic?: number;
  spo2?: number;
  temperature?: number;
}

export interface Patient {
  patient_id: string;
  condition: string;
  timestamp: string;
  metrics: PatientMetrics;
  risk_level: RiskLevel;
  anomaly_score: number | null;
  is_anomaly: boolean;
}

export interface Alert {
  id: number;
  patient_id: string;
  metric: string;
  value: number;
  severity: "WARNING" | "CRITICAL";
  timestamp: string;
}

export interface Stats {
  total_patients: number;
  alerts_last_hour: number;
  high_risk_count: number;
}

export type PatientsMap = Record<string, Patient>;
