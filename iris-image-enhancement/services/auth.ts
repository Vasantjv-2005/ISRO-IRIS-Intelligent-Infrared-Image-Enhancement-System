import { apiClient } from '@/lib/api'

export interface UserRegisterInput {
  full_name: string
  email: string
  password: string
  confirm_password: string
}

export interface UserLoginInput {
  email: string
  password: string
}

export interface UserProfile {
  user_id: string
  full_name: string
  email: string
  is_active: boolean
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: {
    user_id: string
    full_name: string
    email: string
    is_active: boolean
    created_at: string
  }
  message: string
}

export const authService = {
  async register(data: UserRegisterInput): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/register', data)
    return response.data
  },

  async login(data: UserLoginInput): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/login', data)
    return response.data
  },
}
