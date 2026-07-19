import { apiClient } from '@/lib/api'
import { ComparisonRequestSchema, MultiComparisonRequestSchema, ComparisonResponseSchema } from '@/types/api'

export const comparisonService = {
  async compare(data: ComparisonRequestSchema): Promise<ComparisonResponseSchema> {
    const response = await apiClient.post<ComparisonResponseSchema>('/comparison/compare', data)
    return response.data
  },
  async compareMulti(data: MultiComparisonRequestSchema): Promise<ComparisonResponseSchema> {
    const response = await apiClient.post<ComparisonResponseSchema>('/comparison/multi', data)
    return response.data
  },
}

