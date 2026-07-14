import { apiClient, getFileDownloadUrl } from '@/lib/api'

export const downloadService = {
  getDownloadUrl(filePath: string): string {
    return getFileDownloadUrl(filePath)
  },

  async downloadFileBlob(filePath: string): Promise<Blob> {
    if (filePath.startsWith('data:') || filePath.startsWith('blob:')) {
      const res = await fetch(filePath)
      return await res.blob()
    }

    let cleanPath = filePath
    if (filePath.includes('file_path=')) {
      try {
        const urlObj = new URL(filePath, typeof window !== 'undefined' ? window.location.origin : 'http://localhost')
        const param = urlObj.searchParams.get('file_path')
        if (param) {
          cleanPath = param
        } else {
          const match = filePath.match(/file_path=([^&]+)/)
          if (match && match[1]) cleanPath = decodeURIComponent(match[1])
        }
      } catch (e) {
        const match = filePath.match(/file_path=([^&]+)/)
        if (match && match[1]) cleanPath = decodeURIComponent(match[1])
      }
    } else if (filePath.startsWith('http://') || filePath.startsWith('https://')) {
      const res = await fetch(filePath)
      return await res.blob()
    }

    try {
      const response = await apiClient.get(`/download/?file_path=${encodeURIComponent(cleanPath)}`, {
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
