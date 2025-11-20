export interface Alert {
  alert_id: string
  patient_id: string
  alert_type: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  message: string
  details?: Record<string, any>
  status: 'active' | 'acknowledged' | 'resolved'
  created_by: string
  timestamp: string
  acknowledged_at?: string
  resolved_at?: string
}

export interface AlertFilter {
  patient_id?: string
  severity?: Alert['severity']
  status?: Alert['status']
  from_date?: string
  to_date?: string
}
