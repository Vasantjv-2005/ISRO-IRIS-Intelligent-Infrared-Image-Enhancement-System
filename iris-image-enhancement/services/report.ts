import { apiClient } from '@/lib/api'
import { ReportRequestSchema, ReportResponseSchema } from '@/types/api'

export const reportService = {
  async generate(data: ReportRequestSchema): Promise<ReportResponseSchema> {
    const response = await apiClient.post<ReportResponseSchema>('/report/generate', data)
    return response.data
  },
}
