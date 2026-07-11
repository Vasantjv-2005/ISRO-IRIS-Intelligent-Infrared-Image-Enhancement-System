'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Zap, BarChart3 } from 'lucide-react'
import { AuthProvider } from '@/lib/context/AuthContext'
import { ImageProvider } from '@/lib/context/ImageContext'
import { PipelineProvider } from '@/lib/context/PipelineContext'
import { Header } from '@/components/layout/Header'
import { PipelinePanel } from '@/components/layout/PipelinePanel'
import { ImageComparisonViewer } from '@/components/visualization/ImageComparisonViewer'
import { GeminiAnalysisCard } from '@/components/visualization/GeminiAnalysisCard'
import { MetricsGauge } from '@/components/visualization/MetricsGauge'
import { GlassCard } from '@/components/ui/GlassCard'

function IRISCommandCenter() {
  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="pt-20 pb-12">
        <div className="container mx-auto px-4">
          {/* Hero Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-8 text-center"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
              Thermal Imaging Command Center
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Advanced AI-powered infrared image enhancement, object detection, and scene analysis
            </p>
          </motion.div>

          {/* Main Grid Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left Panel - Controls */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="lg:col-span-3"
            >
              <div className="sticky top-24">
                <PipelinePanel />
              </div>
            </motion.div>

            {/* Right Panel - Visualization */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.15 }}
              className="lg:col-span-9 space-y-6"
            >
              {/* Image Comparison */}
              <div>
                <motion.h3
                  className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.25 }}
                >
                  <span className="w-1 h-4 bg-gradient-to-b from-primary to-secondary rounded-full" />
                  Interactive Comparison
                </motion.h3>
                <ImageComparisonViewer
                  beforeLabel="Original Thermal"
                  afterLabel="AI Enhanced"
                  showComparison={true}
                />
              </div>

              {/* Metrics & Statistics */}
              <div>
                <motion.h3
                  className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  <BarChart3 className="w-4 h-4 text-primary" />
                  Processing Metrics
                </motion.h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {[
                    { label: 'PSNR', value: 32.5, unit: 'dB', variant: 'primary' as const, icon: '📊' },
                    { label: 'SSIM', value: 0.89, unit: 'score', variant: 'secondary' as const, icon: '✓' },
                    { label: 'Processing', value: 2340, unit: 'ms', variant: 'accent' as const, icon: '⏱️' },
                    { label: 'Objects', value: 12, unit: 'detected', variant: 'warning' as const, icon: '🎯' },
                  ].map((metric, idx) => (
                    <motion.div
                      key={metric.label}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.35 + idx * 0.08 }}
                    >
                      <MetricsGauge
                        label={metric.label}
                        value={metric.value}
                        unit={metric.unit}
                        variant={metric.variant}
                        icon={metric.icon}
                        max={metric.label === 'SSIM' ? 1 : metric.label === 'Objects' ? 50 : 50000}
                        format={metric.label === 'SSIM' ? 'percentage' : metric.label === 'Processing' ? 'time' : 'number'}
                      />
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Gemini Analysis */}
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.65 }}
              >
                <h3 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
                  <Zap className="w-4 h-4 text-accent" />
                  AI Scene Analysis
                </h3>
                <GeminiAnalysisCard />
              </motion.div>

              {/* Info Footer */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.7 }}
              >
                <GlassCard compact hover={false}>
                  <div className="px-4 py-3 text-center">
                    <p className="text-xs text-muted-foreground">
                      💡 Upload a thermal image from the left panel to begin processing and analysis
                    </p>
                  </div>
                </GlassCard>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default function Page() {
  return (
    <AuthProvider>
      <ImageProvider>
        <PipelineProvider>
          <IRISCommandCenter />
        </PipelineProvider>
      </ImageProvider>
    </AuthProvider>
  )
}
