import { apiClient } from '@/lib/api'
import { DashboardResponseSchema } from '@/types/api'

export const dashboardService = {
  async getDashboardData(): Promise<DashboardResponseSchema> {
    const response = await apiClient.get<DashboardResponseSchema>('/dashboard/')
    return response.data
  },
}
