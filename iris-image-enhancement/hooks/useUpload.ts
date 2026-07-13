'use client'

import { useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { uploadService } from '@/services/upload'
import { sessionService } from '@/services/session'
import { useImage } from '@/lib/context/ImageContext'
import { usePipeline } from '@/lib/context/PipelineContext'
import { UploadResponseSchema } from '@/types/api'

export function useUpload() {
  const queryClient = useQueryClient()
  const { setCurrentImage } = useImage()
  const { markStepComplete, updateStep, setIsProcessing, setProcessingStatus, setError } = usePipeline()

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      setIsProcessing(true)
      setProcessingStatus('Uploading infrared thermal image...')
      setError(null)

      const uploadResponse = await uploadService.uploadImage(file)

      // Automatically create a processing session for this upload
      setProcessingStatus('Creating mission processing session...')
      try {
        await sessionService.createSession(uploadResponse.upload_id)
      } catch (e) {
        console.warn('Notice: Session creation skipped or handled resiliently', e)
      }

      return uploadResponse
    },
    onSuccess: (data: UploadResponseSchema) => {
      setCurrentImage({
        upload_id: data.upload_id,
        filename: data.filename,
        file_path: data.file_path,
        resolution: '4K THERMAL',
        channels: 1,
        format: data.file_type,
        original_image: data.file_path,
      })

      markStepComplete('upload')
      updateStep('preprocessing')
      setIsProcessing(false)
      setProcessingStatus('')
      toast.success(`Infrared image ${data.filename} uploaded successfully`)
      queryClient.invalidateQueries({ queryKey: ['dashboard'] })
      queryClient.invalidateQueries({ queryKey: ['sessions'] })
    },
    onError: (error: any) => {
      setIsProcessing(false)
      const msg = error.response?.data?.detail || error.message || 'Image upload failed'
      setError(msg)
      toast.error(`Upload Failed: ${msg}`)
    },
  })

  return {
    upload: uploadMutation.mutate,
    uploadAsync: uploadMutation.mutateAsync,
    isUploading: uploadMutation.isPending,
    error: uploadMutation.error,
    data: uploadMutation.data,
  }
}
