import { useAuth } from '../../hooks/useAuth'
import { useAlertStore } from '../../store/alertStore'
import { Bell, LogOut } from 'lucide-react'
import { useEffect } from 'react'

export default function Header() {
  const { user, logout } = useAuth()
  const { alerts, fetchAlerts } = useAlertStore()

  useEffect(() => {
    fetchAlerts()
  }, [fetchAlerts])

  const activeAlerts = alerts.filter((a) => a.status === 'active')

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="px-6 py-4 flex items-center justify-between">
        <div className="flex items-center">
          <h1 className="text-2xl font-bold text-primary-600">Monit Patient</h1>
          <p className="ml-4 text-sm text-gray-600 italic">
            "Predict the future where uncertainty is the enemy"
          </p>
        </div>

        <div className="flex items-center gap-4">
          {/* Alert Bell */}
          <button className="relative p-2 hover:bg-gray-100 rounded-full">
            <Bell className="w-6 h-6 text-gray-600" />
            {activeAlerts.length > 0 && (
              <span className="absolute top-0 right-0 bg-danger-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                {activeAlerts.length}
              </span>
            )}
          </button>

          {/* User Info */}
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">{user?.full_name}</p>
              <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
            </div>

            {/* Logout */}
            <button
              onClick={logout}
              className="p-2 hover:bg-gray-100 rounded-full"
              title="Logout"
            >
              <LogOut className="w-5 h-5 text-gray-600" />
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
