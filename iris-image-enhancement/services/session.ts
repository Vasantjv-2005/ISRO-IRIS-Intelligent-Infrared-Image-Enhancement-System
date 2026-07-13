import { apiClient } from '@/lib/api'
import { SessionModel } from '@/types/api'

export const sessionService = {
  async createSession(uploadId: string): Promise<SessionModel> {
    const response = await apiClient.post<SessionModel>(`/sessions/?upload_id=${encodeURIComponent(uploadId)}`)
    return response.data
  },

  async listSessions(limit: number = 20): Promise<SessionModel[]> {
    const response = await apiClient.get<SessionModel[]>(`/sessions/?limit=${limit}`)
    return response.data
  },

  async getSession(sessionId: string): Promise<SessionModel> {
    const response = await apiClient.get<SessionModel>(`/sessions/${encodeURIComponent(sessionId)}`)
    return response.data
  },

  async deleteSession(sessionId: string): Promise<{ success: boolean; message: string }> {
    const response = await apiClient.delete<{ success: boolean; message: string }>(
      `/sessions/${encodeURIComponent(sessionId)}`
    )
    return response.data
  },
}
