'use client'

import React, { createContext, useContext, useState } from 'react'

export interface ImageData {
  upload_id?: string
  filename?: string
  file_path?: string
  resolution?: string
  channels?: number
  format?: string
  original_image?: string
  processed_image?: string
  detections?: any[]
  analysis?: string
  metrics?: {
    psnr?: number
    ssim?: number
    processing_time?: number
  }
}

interface ImageContextType {
  currentImage: ImageData | null
  setCurrentImage: (image: ImageData) => void
  clearCurrentImage: () => void
  updateImageMetrics: (metrics: any) => void
  updateProcessedImage: (path: string) => void
}

const ImageContext = createContext<ImageContextType | undefined>(undefined)

export function ImageProvider({ children }: { children: React.ReactNode }) {
  const [currentImage, setCurrentImageState] = useState<ImageData | null>(null)

  const setCurrentImage = (image: ImageData) => {
    setCurrentImageState(image)
  }

  const clearCurrentImage = () => {
    setCurrentImageState(null)
  }

  const updateImageMetrics = (metrics: any) => {
    if (currentImage) {
      setCurrentImageState({
        ...currentImage,
        metrics: { ...currentImage.metrics, ...metrics },
      })
    }
  }

  const updateProcessedImage = (path: string) => {
    if (currentImage) {
      setCurrentImageState({
        ...currentImage,
        processed_image: path,
      })
    }
  }

  return (
    <ImageContext.Provider
      value={{
        currentImage,
        setCurrentImage,
        clearCurrentImage,
        updateImageMetrics,
        updateProcessedImage,
      }}
    >
      {children}
    </ImageContext.Provider>
  )
}

export function useImage() {
  const context = useContext(ImageContext)
  if (context === undefined) {
    throw new Error('useImage must be used within ImageProvider')
  }
  return context
}
