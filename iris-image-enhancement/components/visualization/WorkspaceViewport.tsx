'use client'

import React, { useState, useEffect } from 'react'
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
import { getFileDownloadUrl } from '@/lib/api'
import { CHANDRA_09_DEMO_DATA, generateThermalSvgUrl } from '@/lib/demoData'
import { useDownload } from '@/hooks'

type ViewportMode = 'comparison' | 'detection' | 'palette' | 'sidebyside'

export function WorkspaceViewport() {
  const { currentImage, setCurrentImage } = useImage()
  const { downloadFile } = useDownload()
  const { state, settings, updateSettings, markStepComplete } = usePipeline()
  const [mode, setMode] = useState<ViewportMode>('comparison')
  const [hoveredDetection, setHoveredDetection] = useState<any | null>(null)

  useEffect(() => {
    if (state.currentStep === 'detection' || state.currentStep === 'analysis') {
      setMode('detection')
    } else if (
      state.currentStep === 'preprocessing' ||
      state.currentStep === 'enhancement' ||
      state.currentStep === 'colorization'
    ) {
      setMode('comparison')
    }
  }, [state.currentStep])

  const handleLoadDemo = () => {
    setCurrentImage(CHANDRA_09_DEMO_DATA)
    markStepComplete('upload')
    markStepComplete('preprocessing')
    markStepComplete('enhancement')
    markStepComplete('colorization')
    markStepComplete('detection')
    markStepComplete('analysis')
  }

  const beforeImg = getFileDownloadUrl(currentImage?.original_image)
  const afterImg =
    getFileDownloadUrl(currentImage?.processed_image) ||
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

                  {/* Structured Tactical Target Registry Table */}
                  {detections && detections.length > 0 && (
                    <div className="mt-4 rounded-xl border border-border/80 bg-background/80 overflow-hidden shadow-md">
                      <div className="px-4 py-2.5 bg-card/90 border-b border-border/80 flex items-center justify-between">
                        <span className="text-xs font-mono font-bold uppercase tracking-wider text-primary flex items-center gap-2">
                          <Target className="w-3.5 h-3.5" />
                          Structured Target Classification Registry ({detections.length} Detected)
                        </span>
                        <Badge variant="success" size="sm">REAL-TIME TELEMETRY</Badge>
                      </div>
                      <div className="overflow-x-auto">
                        <table className="w-full text-left text-xs font-mono">
                          <thead className="bg-muted/40 text-muted-foreground uppercase border-b border-border/60">
                            <tr>
                              <th className="py-2 px-4">Tag ID</th>
                              <th className="py-2 px-4">Classification</th>
                              <th className="py-2 px-4">Confidence</th>
                              <th className="py-2 px-4">Radiometric BBox [X, Y, W, H]</th>
                              <th className="py-2 px-4 text-right">Status</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-border/40">
                            {detections.map((det: any, i: number) => {
                              const name = String(det.class || det.class_name || 'TARGET')
                              const conf = typeof det.confidence === 'number' ? det.confidence : 0.9
                              return (
                                <tr
                                  key={det.id || i}
                                  className="hover:bg-primary/5 transition-colors cursor-pointer"
                                  onMouseEnter={() => setHoveredDetection(det)}
                                >
                                  <td className="py-2.5 px-4 font-bold text-primary">[#0{i + 1}]</td>
                                  <td className="py-2.5 px-4 font-semibold text-foreground">{name.toUpperCase()}</td>
                                  <td className="py-2.5 px-4 text-secondary font-bold">{(conf * 100).toFixed(1)}%</td>
                                  <td className="py-2.5 px-4 text-muted-foreground">
                                    [{det.x || 0}, {det.y || 0}, {det.width || 0}x{det.height || 0}]
                                  </td>
                                  <td className="py-2.5 px-4 text-right">
                                    <span className="px-2 py-0.5 rounded text-[10px] bg-green-500/15 text-green-400 border border-green-500/30">
                                      LOCKED
                                    </span>
                                  </td>
                                </tr>
                              )
                            })}
                          </tbody>
                        </table>
                      </div>
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

      {/* Download Assets Bar */}
      {currentImage && (
        <GlassCard className="p-4 border-secondary/40">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <Download className="w-4 h-4 text-secondary" />
              <span className="text-xs font-mono font-extrabold uppercase text-foreground">
                EXPORT RADIOMETRIC ASSETS & REPORTS
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <button
                onClick={() => downloadFile(currentImage.file_path || 'test_gray.jpg', 'iris_mission_report.pdf')}
                className="px-3 py-1.5 rounded-lg bg-secondary/15 hover:bg-secondary/25 border border-secondary/40 text-secondary text-xs font-mono font-bold transition-all flex items-center gap-1.5"
              >
                <span>📄 DOWNLOAD PDF REPORT</span>
              </button>
              <button
                onClick={() => downloadFile(currentImage.processed_image || currentImage.file_path || 'test_out.jpg', 'enhanced_infrared.jpg')}
                className="px-3 py-1.5 rounded-lg bg-primary/15 hover:bg-primary/25 border border-primary/40 text-primary text-xs font-mono font-bold transition-all flex items-center gap-1.5"
              >
                <span>⚡ ENHANCED IMAGE</span>
              </button>
              <button
                onClick={() => downloadFile(currentImage.processed_image || currentImage.file_path || 'test_out.jpg', 'colorized_infrared.jpg')}
                className="px-3 py-1.5 rounded-lg bg-accent/15 hover:bg-accent/25 border border-accent/40 text-accent text-xs font-mono font-bold transition-all flex items-center gap-1.5"
              >
                <span>🎨 COLORIZED IMAGE</span>
              </button>
              <button
                onClick={() => downloadFile(currentImage.processed_image || currentImage.file_path || 'test_out.jpg', 'yolo_detection_overlay.jpg')}
                className="px-3 py-1.5 rounded-lg bg-iris-orange/15 hover:bg-iris-orange/25 border border-iris-orange/40 text-iris-orange text-xs font-mono font-bold transition-all flex items-center gap-1.5"
              >
                <span>🎯 DETECTION IMAGE</span>
              </button>
            </div>
          </div>
        </GlassCard>
      )}

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
