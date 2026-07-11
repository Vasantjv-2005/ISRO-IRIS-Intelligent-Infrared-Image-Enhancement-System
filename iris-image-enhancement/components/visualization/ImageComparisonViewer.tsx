'use client'

import React, { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { GlassCard } from '@/components/ui/GlassCard'

interface ImageComparisonViewerProps {
  beforeImage?: string
  afterImage?: string
  beforeLabel?: string
  afterLabel?: string
  showComparison?: boolean
}

export function ImageComparisonViewer({
  beforeImage,
  afterImage,
  beforeLabel = 'Original',
  afterLabel = 'Processed',
  showComparison = true,
}: ImageComparisonViewerProps) {
  const [sliderPosition, setSliderPosition] = useState(50)
  const [isDragging, setIsDragging] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)

  const handleMouseDown = () => setIsDragging(true)
  const handleMouseUp = () => setIsDragging(false)

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging || !containerRef.current) return

      const rect = containerRef.current.getBoundingClientRect()
      const newPosition = ((e.clientX - rect.left) / rect.width) * 100
      setSliderPosition(Math.max(0, Math.min(100, newPosition)))
    }

    window.addEventListener('mousemove', handleMouseMove)
    window.addEventListener('mouseup', handleMouseUp)

    return () => {
      window.removeEventListener('mousemove', handleMouseMove)
      window.removeEventListener('mouseup', handleMouseUp)
    }
  }, [isDragging])

  if (!beforeImage && !afterImage) {
    return (
      <GlassCard className="flex items-center justify-center aspect-video">
        <div className="text-center">
          <p className="text-muted-foreground">Upload an image to begin</p>
        </div>
      </GlassCard>
    )
  }

  if (!showComparison || !afterImage) {
    return (
      <GlassCard className="overflow-hidden">
        <div className="relative aspect-video bg-background">
          {beforeImage && (
            <img src={beforeImage} alt={beforeLabel} className="w-full h-full object-cover" crossOrigin="anonymous" />
          )}
          <div className="absolute bottom-4 left-4">
            <div className="px-3 py-1.5 rounded-lg bg-background/80 backdrop-blur-sm border border-border">
              <p className="text-xs font-medium text-foreground">{beforeLabel}</p>
            </div>
          </div>
        </div>
      </GlassCard>
    )
  }

  return (
    <GlassCard className="overflow-hidden">
      <div
        ref={containerRef}
        className="relative aspect-video bg-background cursor-col-resize group"
        onMouseDown={handleMouseDown}
        onTouchStart={handleMouseDown}
      >
        {/* After Image (Background) */}
        <div className="absolute inset-0">
          {afterImage && (
            <img src={afterImage} alt={afterLabel} className="w-full h-full object-cover" crossOrigin="anonymous" />
          )}
          <div className="absolute bottom-4 right-4">
            <div className="px-3 py-1.5 rounded-lg bg-background/80 backdrop-blur-sm border border-border">
              <p className="text-xs font-medium text-foreground">{afterLabel}</p>
            </div>
          </div>
        </div>

        {/* Before Image (Clipped) */}
        <div className="absolute inset-0 overflow-hidden" style={{ width: `${sliderPosition}%` }}>
          {beforeImage && (
            <img src={beforeImage} alt={beforeLabel} className="w-screen h-full object-cover" crossOrigin="anonymous" />
          )}
          <div className="absolute bottom-4 left-4">
            <div className="px-3 py-1.5 rounded-lg bg-background/80 backdrop-blur-sm border border-border">
              <p className="text-xs font-medium text-foreground">{beforeLabel}</p>
            </div>
          </div>
        </div>

        {/* Slider Divider */}
        <motion.div
          className="absolute top-0 bottom-0 w-1 bg-gradient-to-b from-transparent via-primary to-transparent group-hover:w-2 transition-all"
          style={{ left: `${sliderPosition}%`, x: '-50%' }}
          animate={{ boxShadow: `0 0 20px rgba(0, 240, 255, ${isDragging ? 0.8 : 0.4})` }}
        >
          {/* Handle */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-10 h-10 bg-primary rounded-full flex items-center justify-center shadow-lg border-2 border-background">
            <div className="flex gap-1">
              <div className="w-0.5 h-4 bg-background rounded-full" />
              <div className="w-0.5 h-4 bg-background rounded-full" />
            </div>
          </div>
        </motion.div>
      </div>
    </GlassCard>
  )
}
