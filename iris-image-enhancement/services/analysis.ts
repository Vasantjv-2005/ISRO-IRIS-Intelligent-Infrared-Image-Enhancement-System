import { apiClient } from '@/lib/api'
import { AnalysisRequestSchema, AnalysisResponseSchema } from '@/types/api'

export const analysisService = {
  async process(data: AnalysisRequestSchema): Promise<AnalysisResponseSchema> {
    const response = await apiClient.post<AnalysisResponseSchema>('/analysis/process', data)
    return response.data
  },
}
