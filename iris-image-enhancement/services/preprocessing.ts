import { apiClient } from '@/lib/api'
import { PreprocessingRequestSchema, PreprocessingResponseSchema } from '@/types/api'

export const preprocessingService = {
  async process(data: PreprocessingRequestSchema): Promise<PreprocessingResponseSchema> {
    const response = await apiClient.post<PreprocessingResponseSchema>('/preprocessing/process', data)
    return response.data
  },
}
