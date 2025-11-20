import { useEffect } from 'react'
import { usePatientStore } from '../store/patientStore'

export function usePatientData(patientId?: string) {
  const {
    patients,
    selectedPatient,
    vitals,
    riskScores,
    isLoading,
    error,
    fetchPatients,
    fetchPatient,
    fetchVitals,
    fetchRiskScore,
  } = usePatientStore()

  useEffect(() => {
    if (!patients.length) {
      fetchPatients()
    }
  }, [patients.length, fetchPatients])

  useEffect(() => {
    if (patientId) {
      fetchPatient(patientId)
      fetchVitals(patientId)
      fetchRiskScore(patientId)
    }
  }, [patientId, fetchPatient, fetchVitals, fetchRiskScore])

  return {
    patients,
    selectedPatient,
    vitals: patientId ? vitals[patientId] || [] : [],
    riskScore: patientId ? riskScores[patientId] : undefined,
    isLoading,
    error,
    refreshPatient: () => patientId && fetchPatient(patientId),
    refreshVitals: () => patientId && fetchVitals(patientId),
    refreshRiskScore: () => patientId && fetchRiskScore(patientId),
  }
}
