import React from 'react'

interface GlassCardProps {
  children: React.ReactNode
  className?: string
  compact?: boolean
  hover?: boolean
}

export function GlassCard({ children, className = '', compact = false, hover = true }: GlassCardProps) {
  const baseClass = compact ? 'glass-card-sm' : 'glass-card'
  const hoverClass = hover ? '' : 'hover:shadow-none hover:border-border'

  return <div className={`${baseClass} ${hoverClass} ${className}`}>{children}</div>
}
