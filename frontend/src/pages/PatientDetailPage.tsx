import { useParams, useNavigate } from 'react-router-dom'
import { usePatientData } from '../hooks/usePatientData'
import { ArrowLeft, Activity, AlertCircle } from 'lucide-react'

export default function PatientDetailPage() {
  const { patientId } = useParams<{ patientId: string }>()
  const navigate = useNavigate()
  const { selectedPatient, vitals, riskScore, isLoading } = usePatientData(patientId)

  if (isLoading) {
    return <div className="text-center py-12">Loading patient data...</div>
  }

  if (!selectedPatient) {
    return <div className="text-center py-12">Patient not found</div>
  }

  return (
    <div>
      <button
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
      >
        <ArrowLeft className="w-5 h-5" />
        Back
      </button>

      <h1 className="text-3xl font-bold text-gray-900 mb-6">Patient Details</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Patient Info */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Patient Information</h2>
          <dl className="space-y-2">
            <div>
              <dt className="text-sm text-gray-600">Name</dt>
              <dd className="font-medium text-gray-900">{selectedPatient.name}</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-600">ID</dt>
              <dd className="font-medium text-gray-900">{selectedPatient.patient_id}</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-600">Age</dt>
              <dd className="font-medium text-gray-900">{selectedPatient.age} years</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-600">Gender</dt>
              <dd className="font-medium text-gray-900 capitalize">{selectedPatient.gender}</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-600">Room</dt>
              <dd className="font-medium text-gray-900">{selectedPatient.room_number}</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-600">Diagnosis</dt>
              <dd className="font-medium text-gray-900">{selectedPatient.diagnosis}</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-600">Status</dt>
              <dd>
                <span
                  className={`inline-block px-2 py-1 text-xs rounded-full ${
                    selectedPatient.status === 'critical'
                      ? 'bg-danger-100 text-danger-700'
                      : 'bg-success-100 text-success-700'
                  }`}
                >
                  {selectedPatient.status}
                </span>
              </dd>
            </div>
          </dl>
        </div>

        {/* Risk Score */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Risk Assessment</h2>
          {riskScore ? (
            <div>
              <div className="text-center mb-4">
                <div className="text-5xl font-bold text-gray-900 mb-2">
                  {riskScore.risk_score}
                </div>
                <div className="text-sm text-gray-600">Risk Score (0-100)</div>
              </div>
              <div className="mb-4">
                <span
                  className={`inline-block px-4 py-2 rounded-full text-sm font-medium ${
                    riskScore.risk_level === 'critical'
                      ? 'bg-danger-100 text-danger-700'
                      : riskScore.risk_level === 'high'
                      ? 'bg-warning-100 text-warning-700'
                      : riskScore.risk_level === 'medium'
                      ? 'bg-warning-50 text-warning-600'
                      : 'bg-success-100 text-success-700'
                  }`}
                >
                  {riskScore.risk_level.toUpperCase()}
                </span>
              </div>
              {riskScore.concerns && riskScore.concerns.length > 0 && (
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Concerns:</h3>
                  <ul className="space-y-1">
                    {riskScore.concerns.map((concern, index) => (
                      <li key={index} className="text-sm text-gray-700 flex items-start gap-2">
                        <AlertCircle className="w-4 h-4 text-warning-500 mt-0.5" />
                        {concern}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <p className="text-gray-600">No risk data available</p>
          )}
        </div>

        {/* Latest Vitals */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Latest Vitals</h2>
          {vitals && vitals.length > 0 ? (
            <dl className="space-y-3">
              <div>
                <dt className="text-sm text-gray-600">Heart Rate</dt>
                <dd className="text-2xl font-bold text-gray-900">
                  {vitals[0].heart_rate} <span className="text-sm text-gray-600">bpm</span>
                </dd>
              </div>
              <div>
                <dt className="text-sm text-gray-600">Blood Pressure</dt>
                <dd className="text-2xl font-bold text-gray-900">
                  {vitals[0].bp_systolic}/{vitals[0].bp_diastolic}{' '}
                  <span className="text-sm text-gray-600">mmHg</span>
                </dd>
              </div>
              <div>
                <dt className="text-sm text-gray-600">O2 Saturation</dt>
                <dd className="text-2xl font-bold text-gray-900">
                  {vitals[0].o2_saturation} <span className="text-sm text-gray-600">%</span>
                </dd>
              </div>
              <div>
                <dt className="text-sm text-gray-600">Temperature</dt>
                <dd className="text-2xl font-bold text-gray-900">
                  {vitals[0].temperature} <span className="text-sm text-gray-600">°C</span>
                </dd>
              </div>
            </dl>
          ) : (
            <p className="text-gray-600">No vitals data available</p>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-6 flex gap-4">
        <button
          onClick={() => navigate(`/chat/${patientId}`)}
          className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors"
        >
          Chat with AI about this patient
        </button>
      </div>
    </div>
  )
}
