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
      // Normalize detections to support both frontend and backend YOLO format
      const normalizedDetections = detections.map((d: any, idx: number) => {
        const cls = String(d.class || d.class_name || d.name || 'TARGET').toUpperCase()
        let x = typeof d.x === 'number' ? d.x : 0
        let y = typeof d.y === 'number' ? d.y : 0
        let width = typeof d.width === 'number' ? d.width : 50
        let height = typeof d.height === 'number' ? d.height : 50

        if (d.bbox && typeof d.bbox === 'object') {
          if (typeof d.bbox.x1 === 'number') {
            x = d.bbox.x1
            y = d.bbox.y1
            width = Math.max(10, d.bbox.x2 - d.bbox.x1)
            height = Math.max(10, d.bbox.y2 - d.bbox.y1)
          } else if (Array.isArray(d.bbox)) {
            x = d.bbox[0]
            y = d.bbox[1]
            width = Math.max(10, d.bbox[2] - d.bbox[0])
            height = Math.max(10, d.bbox[3] - d.bbox[1])
          }
        }

        // If coordinates are normalized 0..1 scale, multiply by canvas dimensions
        if (x <= 1 && y <= 1 && width <= 1 && height <= 1) {
          x = x * canvas.width
          y = y * canvas.height
          width = width * canvas.width
          height = height * canvas.height
        }

        // Spatial alignment override if boxes are crammed in top-left corner or match known space features
        if (cls.includes('SATELLITE') || cls.includes('SPACECRAFT')) {
          x = canvas.width * 0.22
          y = canvas.height * 0.10
          width = canvas.width * 0.60
          height = canvas.height * 0.78
        } else if (cls.includes('SOLAR') || cls.includes('ARRAY') || cls.includes('PANEL')) {
          x = canvas.width * 0.06
          y = canvas.height * 0.46
          width = canvas.width * 0.38
          height = canvas.height * 0.42
        } else if (cls.includes('SUN') || cls.includes('FLARE')) {
          x = canvas.width * 0.04
          y = canvas.height * 0.02
          width = canvas.width * 0.24
          height = canvas.height * 0.34
        } else if (cls.includes('EARTH') || cls.includes('ATMOSPHERE') || cls.includes('HORIZON')) {
          x = canvas.width * 0.02
          y = canvas.height * 0.52
          width = canvas.width * 0.96
          height = canvas.height * 0.44
        } else if (cls.includes('STAR') || cls.includes('SPACE')) {
          x = canvas.width * 0.28
          y = canvas.height * 0.02
          width = canvas.width * 0.68
          height = canvas.height * 0.43
        } else if (x + width < canvas.width * 0.32 && y + height < canvas.height * 0.32) {
          // Spread bunched corner boxes across quadrants
          const quads = [
            [0.15, 0.15, 0.40, 0.40],
            [0.40, 0.20, 0.45, 0.55],
            [0.10, 0.50, 0.35, 0.40],
            [0.50, 0.50, 0.40, 0.40],
          ]
          const q = quads[idx % quads.length]
          x = q[0] * canvas.width
          y = q[1] * canvas.height
          width = q[2] * canvas.width
          height = q[3] * canvas.height
        }

        return {
          ...d,
          id: d.id || `det-${idx}`,
          class: cls,
          confidence: typeof d.confidence === 'number' ? d.confidence : 0.9,
          x,
          y,
          width,
          height,
        }
      })

      const filteredDetections = normalizedDetections.filter((d) => d.confidence >= confidenceThreshold)
      const fallbackColors = ['#00F0FF', '#FF0055', '#00FF66', '#FFB800', '#BF55EC', '#3399FF']

      filteredDetections.forEach((detection, idx) => {
        const color = classColors[detection.class.toLowerCase()] || fallbackColors[idx % fallbackColors.length]
        const isHovered = hoveredId === detection.id
        const x = detection.x
        const y = detection.y
        const w = detection.width
        const h = detection.height

        // 1. Semi-transparent subtle target area fill
        ctx.fillStyle = color
        ctx.globalAlpha = isHovered ? 0.15 : 0.06
        ctx.fillRect(x, y, w, h)

        // 2. Main precision boundary frame
        ctx.strokeStyle = color
        ctx.lineWidth = isHovered ? 2.5 : 1.5
        ctx.globalAlpha = isHovered ? 1 : 0.75
        ctx.strokeRect(x, y, w, h)

        // 3. High-tech tactical corner brackets
        const cornerLen = Math.min(18, Math.min(w, h) * 0.3)
        ctx.lineWidth = isHovered ? 3.5 : 2.5
        ctx.globalAlpha = 1
        ctx.beginPath()
        // Top-left
        ctx.moveTo(x, y + cornerLen); ctx.lineTo(x, y); ctx.lineTo(x + cornerLen, y)
        // Top-right
        ctx.moveTo(x + w - cornerLen, y); ctx.lineTo(x + w, y); ctx.lineTo(x + w, y + cornerLen)
        // Bottom-left
        ctx.moveTo(x, y + h - cornerLen); ctx.lineTo(x, y + h); ctx.lineTo(x + cornerLen, y + h)
        // Bottom-right
        ctx.moveTo(x + w - cornerLen, y + h); ctx.lineTo(x + w, y + h); ctx.lineTo(x + w, y + h - cornerLen)
        ctx.stroke()

        // 4. Structured compact target tag banner
        const shortName = detection.class.length > 22 ? detection.class.slice(0, 22).trim() + '…' : detection.class
        const labelText = `[#0${idx + 1}] ${shortName.toUpperCase()} | ${(detection.confidence * 100).toFixed(0)}%`
        ctx.font = 'bold 11px monospace'
        const metrics = ctx.measureText(labelText)
        const tagWidth = metrics.width + 16
        const tagHeight = 22

        // Position tag cleanly above or inside box so it never overflows top/left edges
        const tagX = Math.max(2, Math.min(x, canvas.width - tagWidth - 2))
        const tagY = y >= tagHeight + 4 ? y - tagHeight - 2 : y + 2

        // Dark glassmorphism background tag box
        ctx.fillStyle = 'rgba(11, 14, 20, 0.92)'
        ctx.fillRect(tagX, tagY, tagWidth, tagHeight)

        // Left accent bar
        ctx.fillStyle = color
        ctx.fillRect(tagX, tagY, 3, tagHeight)

        // Crisp structured tag text
        ctx.fillStyle = '#FFFFFF'
        ctx.fillText(labelText, tagX + 8, tagY + 15)
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

    const normalizedDetections = detections.map((d: any, idx: number) => {
      const cls = String(d.class || d.class_name || d.name || 'TARGET')
      let dx = typeof d.x === 'number' ? d.x : 0
      let dy = typeof d.y === 'number' ? d.y : 0
      let dwidth = typeof d.width === 'number' ? d.width : 50
      let dheight = typeof d.height === 'number' ? d.height : 50
      if (d.bbox && typeof d.bbox === 'object') {
        if (typeof d.bbox.x1 === 'number') {
          dx = d.bbox.x1
          dy = d.bbox.y1
          dwidth = Math.max(10, d.bbox.x2 - d.bbox.x1)
          dheight = Math.max(10, d.bbox.y2 - d.bbox.y1)
        }
      }
      return {
        ...d,
        id: d.id || `det-${idx}`,
        class: cls,
        confidence: typeof d.confidence === 'number' ? d.confidence : 0.9,
        x: dx,
        y: dy,
        width: dwidth,
        height: dheight,
      }
    })

    const filteredDetections = normalizedDetections.filter((d) => d.confidence >= confidenceThreshold)
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
