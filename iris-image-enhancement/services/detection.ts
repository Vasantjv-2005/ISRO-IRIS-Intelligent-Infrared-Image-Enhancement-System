import { apiClient } from '@/lib/api'
import { DetectionRequestSchema, DetectionResponseSchema } from '@/types/api'

export const detectionService = {
  async process(data: DetectionRequestSchema): Promise<DetectionResponseSchema> {
    const response = await apiClient.post<DetectionResponseSchema>('/detection/process', data)
    return response.data
  },
}
