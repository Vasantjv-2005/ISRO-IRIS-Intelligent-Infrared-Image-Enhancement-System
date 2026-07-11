'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { GlassCard } from '@/components/ui/GlassCard'

interface MetricsGaugeProps {
  label: string
  value: number | string
  unit?: string
  max?: number
  variant?: 'primary' | 'secondary' | 'accent' | 'warning'
  format?: 'number' | 'percentage' | 'time'
  icon?: React.ReactNode
}

export function MetricsGauge({
  label,
  value,
  unit = '',
  max = 100,
  variant = 'primary',
  format = 'number',
  icon,
}: MetricsGaugeProps) {
  const numericValue = typeof value === 'number' ? value : 0
  const percentage = Math.min((numericValue / max) * 100, 100)

  const variantColors = {
    primary: { bg: 'bg-primary/20', bar: 'from-primary to-secondary', text: 'text-primary' },
    secondary: { bg: 'bg-secondary/20', bar: 'from-secondary to-primary', text: 'text-secondary' },
    accent: { bg: 'bg-accent/20', bar: 'from-accent to-primary', text: 'text-accent' },
    warning: { bg: 'bg-yellow-500/20', bar: 'from-yellow-500 to-orange-500', text: 'text-yellow-400' },
  }

  const colors = variantColors[variant]

  const formatValue = () => {
    if (typeof value === 'string') return value
    if (format === 'percentage') return `${(numericValue * 100).toFixed(1)}%`
    if (format === 'time') return `${numericValue.toFixed(0)}ms`
    return numericValue.toFixed(2)
  }

  return (
    <GlassCard compact>
      <div className="p-4 space-y-3">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {icon && <span className="text-lg">{icon}</span>}
            <p className="text-xs font-medium text-muted-foreground">{label}</p>
          </div>
        </div>

        {/* Value */}
        <div className="space-y-1">
          <motion.div
            className={`text-2xl font-bold ${colors.text}`}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5, type: 'spring' }}
          >
            {formatValue()}
          </motion.div>
          {unit && <p className="text-xs text-muted-foreground">{unit}</p>}
        </div>

        {/* Progress bar */}
        <div className={`h-1.5 rounded-full ${colors.bg} overflow-hidden`}>
          <motion.div
            className={`h-full bg-gradient-to-r ${colors.bar} rounded-full shadow-lg`}
            initial={{ width: 0 }}
            animate={{ width: `${percentage}%` }}
            transition={{ duration: 1, ease: 'easeOut' }}
          />
        </div>
      </div>
    </GlassCard>
  )
}
