export const APP_CONFIG = {
  name: 'Monit Patient',
  tagline: 'Predict the future where uncertainty is the enemy',
  version: '1.0.0',
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  wsUrl: import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws',
}

export default APP_CONFIG
