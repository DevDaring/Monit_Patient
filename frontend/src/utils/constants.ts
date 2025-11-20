export const RISK_LEVELS = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  CRITICAL: 'critical',
} as const

export const PATIENT_STATUS = {
  ACTIVE: 'active',
  DISCHARGED: 'discharged',
  CRITICAL: 'critical',
} as const

export const ALERT_STATUS = {
  ACTIVE: 'active',
  ACKNOWLEDGED: 'acknowledged',
  RESOLVED: 'resolved',
} as const

export const AGENT_TYPES = {
  ORCHESTRATOR: 'orchestrator',
  SUPER: 'super',
  UTILITY: 'utility',
} as const
