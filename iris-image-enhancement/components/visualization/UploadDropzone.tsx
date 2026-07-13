'use client'

import React, { useState, useRef } from 'react'
import { motion } from 'framer-motion'
import { Upload, CheckCircle, AlertCircle } from 'lucide-react'
import { uploadAPI } from '@/lib/api'
import { useImage } from '@/lib/context/ImageContext'
import { usePipeline } from '@/lib/context/PipelineContext'
import { GlassCard } from '@/components/ui/GlassCard'
import { Spinner } from '@/components/ui/Spinner'

interface UploadDropzoneProps {
  onComplete?: (uploadId: string) => void
}

import { useUpload } from '@/hooks'

export function UploadDropzone({ onComplete }: UploadDropzoneProps) {
  const [isDragActive, setIsDragActive] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [errorMessage, setErrorMessage] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)
  const { uploadAsync, isUploading } = useUpload()

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragActive(true)
    } else if (e.type === 'dragleave') {
      setIsDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragActive(false)
    const files = e.dataTransfer.files
    if (files && files[0]) {
      processFile(files[0])
    }
  }

  const processFile = async (file: File) => {
    // Validate file type & size
    const validTypes = ['image/png', 'image/jpeg', 'image/tiff', 'image/jpg']
    if (!validTypes.includes(file.type)) {
      setErrorMessage('Please upload a PNG, JPEG, or TIFF image')
      setUploadStatus('error')
      return
    }
    if (file.size > 50 * 1024 * 1024) {
      setErrorMessage('File size exceeds 50MB limit')
      setUploadStatus('error')
      return
    }

    setUploadStatus('idle')
    setErrorMessage('')

    try {
      const response = await uploadAsync(file)
      setUploadStatus('success')
      if (onComplete && response?.upload_id) {
        onComplete(response.upload_id)
      }
    } catch (error: any) {
      setErrorMessage(error.response?.data?.detail || error.message || 'Upload failed')
      setUploadStatus('error')
    }
  }

  return (
    <GlassCard>
      <motion.div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        animate={{ scale: isDragActive ? 1.02 : 1 }}
        className={`relative p-8 rounded-xl border-2 border-dashed transition-all cursor-pointer ${
          isDragActive
            ? 'border-primary bg-primary/5'
            : uploadStatus === 'success'
              ? 'border-secondary bg-secondary/5'
              : uploadStatus === 'error'
                ? 'border-destructive bg-destructive/5'
                : 'border-border hover:border-primary/50 hover:bg-primary/5'
        }`}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/png,image/jpeg,image/tiff"
          onChange={(e) => e.target.files && processFile(e.target.files[0])}
          className="hidden"
        />

        <div className="flex flex-col items-center gap-4">
          {isUploading ? (
            <>
              <Spinner size="lg" variant="orbital" />
              <p className="text-sm text-muted-foreground">Processing thermal image...</p>
            </>
          ) : uploadStatus === 'success' ? (
            <>
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', stiffness: 200 }}
              >
                <CheckCircle className="w-12 h-12 text-secondary" />
              </motion.div>
              <div className="text-center">
                <p className="text-sm font-medium text-secondary">Upload successful!</p>
                <p className="text-xs text-muted-foreground">Ready for processing</p>
              </div>
            </>
          ) : uploadStatus === 'error' ? (
            <>
              <AlertCircle className="w-12 h-12 text-destructive" />
              <div className="text-center">
                <p className="text-sm font-medium text-destructive">Upload failed</p>
                <p className="text-xs text-muted-foreground">{errorMessage}</p>
              </div>
            </>
          ) : (
            <>
              <motion.div animate={{ y: [0, -8, 0] }} transition={{ duration: 2, repeat: Infinity }}>
                <Upload className="w-12 h-12 text-primary" />
              </motion.div>
              <div className="text-center">
                <p className="text-sm font-medium text-foreground">Drag thermal image here</p>
                <p className="text-xs text-muted-foreground">or click to browse (PNG, JPEG, TIFF)</p>
              </div>
            </>
          )}
        </div>
      </motion.div>
    </GlassCard>
  )
}
