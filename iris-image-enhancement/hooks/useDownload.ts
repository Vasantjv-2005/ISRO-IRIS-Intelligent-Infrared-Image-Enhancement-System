'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { downloadService } from '@/services/download'

export function useDownload() {
  const [isDownloading, setIsDownloading] = useState(false)

  const downloadFile = async (filePath: string, customFilename?: string) => {
    if (!filePath) {
      toast.error('No file path provided for download')
      return
    }
    try {
      setIsDownloading(true)
      toast.info('Preparing download...')
      await downloadService.triggerDownload(filePath, customFilename)
      toast.success('Download initiated')
    } catch (err: any) {
      toast.error('Failed to download file')
      console.error(err)
    } finally {
      setIsDownloading(false)
    }
  }

  return {
    downloadFile,
    isDownloading,
  }
}
