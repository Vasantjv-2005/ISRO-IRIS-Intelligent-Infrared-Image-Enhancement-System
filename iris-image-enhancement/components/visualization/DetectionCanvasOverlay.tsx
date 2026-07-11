'use client'

import React, { useEffect, useRef, useState } from 'react'
import { GlassCard } from '@/components/ui/GlassCard'

interface Detection {
  id: string
  class: string
  confidence: number
  x: number
  y: number
  width: number
  height: number
}

interface DetectionCanvasOverlayProps {
  imageUrl?: string
  detections?: Detection[]
  confidenceThreshold?: number
  onDetectionHover?: (detection: Detection | null) => void
  interactive?: boolean
}

const classColors: Record<string, string> = {
  vehicle: '#ff6b00',
  vessel: '#ffb800',
  'thermal-anomaly': '#e01e79',
  structure: '#00f0ff',
  person: '#00d2b4',
  aircraft: '#ff6b00',
}

export function DetectionCanvasOverlay({
  imageUrl,
  detections = [],
  confidenceThreshold = 0.5,
  onDetectionHover,
  interactive = true,
}: DetectionCanvasOverlayProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const [hoveredId, setHoveredId] = useState<string | null>(null)

  useEffect(() => {
    if (!canvasRef.current || !imageUrl) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const img = new Image()
    img.crossOrigin = 'anonymous'

    img.onload = () => {
      canvas.width = img.width
      canvas.height = img.height

      // Draw image
      ctx.drawImage(img, 0, 0)

      // Draw bounding boxes
      const filteredDetections = detections.filter((d) => d.confidence >= confidenceThreshold)

      filteredDetections.forEach((detection) => {
        const color = classColors[detection.class.toLowerCase()] || '#00f0ff'
        const isHovered = hoveredId === detection.id
        const lineWidth = isHovered ? 3 : 2
        const opacity = isHovered ? 1 : 0.7

        // Draw box
        ctx.strokeStyle = color
        ctx.lineWidth = lineWidth
        ctx.globalAlpha = opacity
        ctx.strokeRect(detection.x, detection.y, detection.width, detection.height)

        // Draw glow effect
        ctx.shadowColor = color
        ctx.shadowBlur = isHovered ? 15 : 8
        ctx.shadowOffsetX = 0
        ctx.shadowOffsetY = 0
        ctx.strokeRect(detection.x, detection.y, detection.width, detection.height)

        // Reset shadow
        ctx.shadowBlur = 0
        ctx.globalAlpha = 1

        // Draw label background
        const labelText = `${detection.class.toUpperCase()} ${(detection.confidence * 100).toFixed(0)}%`
        ctx.font = 'bold 12px monospace'
        const metrics = ctx.measureText(labelText)
        const labelHeight = 20
        const labelX = detection.x
        const labelY = detection.y - labelHeight - 4

        ctx.fillStyle = `${color}40`
        ctx.fillRect(labelX, labelY, metrics.width + 8, labelHeight)

        // Draw label text
        ctx.fillStyle = color
        ctx.fillText(labelText, labelX + 4, labelY + 14)
      })
    }

    img.src = imageUrl
  }, [imageUrl, detections, confidenceThreshold, hoveredId])

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!interactive || !containerRef.current) return

    const rect = containerRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    const scale = canvasRef.current?.width! / rect.width

    const filteredDetections = detections.filter((d) => d.confidence >= confidenceThreshold)
    let found = false

    for (const detection of filteredDetections) {
      if (
        x * scale >= detection.x &&
        x * scale <= detection.x + detection.width &&
        y * scale >= detection.y &&
        y * scale <= detection.y + detection.height
      ) {
        setHoveredId(detection.id)
        onDetectionHover?.(detection)
        found = true
        break
      }
    }

    if (!found) {
      setHoveredId(null)
      onDetectionHover?.(null)
    }
  }

  if (!imageUrl) {
    return (
      <GlassCard className="flex items-center justify-center aspect-video">
        <p className="text-muted-foreground">No image to display</p>
      </GlassCard>
    )
  }

  return (
    <GlassCard className="overflow-hidden">
      <div ref={containerRef} className="relative inline-block w-full" onMouseMove={handleMouseMove}>
        <canvas
          ref={canvasRef}
          className={`w-full block ${interactive ? 'cursor-crosshair' : ''}`}
          crossOrigin="anonymous"
        />
      </div>
    </GlassCard>
  )
}
