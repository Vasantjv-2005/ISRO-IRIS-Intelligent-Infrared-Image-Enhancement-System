'use client'

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Brain, Copy, Check, Zap } from 'lucide-react'
import { GlassCard } from '@/components/ui/GlassCard'
import { Badge } from '@/components/ui/Badge'
import { Spinner } from '@/components/ui/Spinner'

interface GeminiAnalysisCardProps {
  analysis?: string
  isLoading?: boolean
  error?: string | null
  onRetry?: () => void
}

export function GeminiAnalysisCard({ analysis, isLoading = false, error, onRetry }: GeminiAnalysisCardProps) {
  const [displayedText, setDisplayedText] = useState('')
  const [copied, setCopied] = useState(false)

  // Typewriter effect
  useEffect(() => {
    if (!analysis || isLoading) {
      setDisplayedText('')
      return
    }

    let index = 0
    const interval = setInterval(() => {
      if (index < analysis.length) {
        setDisplayedText(analysis.substring(0, index + 1))
        index++
      } else {
        clearInterval(interval)
      }
    }, 15)

    return () => clearInterval(interval)
  }, [analysis, isLoading])

  const handleCopy = () => {
    if (analysis) {
      navigator.clipboard.writeText(analysis)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <GlassCard>
      <div className="p-6 space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <motion.div animate={{ rotate: [0, 360] }} transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}>
              <Brain className="w-5 h-5 text-primary" />
            </motion.div>
            <div>
              <h3 className="font-semibold text-foreground">Gemini Intelligence</h3>
              <p className="text-xs text-muted-foreground">AI Scene Analysis & Interpretation</p>
            </div>
          </div>

          {/* Action buttons */}
          {analysis && (
            <motion.button
              onClick={handleCopy}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 rounded-lg hover:bg-primary/10 transition-all"
              title="Copy analysis"
            >
              {copied ? (
                <Check className="w-4 h-4 text-secondary" />
              ) : (
                <Copy className="w-4 h-4 text-muted-foreground hover:text-primary" />
              )}
            </motion.button>
          )}
        </div>

        {/* Content */}
        <div className="min-h-[120px]">
          {isLoading ? (
            <div className="flex flex-col items-center justify-center gap-3 py-8">
              <Spinner size="md" variant="orbital" />
              <p className="text-sm text-muted-foreground">Analyzing thermal data...</p>
            </div>
          ) : error ? (
            <div className="space-y-3">
              <p className="text-sm text-destructive">{error}</p>
              {onRetry && (
                <button
                  onClick={onRetry}
                  className="px-3 py-1.5 rounded-lg bg-destructive/10 text-destructive text-sm font-medium hover:bg-destructive/20 transition-all"
                >
                  Retry
                </button>
              )}
            </div>
          ) : analysis ? (
            <div className="space-y-3">
              <p className="text-sm text-foreground leading-relaxed whitespace-pre-wrap">{displayedText}</p>

              {/* Analysis badges */}
              <div className="flex flex-wrap gap-2 pt-3 border-t border-border">
                <Badge variant="info" size="sm">
                  <Zap className="w-3 h-3" />
                  High Confidence
                </Badge>
                <Badge variant="success" size="sm">
                  Scene Detected
                </Badge>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center gap-2 text-center py-6">
              <Brain className="w-8 h-8 text-muted-foreground/30" />
              <p className="text-sm text-muted-foreground">Run analysis to see insights</p>
            </div>
          )}
        </div>
      </div>
    </GlassCard>
  )
}
