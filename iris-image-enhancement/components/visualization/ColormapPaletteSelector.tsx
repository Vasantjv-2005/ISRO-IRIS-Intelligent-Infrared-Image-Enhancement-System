'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Check } from 'lucide-react'
import { GlassCard } from '@/components/ui/GlassCard'

interface Colormap {
  name: string
  id: string
  gradient: string
  description: string
}

const colormaps: Colormap[] = [
  {
    name: 'Inferno',
    id: 'inferno',
    gradient: 'linear-gradient(90deg, #000004, #420a68, #932667, #fca636)',
    description: 'Hot to cold thermal',
  },
  {
    name: 'Magma',
    id: 'magma',
    gradient: 'linear-gradient(90deg, #000004, #3b0f70, #8c2981, #fcfdbf)',
    description: 'Perceptually uniform',
  },
  {
    name: 'Plasma',
    id: 'plasma',
    gradient: 'linear-gradient(90deg, #0d0887, #7e03a8, #cc4778, #f89540)',
    description: 'High contrast spectrum',
  },
  {
    name: 'Viridis',
    id: 'viridis',
    gradient: 'linear-gradient(90deg, #440154, #31688e, #35b779, #fde724)',
    description: 'Perceptually optimal',
  },
  {
    name: 'Jet',
    id: 'jet',
    gradient: 'linear-gradient(90deg, #0000ff, #00ffff, #ffff00, #ff0000)',
    description: 'Classic thermal map',
  },
  {
    name: 'Rainbow',
    id: 'rainbow',
    gradient: 'linear-gradient(90deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff)',
    description: 'Full spectrum colors',
  },
]

interface ColormapPaletteSelectorProps {
  selectedColormap?: string
  onSelect?: (colormapId: string) => void
  compact?: boolean
}

export function ColormapPaletteSelector({
  selectedColormap = 'inferno',
  onSelect,
  compact = false,
}: ColormapPaletteSelectorProps) {
  return (
    <GlassCard>
      <div className={compact ? 'p-4' : 'p-6'}>
        <h3 className="text-sm font-semibold text-foreground mb-4">Thermal Color Palette</h3>

        <div className={`grid gap-3 ${compact ? 'grid-cols-3 md:grid-cols-6' : 'grid-cols-2 md:grid-cols-3'}`}>
          {colormaps.map((colormap) => (
            <motion.button
              key={colormap.id}
              onClick={() => onSelect?.(colormap.id)}
              className={`relative group transition-all ${compact ? 'rounded-lg overflow-hidden' : 'rounded-xl overflow-hidden'}`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {/* Gradient preview */}
              <div
                className={`${compact ? 'h-8' : 'h-12'} rounded-lg border-2 transition-all ${
                  selectedColormap === colormap.id ? 'border-primary shadow-[0_0_15px_rgba(0,240,255,0.5)]' : 'border-border'
                }`}
                style={{ backgroundImage: colormap.gradient }}
              />

              {/* Selected checkmark */}
              {selectedColormap === colormap.id && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute inset-0 flex items-center justify-center bg-background/40 backdrop-blur-sm"
                >
                  <Check className="w-5 h-5 text-primary" />
                </motion.div>
              )}

              {/* Label and description */}
              {!compact && (
                <div className="absolute inset-0 flex flex-col items-center justify-center bg-background/80 backdrop-blur-md opacity-0 group-hover:opacity-100 transition-opacity rounded-xl">
                  <p className="text-xs font-bold text-foreground">{colormap.name}</p>
                  <p className="text-xs text-muted-foreground">{colormap.description}</p>
                </div>
              )}

              {/* Tooltip for compact mode */}
              {compact && (
                <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 px-2 py-1 rounded-md bg-background/90 border border-border text-xs text-foreground whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                  {colormap.name}
                </div>
              )}
            </motion.button>
          ))}
        </div>
      </div>
    </GlassCard>
  )
}
