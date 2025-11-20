import api from './api'
import { Alert } from '../types/alert.types'

export const alertService = {
  // Get alerts
  async getAlerts(patientId?: string): Promise<{ status: string; alerts: Alert[]; count: number }> {
    const response = await api.get('/api/alerts/', {
      params: patientId ? { patient_id: patientId } : undefined,
    })
    return response.data
  },

  // Acknowledge alert
  async acknowledgeAlert(alertId: string): Promise<{ status: string; message: string }> {
    const response = await api.post(`/api/alerts/${alertId}/acknowledge`)
    return response.data
  },

  // Resolve alert
  async resolveAlert(alertId: string): Promise<{ status: string; message: string }> {
    const response = await api.post(`/api/alerts/${alertId}/resolve`)
    return response.data
  },
}
