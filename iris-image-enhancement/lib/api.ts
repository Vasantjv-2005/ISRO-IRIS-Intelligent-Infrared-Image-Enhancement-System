import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import { uploadService } from '@/services/upload'

// Initialize Axios instance with base URL from environment variable
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds timeout for intensive AI processing
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request Interceptor: Attach Auth token if available & log telemetry
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// Response Interceptor: Error handling & automatic retry for transient network errors
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const config = error.config as InternalAxiosRequestConfig & { _retryCount?: number }
    if (config && !config._retryCount && (error.code === 'ECONNABORTED' || !error.response || error.response.status >= 500)) {
      config._retryCount = 1
      await new Promise((resolve) => setTimeout(resolve, 1000))
      return apiClient(config)
    }

    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token')
      }
    }
    return Promise.reject(error)
  }
)

// Helper to convert any backend file_path into an accessible download/preview URL
export function getFileDownloadUrl(filePath: string | undefined | null): string {
  if (!filePath) return ''
  if (
    filePath.startsWith('http://') ||
    filePath.startsWith('https://') ||
    filePath.startsWith('data:') ||
    filePath.startsWith('blob:')
  ) {
    return filePath
  }
  return `${API_BASE_URL}/download/?file_path=${encodeURIComponent(filePath)}`
}

// System API for Header Telemetry & Diagnostics
export const systemAPI = {
  health: () => apiClient.get('/health'),
  getStatus: () => apiClient.get('/health'),
}

// Auth API & helpers for Auth pages/context
export const authAPI = {
  login: (data: any) => apiClient.post('/auth/login', data),
  register: (data: any) => apiClient.post('/auth/register', data),
  me: () => apiClient.get('/auth/me'),
}

export async function login(email: string, password?: string): Promise<any> {
  const response = await apiClient.post('/auth/login', { email, password })
  return response.data
}

export async function register(
  full_name: string,
  email: string,
  password?: string,
  confirm_password?: string
): Promise<any> {
  const response = await apiClient.post('/auth/register', { full_name, email, password, confirm_password })
  return response.data
}

// Upload API helper compatibility
export const uploadAPI = {
  upload: async (file: File) => {
    const res = await uploadService.uploadImage(file)
    return { data: res }
  },
}

export default apiClient
