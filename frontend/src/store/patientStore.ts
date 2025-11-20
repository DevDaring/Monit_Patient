import { create } from 'zustand'
import { Patient, VitalSigns, RiskScore } from '../types/patient.types'
import { patientService } from '../services/patientService'

interface PatientState {
  patients: Patient[]
  selectedPatient: Patient | null
  vitals: Record<string, VitalSigns[]>
  riskScores: Record<string, RiskScore>
  isLoading: boolean
  error: string | null
  fetchPatients: () => Promise<void>
  fetchPatient: (patientId: string) => Promise<void>
  fetchVitals: (patientId: string) => Promise<void>
  fetchRiskScore: (patientId: string) => Promise<void>
  setSelectedPatient: (patient: Patient | null) => void
}

export const usePatientStore = create<PatientState>((set, get) => ({
  patients: [],
  selectedPatient: null,
  vitals: {},
  riskScores: {},
  isLoading: false,
  error: null,

  fetchPatients: async () => {
    set({ isLoading: true, error: null })
    try {
      const patients = await patientService.getAllPatients()
      set({ patients, isLoading: false })
    } catch (error: any) {
      set({ error: error.message, isLoading: false })
    }
  },

  fetchPatient: async (patientId: string) => {
    set({ isLoading: true, error: null })
    try {
      const patient = await patientService.getPatient(patientId)
      set({ selectedPatient: patient, isLoading: false })
    } catch (error: any) {
      set({ error: error.message, isLoading: false })
    }
  },

  fetchVitals: async (patientId: string) => {
    try {
      const vitalsData = await patientService.getPatientVitals(patientId)
      set((state) => ({
        vitals: { ...state.vitals, [patientId]: vitalsData },
      }))
    } catch (error: any) {
      set({ error: error.message })
    }
  },

  fetchRiskScore: async (patientId: string) => {
    try {
      const riskScore = await patientService.getRiskScore(patientId)
      set((state) => ({
        riskScores: { ...state.riskScores, [patientId]: riskScore },
      }))
    } catch (error: any) {
      set({ error: error.message })
    }
  },

  setSelectedPatient: (patient: Patient | null) => {
    set({ selectedPatient: patient })
  },
}))
