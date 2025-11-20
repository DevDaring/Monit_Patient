import { create } from 'zustand'
import { Alert } from '../types/alert.types'
import { alertService } from '../services/alertService'

interface AlertState {
  alerts: Alert[]
  isLoading: boolean
  error: string | null
  fetchAlerts: (patientId?: string) => Promise<void>
  acknowledgeAlert: (alertId: string) => Promise<void>
  resolveAlert: (alertId: string) => Promise<void>
  addAlert: (alert: Alert) => void
}

export const useAlertStore = create<AlertState>((set) => ({
  alerts: [],
  isLoading: false,
  error: null,

  fetchAlerts: async (patientId?: string) => {
    set({ isLoading: true, error: null })
    try {
      const response = await alertService.getAlerts(patientId)
      set({ alerts: response.alerts, isLoading: false })
    } catch (error: any) {
      set({ error: error.message, isLoading: false })
    }
  },

  acknowledgeAlert: async (alertId: string) => {
    try {
      await alertService.acknowledgeAlert(alertId)
      set((state) => ({
        alerts: state.alerts.map((alert) =>
          alert.alert_id === alertId ? { ...alert, status: 'acknowledged' as const } : alert
        ),
      }))
    } catch (error: any) {
      set({ error: error.message })
    }
  },

  resolveAlert: async (alertId: string) => {
    try {
      await alertService.resolveAlert(alertId)
      set((state) => ({
        alerts: state.alerts.map((alert) =>
          alert.alert_id === alertId ? { ...alert, status: 'resolved' as const } : alert
        ),
      }))
    } catch (error: any) {
      set({ error: error.message })
    }
  },

  addAlert: (alert: Alert) => {
    set((state) => ({
      alerts: [alert, ...state.alerts],
    }))
  },
}))
