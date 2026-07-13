import { apiClient } from '@/lib/api'
import { EnhancementResponseSchema } from '@/types/api'

export const enhancementService = {
  async process(imagePath: string): Promise<EnhancementResponseSchema> {
    const response = await apiClient.post<EnhancementResponseSchema>(
      `/enhancement/process?image_path=${encodeURIComponent(imagePath)}`
    )
    return response.data
  },
}
