'use client'

import React, { useRef, useState } from 'react'
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

export function DetectionCanvasOverlay({
  imageUrl,
  detections = [],
  confidenceThreshold = 0.5,
  onDetectionHover,
  interactive = true,
}: DetectionCanvasOverlayProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [hoveredId, setHoveredId] = useState<string | null>(null)

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!interactive || !containerRef.current || !onDetectionHover) return

    const rect = containerRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    // Normalize coordinates 0..1 relative to container dimensions
    const nx = x / maxDivWidth(rect.width)
    const ny = y / maxDivWidth(rect.height)

    let found = false
    for (const d of detections) {
      if (d.confidence < confidenceThreshold) continue

      let bx = d.x
      let by = d.y
      let bw = d.width
      let bh = d.height

      // If coordinates are normalized 0..1 scale
      if (bx <= 1 && by <= 1 && bw <= 1 && bh <= 1) {
        if (nx >= bx && nx <= bx + bw && ny >= by && ny <= by + bh) {
          setHoveredId(d.id)
          onDetectionHover(d)
          found = true
          break
        }
      }
    }

    if (!found && hoveredId !== null) {
      setHoveredId(null)
      onDetectionHover(null)
    }
  }

  function maxDivWidth(val: number): number {
    return val > 0 ? val : 1
  }

  if (!imageUrl) {
    return (
      <GlassCard className="flex items-center justify-center aspect-video">
        <p className="text-muted-foreground">No detection image to display</p>
      </GlassCard>
    )
  }

  return (
    <GlassCard className="overflow-hidden">
      <div
        ref={containerRef}
        className="relative inline-block w-full"
        onMouseMove={handleMouseMove}
      >
        {/* Pixel-identical backend OpenCV detection image — zero frontend redraw or modifications */}
        <img
          src={imageUrl}
          alt="AI Detection Output"
          className="w-full h-auto block object-contain select-none"
        />
      </div>
    </GlassCard>
  )
}
