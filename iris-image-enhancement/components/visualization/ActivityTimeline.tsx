'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { GlassCard } from '@/components/ui/GlassCard'
import { Badge } from '@/components/ui/Badge'
import { CheckCircle2, Clock, AlertCircle, Zap } from 'lucide-react'

interface TimelineItem {
  id: string
  type: 'upload' | 'processing' | 'complete' | 'error' | 'analysis'
  title: string
  description: string
  timestamp: Date
  status: 'pending' | 'in-progress' | 'complete' | 'error'
  metadata?: Record<string, any>
}

interface ActivityTimelineProps {
  items?: TimelineItem[]
  compact?: boolean
}

export function ActivityTimeline({ items = [], compact = false }: ActivityTimelineProps) {
  const getIcon = (type: string) => {
    switch (type) {
      case 'upload':
        return '📤'
      case 'processing':
        return '⚙️'
      case 'complete':
        return '✓'
      case 'analysis':
        return '🧠'
      case 'error':
        return '⚠️'
      default:
        return '•'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'complete':
        return 'success'
      case 'in-progress':
        return 'info'
      case 'pending':
        return 'warning'
      case 'error':
        return 'error'
      default:
        return 'info'
    }
  }

  const getStatusLabel = (status: string) => {
    return status.charAt(0).toUpperCase() + status.slice(1).replace('-', ' ')
  }

  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    }).format(date)
  }

  if (items.length === 0) {
    return (
      <GlassCard compact={compact}>
        <div className={compact ? 'p-4' : 'p-6'}>
          <p className="text-center text-sm text-muted-foreground">No activity yet</p>
        </div>
      </GlassCard>
    )
  }

  return (
    <GlassCard compact={compact}>
      <div className={compact ? 'p-4' : 'p-6'}>
        <h3 className="text-sm font-semibold text-foreground mb-4">Recent Activity</h3>

        <div className="space-y-3 max-h-96 overflow-y-auto scrollbar-hide">
          {items.map((item, idx) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.05 }}
              className="flex gap-3 pb-3 border-b border-border/50 last:border-b-0 last:pb-0"
            >
              {/* Timeline icon */}
              <div className="flex-shrink-0 flex items-start pt-0.5">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-lg ${
                  item.status === 'complete'
                    ? 'bg-green-500/20'
                    : item.status === 'error'
                      ? 'bg-red-500/20'
                      : item.status === 'in-progress'
                        ? 'bg-primary/20'
                        : 'bg-muted'
                }`}>
                  {getIcon(item.type)}
                </div>
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <h4 className="text-sm font-medium text-foreground truncate">{item.title}</h4>
                  <Badge variant={getStatusColor(item.status) as any} size="sm" className="flex-shrink-0">
                    {getStatusLabel(item.status)}
                  </Badge>
                </div>

                {item.description && (
                  <p className="text-xs text-muted-foreground mt-0.5 line-clamp-2">{item.description}</p>
                )}

                <p className="text-xs text-muted-foreground/60 mt-1">{formatTime(item.timestamp)}</p>

                {/* Metadata */}
                {item.metadata && Object.keys(item.metadata).length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {Object.entries(item.metadata).map(([key, value]) => (
                      <span key={key} className="text-xs bg-background/50 rounded px-1.5 py-0.5">
                        {key}: {String(value)}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </GlassCard>
  )
}
