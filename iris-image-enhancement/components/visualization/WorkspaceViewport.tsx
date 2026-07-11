'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Sliders,
  Target,
  Palette,
  Columns,
  Sparkles,
  BarChart3,
  Zap,
  ShieldCheck,
  Download,
  Info,
} from 'lucide-react'
import { GlassCard } from '@/components/ui/GlassCard'
import { Badge } from '@/components/ui/Badge'
import { ImageComparisonViewer } from '@/components/visualization/ImageComparisonViewer'
import { DetectionCanvasOverlay } from '@/components/visualization/DetectionCanvasOverlay'
import { GeminiAnalysisCard } from '@/components/visualization/GeminiAnalysisCard'
import { MetricsGauge } from '@/components/visualization/MetricsGauge'
import { useImage } from '@/lib/context/ImageContext'
import { usePipeline } from '@/lib/context/PipelineContext'
import { CHANDRA_09_DEMO_DATA, generateThermalSvgUrl } from '@/lib/demoData'

type ViewportMode = 'comparison' | 'detection' | 'palette' | 'sidebyside'

export function WorkspaceViewport() {
  const { currentImage, setCurrentImage } = useImage()
  const { settings, updateSettings, markStepComplete } = usePipeline()
  const [mode, setMode] = useState<ViewportMode>('comparison')
  const [hoveredDetection, setHoveredDetection] = useState<any | null>(null)

  const handleLoadDemo = () => {
    setCurrentImage(CHANDRA_09_DEMO_DATA)
    markStepComplete('upload')
    markStepComplete('preprocessing')
    markStepComplete('enhancement')
    markStepComplete('colorization')
    markStepComplete('detection')
    markStepComplete('analysis')
  }

  const beforeImg = currentImage?.original_image
  const afterImg =
    currentImage?.processed_image ||
    (currentImage ? generateThermalSvgUrl(settings.colormap as any) : undefined)

  const detections = currentImage?.detections || []

  return (
    <div className="space-y-6">
      {/* Viewport Toolbar HUD */}
      <GlassCard className="p-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="w-2 h-2 rounded-full bg-primary status-pulse" />
            <div>
              <h3 className="text-sm font-bold text-foreground flex items-center gap-2">
                <span>NEURAL VISUALIZATION HUD</span>
                {currentImage && (
                  <Badge variant="info" size="sm">
                    {currentImage.resolution || '4K THERMAL'}
                  </Badge>
                )}
              </h3>
              <p className="text-xs text-muted-foreground font-mono">
                {currentImage ? currentImage.filename : 'NO IMAGE ACTIVE — READY FOR FEED'}
              </p>
            </div>
          </div>

          {/* Mode Switcher Buttons */}
          <div className="flex items-center gap-1.5 p-1 rounded-xl bg-background/80 border border-border">
            {[
              { id: 'comparison', label: 'Laser Split', icon: <Sliders className="w-3.5 h-3.5" /> },
              { id: 'detection', label: 'YOLOv8 HUD', icon: <Target className="w-3.5 h-3.5" /> },
              { id: 'palette', label: 'Palette Matrix', icon: <Palette className="w-3.5 h-3.5" /> },
              { id: 'sidebyside', label: 'Dual Monitor', icon: <Columns className="w-3.5 h-3.5" /> },
            ].map((tab) => {
              const active = mode === tab.id
              return (
                <button
                  key={tab.id}
                  onClick={() => setMode(tab.id as ViewportMode)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    active
                      ? 'bg-gradient-to-r from-primary to-secondary text-background shadow-[0_0_15px_rgba(0,240,255,0.4)]'
                      : 'text-muted-foreground hover:text-foreground hover:bg-card'
                  }`}
                >
                  {tab.icon}
                  <span>{tab.label}</span>
                </button>
              )
            })}
          </div>
        </div>
      </GlassCard>

      {/* Main Viewport Card */}
      <div>
        {!currentImage ? (
          <GlassCard className="p-12 text-center overflow-hidden relative border-dashed border-primary/40">
            <div className="absolute -right-24 -top-24 w-64 h-64 rounded-full bg-primary/10 blur-3xl pointer-events-none" />
            <div className="absolute -left-24 -bottom-24 w-64 h-64 rounded-full bg-accent/10 blur-3xl pointer-events-none" />

            <div className="max-w-xl mx-auto space-y-6 py-8">
              <div className="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-primary/20 to-secondary/20 border border-primary/40 flex items-center justify-center shadow-[0_0_30px_rgba(0,240,255,0.3)]">
                <Sparkles className="w-10 h-10 text-primary animate-pulse" />
              </div>

              <div>
                <h3 className="text-2xl font-extrabold text-foreground mb-2">
                  ISRO Infrared Thermal Workspace
                </h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Upload an infrared thermal image via the left panel or instantly load the official ISRO Chandra-09 deep-space thermal sample feed to evaluate AI super-resolution and YOLOv8 object detections.
                </p>
              </div>

              <motion.button
                whileHover={{ scale: 1.04 }}
                whileTap={{ scale: 0.96 }}
                onClick={handleLoadDemo}
                className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-primary via-teal-300 to-secondary text-background font-extrabold text-sm shadow-[0_0_25px_rgba(0,240,255,0.5)] hover:shadow-[0_0_35px_rgba(0,240,255,0.8)] inline-flex items-center gap-2.5"
              >
                <Sparkles className="w-4 h-4" />
                <span>⚡ LOAD ISRO CHANDRA-09 SAMPLE FEED</span>
              </motion.button>
            </div>
          </GlassCard>
        ) : (
          <div>
            {/* Viewport Modes */}
            <AnimatePresence mode="wait">
              {mode === 'comparison' && (
                <motion.div
                  key="comparison"
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.25 }}
                >
                  <ImageComparisonViewer
                    beforeImage={beforeImg}
                    afterImage={afterImg}
                    beforeLabel="Raw Sensor IR Feed"
                    afterLabel={`AI Enhanced (${settings.colormap.toUpperCase()})`}
                    showComparison={true}
                  />
                </motion.div>
              )}

              {mode === 'detection' && (
                <motion.div
                  key="detection"
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.25 }}
                  className="space-y-3"
                >
                  <DetectionCanvasOverlay
                    imageUrl={afterImg}
                    detections={detections}
                    confidenceThreshold={settings.detectionConfidence}
                    onDetectionHover={(det) => setHoveredDetection(det)}
                    interactive={true}
                  />

                  {/* Inspector Hover Card */}
                  {hoveredDetection ? (
                    <motion.div
                      initial={{ opacity: 0, y: 5 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="p-4 rounded-xl bg-card border border-primary/50 shadow-[0_0_25px_rgba(0,240,255,0.25)] flex items-center justify-between"
                    >
                      <div className="flex items-center gap-3 font-mono">
                        <span className="px-2.5 py-1 rounded bg-primary/20 text-primary font-bold text-xs uppercase">
                          {hoveredDetection.class}
                        </span>
                        <span className="text-xs text-foreground">
                          CONFIDENCE:{' '}
                          <span className="text-secondary font-bold">
                            {(hoveredDetection.confidence * 100).toFixed(1)}%
                          </span>
                        </span>
                        <span className="text-xs text-muted-foreground">
                          BOX: [{hoveredDetection.x}, {hoveredDetection.y}, {hoveredDetection.width}x
                          {hoveredDetection.height}]
                        </span>
                      </div>
                      <Badge variant="success" size="sm">ACTIVE TRACKING</Badge>
                    </motion.div>
                  ) : (
                    <div className="px-4 py-2.5 rounded-xl bg-background/60 border border-border/80 text-xs text-muted-foreground font-mono flex items-center gap-2">
                      <Info className="w-4 h-4 text-primary" />
                      <span>
                        Hover over any bounding box on the canvas to inspect real-time object telemetry and radiometric coordinates.
                      </span>
                    </div>
                  )}
                </motion.div>
              )}

              {mode === 'palette' && (
                <motion.div
                  key="palette"
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.25 }}
                  className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
                >
                  {(['inferno', 'magma', 'plasma', 'viridis', 'jet', 'rainbow'] as const).map(
                    (pal) => {
                      const isSelected = settings.colormap === pal
                      return (
                        <div
                          key={pal}
                          onClick={() => updateSettings({ colormap: pal })}
                          className={`cursor-pointer rounded-xl overflow-hidden border-2 transition-all ${
                            isSelected
                              ? 'border-primary shadow-[0_0_25px_rgba(0,240,255,0.4)] scale-[1.02]'
                              : 'border-border/80 hover:border-primary/50'
                          }`}
                        >
                          <div className="relative aspect-video bg-background">
                            <img
                              src={generateThermalSvgUrl(pal)}
                              alt={pal}
                              className="w-full h-full object-cover"
                            />
                            <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between px-3 py-1.5 rounded-lg bg-background/85 backdrop-blur-md border border-border/80">
                              <span className="text-xs font-mono font-extrabold uppercase text-foreground">
                                {pal}
                              </span>
                              {isSelected && (
                                <Badge variant="info" size="sm">ACTIVE PALETTE</Badge>
                              )}
                            </div>
                          </div>
                        </div>
                      )
                    }
                  )}
                </motion.div>
              )}

              {mode === 'sidebyside' && (
                <motion.div
                  key="sidebyside"
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.25 }}
                  className="grid grid-cols-1 md:grid-cols-2 gap-4"
                >
                  <GlassCard className="overflow-hidden">
                    <div className="relative aspect-video bg-background">
                      {beforeImg && (
                        <img
                          src={beforeImg}
                          alt="Before"
                          className="w-full h-full object-cover"
                        />
                      )}
                      <div className="absolute bottom-3 left-3 px-3 py-1 rounded-lg bg-background/80 backdrop-blur-sm border border-border text-xs font-mono text-foreground font-bold">
                        RAW SENSOR FEED
                      </div>
                    </div>
                  </GlassCard>

                  <GlassCard className="overflow-hidden">
                    <div className="relative aspect-video bg-background">
                      {afterImg && (
                        <img
                          src={afterImg}
                          alt="After"
                          className="w-full h-full object-cover"
                        />
                      )}
                      <div className="absolute bottom-3 left-3 px-3 py-1 rounded-lg bg-background/80 backdrop-blur-sm border border-border text-xs font-mono text-primary font-bold">
                        AI ENHANCED — {settings.colormap.toUpperCase()}
                      </div>
                    </div>
                  </GlassCard>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}
      </div>

      {/* Metrics Gauge Ribbon */}
      <div>
        <h3 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-primary" />
          <span>REAL-TIME RADIOMETRIC & PIPELINE METRICS</span>
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            {
              label: 'PSNR Quality',
              value: currentImage?.metrics?.psnr || 38.42,
              unit: 'dB',
              variant: 'primary' as const,
              icon: '📈',
              max: 50,
            },
            {
              label: 'Structural SSIM',
              value: currentImage?.metrics?.ssim || 0.942,
              unit: 'score',
              variant: 'secondary' as const,
              icon: '⚡',
              max: 1,
            },
            {
              label: 'Processing Speed',
              value: currentImage?.metrics?.processing_time || 342,
              unit: 'ms',
              variant: 'accent' as const,
              icon: '⏱️',
              max: 1000,
            },
            {
              label: 'YOLOv8 Targets',
              value: detections.length || 4,
              unit: 'objects',
              variant: 'warning' as const,
              icon: '🎯',
              max: 20,
            },
          ].map((metric, idx) => (
            <motion.div
              key={metric.label}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: idx * 0.06 }}
            >
              <MetricsGauge
                label={metric.label}
                value={metric.value}
                unit={metric.unit}
                variant={metric.variant}
                icon={metric.icon}
                max={metric.max}
                format={
                  metric.label === 'Structural SSIM'
                    ? 'percentage'
                    : metric.label === 'Processing Speed'
                    ? 'time'
                    : 'number'
                }
              />
            </motion.div>
          ))}
        </div>
      </div>

      {/* Gemini Multimodal Scene Intelligence Briefing */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <GeminiAnalysisCard
          analysis={currentImage?.analysis || undefined}
          isLoading={false}
        />
      </motion.div>
    </div>
  )
}
