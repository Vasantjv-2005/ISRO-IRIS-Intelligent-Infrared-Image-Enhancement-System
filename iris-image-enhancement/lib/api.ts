import axios, { AxiosInstance, AxiosError } from 'axios'

// Initialize Axios instance with base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Clear token on unauthorized
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token')
      }
    }
    return Promise.reject(error)
  }
)

// Auth APIs
export const authAPI = {
  register: (data: { full_name: string; email: string; password: string; confirm_password: string }) =>
    apiClient.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    apiClient.post('/auth/login', data),
}

// Health & Dashboard APIs
export const systemAPI = {
  health: () => apiClient.get('/health'),
  dashboard: () => apiClient.get('/dashboard/'),
}

// Upload APIs
export const uploadAPI = {
  upload: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

// Preprocessing APIs
export const preprocessingAPI = {
  process: (data: {
    image_path: string
    output_directory: string
    apply_denoise?: boolean
    apply_contrast?: boolean
    [key: string]: any
  }) => apiClient.post('/preprocessing/process', data),
}

// Enhancement APIs
export const enhancementAPI = {
  process: (imagePath: string) =>
    apiClient.post(`/enhancement/process?image_path=${encodeURIComponent(imagePath)}`),
}

// Colorization APIs
export const colorizationAPI = {
  process: (data: {
    image_path: string
    colormap: string
    super_resolution?: boolean
    backend?: string
  }) => apiClient.post('/colorization/process', data),
}

// Detection APIs
export const detectionAPI = {
  process: (data: {
    image_path: string
    output_directory: string
    confidence: number
  }) => apiClient.post('/detection/process', data),
}

// Analysis APIs
export const analysisAPI = {
  process: (data: {
    image_path: string
    context?: string
    prompt?: string
  }) => apiClient.post('/analysis/process', data),
}

// Comparison APIs
export const comparisonAPI = {
  compare: (uploadId: string) =>
    apiClient.post('/comparison/compare', { upload_id: uploadId }),
}

// Report APIs
export const reportAPI = {
  generate: (data: {
    upload_id: string
    title?: string
    notes?: string
    include_detections?: boolean
    include_analysis?: boolean
  }) => apiClient.post('/report/generate', data),
  download: (filePath: string) =>
    apiClient.get(`/download/?file_path=${encodeURIComponent(filePath)}`, {
      responseType: 'blob',
    }),
}

// Sessions APIs
export const sessionsAPI = {
  list: () => apiClient.get('/sessions/'),
  create: (uploadId: string) =>
    apiClient.post(`/sessions/?upload_id=${encodeURIComponent(uploadId)}`),
  delete: (sessionId: string) =>
    apiClient.delete(`/sessions/${sessionId}`),
}

// Helper functions for auth pages
export async function login(email: string, password: string) {
  const response = await authAPI.login({ email, password })
  return response.data
}

export async function register(
  full_name: string,
  email: string,
  password: string,
  confirm_password: string
) {
  const response = await authAPI.register({ full_name, email, password, confirm_password })
  return response.data
}

export default apiClient
