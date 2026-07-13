import { apiClient, getFileDownloadUrl } from '@/lib/api'

export const downloadService = {
  getDownloadUrl(filePath: string): string {
    return getFileDownloadUrl(filePath)
  },

  async downloadFileBlob(filePath: string): Promise<Blob> {
    const response = await apiClient.get(`/download/?file_path=${encodeURIComponent(filePath)}`, {
      responseType: 'blob',
    })
    return response.data
  },

  async triggerDownload(filePath: string, customFilename?: string): Promise<void> {
    const blob = await this.downloadFileBlob(filePath)
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    const filename = customFilename || filePath.split('/').pop() || filePath.split('\\').pop() || 'download'
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  },
}
