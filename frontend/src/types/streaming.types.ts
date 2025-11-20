export interface StreamMessage {
  type: 'vitals' | 'alert' | 'agent_log' | 'system'
  data: any
  timestamp: string
}

export interface VitalsStreamMessage extends StreamMessage {
  type: 'vitals'
  data: {
    patient_id: string
    heart_rate: number
    bp_systolic: number
    bp_diastolic: number
    o2_saturation: number
    temperature: number
    respiratory_rate?: number
  }
}

export interface AlertStreamMessage extends StreamMessage {
  type: 'alert'
  data: {
    alert_id: string
    patient_id: string
    alert_type: string
    severity: 'low' | 'medium' | 'high' | 'critical'
    message: string
    details?: Record<string, any>
  }
}

export interface WebSocketConfig {
  url: string
  reconnect?: boolean
  reconnectInterval?: number
  maxReconnectAttempts?: number
}
