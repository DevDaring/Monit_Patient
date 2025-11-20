import api from './api'
import { Patient, VitalSigns, RiskScore } from '../types/patient.types'

export const patientService = {
  // Get all patients
  async getAllPatients(): Promise<Patient[]> {
    const response = await api.get('/api/patients/')
    return response.data
  },

  // Get single patient
  async getPatient(patientId: string): Promise<Patient> {
    const response = await api.get(`/api/patients/${patientId}`)
    return response.data
  },

  // Create patient
  async createPatient(patient: Partial<Patient>): Promise<{ status: string; patient_id: string }> {
    const response = await api.post('/api/patients/', patient)
    return response.data
  },

  // Get patient vitals
  async getPatientVitals(patientId: string, limit = 100): Promise<VitalSigns[]> {
    const response = await api.get(`/api/patients/${patientId}/vitals`, {
      params: { limit },
    })
    return response.data
  },

  // Add vital signs
  async addVitalSigns(vitals: Partial<VitalSigns>): Promise<{ status: string; patient_id: string }> {
    const response = await api.post('/api/patients/vitals', vitals)
    return response.data
  },

  // Get risk score
  async getRiskScore(patientId: string): Promise<RiskScore> {
    const response = await api.get(`/api/patients/${patientId}/risk-score`)
    return response.data
  },
}
