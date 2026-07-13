import { apiClient } from '@/lib/api'
import { ComparisonRequestSchema, ComparisonResponseSchema } from '@/types/api'

export const comparisonService = {
  async compare(data: ComparisonRequestSchema): Promise<ComparisonResponseSchema> {
    const response = await apiClient.post<ComparisonResponseSchema>('/comparison/compare', data)
    return response.data
  },
}
