import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { usePatientStore } from '../store/patientStore'
import { useAlertStore } from '../store/alertStore'
import { AlertCircle, Activity, Users } from 'lucide-react'

export default function DashboardPage() {
  const { patients, fetchPatients, isLoading } = usePatientStore()
  const { alerts, fetchAlerts } = useAlertStore()
  const navigate = useNavigate()

  useEffect(() => {
    fetchPatients()
    fetchAlerts()
  }, [fetchPatients, fetchAlerts])

  const criticalPatients = patients.filter((p) => p.status === 'critical')
  const activeAlerts = alerts.filter((a) => a.status === 'active')

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Patient Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Total Patients</p>
              <p className="text-3xl font-bold text-gray-900">{patients.length}</p>
            </div>
            <Users className="w-12 h-12 text-primary-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Critical Patients</p>
              <p className="text-3xl font-bold text-danger-600">{criticalPatients.length}</p>
            </div>
            <AlertCircle className="w-12 h-12 text-danger-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Active Alerts</p>
              <p className="text-3xl font-bold text-warning-600">{activeAlerts.length}</p>
            </div>
            <Activity className="w-12 h-12 text-warning-500" />
          </div>
        </div>
      </div>

      {/* Patients List */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">All Patients</h2>
        </div>
        <div className="p-6">
          {isLoading ? (
            <p className="text-gray-600">Loading patients...</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {patients.map((patient) => (
                <div
                  key={patient.patient_id}
                  onClick={() => navigate(`/patient/${patient.patient_id}`)}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-gray-900">{patient.name}</h3>
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        patient.status === 'critical'
                          ? 'bg-danger-100 text-danger-700'
                          : 'bg-success-100 text-success-700'
                      }`}
                    >
                      {patient.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">ID: {patient.patient_id}</p>
                  <p className="text-sm text-gray-600">
                    {patient.age} years • {patient.gender}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">
                    Room: {patient.room_number || 'N/A'}
                  </p>
                  <p className="text-sm font-medium text-gray-900 mt-2">
                    {patient.diagnosis || 'No diagnosis'}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
