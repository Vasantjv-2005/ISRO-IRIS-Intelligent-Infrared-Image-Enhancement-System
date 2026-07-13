import { apiClient } from '@/lib/api'
import { ColorizationResponseSchema } from '@/types/api'

export interface ColorizationParams {
  image_path: string
  colormap?: string
  super_resolution?: boolean
  backend?: string
}

export const colorizationService = {
  async process({
    image_path,
    colormap = 'inferno',
    super_resolution = true,
    backend,
  }: ColorizationParams): Promise<ColorizationResponseSchema> {
    const params = new URLSearchParams({
      image_path,
      colormap,
      super_resolution: String(super_resolution),
    })
    if (backend) {
      params.append('backend', backend)
    }
    const response = await apiClient.post<ColorizationResponseSchema>(`/colorization/process?${params.toString()}`)
    return response.data
  },
}
