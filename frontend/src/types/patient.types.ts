export interface Patient {
  patient_id: string
  name: string
  age: number
  gender: string
  blood_type?: string
  admission_date: string
  assigned_doctor?: string
  room_number?: string
  diagnosis?: string
  medical_history?: string
  allergies?: string
  medications?: string
  emergency_contact?: string
  status: 'active' | 'discharged' | 'critical'
  created_at?: string
  updated_at?: string
}

export interface VitalSigns {
  vital_id?: string
  patient_id: string
  heart_rate: number
  bp_systolic: number
  bp_diastolic: number
  o2_saturation: number
  temperature: number
  respiratory_rate?: number
  timestamp: string
}

export interface RiskScore {
  patient_id: string
  risk_score: number
  risk_level: 'low' | 'medium' | 'high' | 'critical' | 'unknown'
  concerns: string[]
  latest_vitals?: VitalSigns
}
