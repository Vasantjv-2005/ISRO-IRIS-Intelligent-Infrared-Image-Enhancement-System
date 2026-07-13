import { apiClient, getFileDownloadUrl } from '@/lib/api'

export const downloadService = {
  getDownloadUrl(filePath: string): string {
    return getFileDownloadUrl(filePath)
  },

  async downloadFileBlob(filePath: string): Promise<Blob> {
    if (filePath.startsWith('data:')) {
      const res = await fetch(filePath)
      return await res.blob()
    }
    try {
      const response = await apiClient.get(`/download/?file_path=${encodeURIComponent(filePath)}`, {
        responseType: 'blob',
      })
      return response.data
    } catch (err) {
      const res = await fetch(filePath)
      return await res.blob()
    }
  },

  async triggerDownload(filePath: string, customFilename?: string): Promise<void> {
    try {
      const blob = await this.downloadFileBlob(filePath)
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      const filename = customFilename || filePath.split('/').pop() || filePath.split('\\').pop() || 'detected_image.jpg'
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      const link = document.createElement('a')
      link.href = filePath
      link.setAttribute('download', customFilename || 'detected_image.jpg')
      link.target = '_blank'
      document.body.appendChild(link)
      link.click()
      link.remove()
    }
  },
}
