import { apiClient } from '@/lib/api'
import { UploadResponseSchema } from '@/types/api'

export const uploadService = {
  async uploadImage(file: File): Promise<UploadResponseSchema> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await apiClient.post<UploadResponseSchema>('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}
