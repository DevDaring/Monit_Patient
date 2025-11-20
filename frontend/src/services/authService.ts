import api from './api'

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  token: string
  user: {
    user_id: string
    username: string
    email: string
    full_name: string
    role: string
  }
}

export const authService = {
  // Login
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    // For demo purposes, simulate login
    // In production, this would call the actual API
    if (credentials.username === 'admin' && credentials.password === 'admin') {
      const mockResponse: LoginResponse = {
        token: 'mock-jwt-token',
        user: {
          user_id: 'U001',
          username: 'admin',
          email: 'admin@hospital.com',
          full_name: 'Admin User',
          role: 'admin',
        },
      }
      localStorage.setItem('auth_token', mockResponse.token)
      return mockResponse
    }
    throw new Error('Invalid credentials')
  },

  // Logout
  async logout(): Promise<void> {
    localStorage.removeItem('auth_token')
  },

  // Check if authenticated
  isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token')
  },
}
