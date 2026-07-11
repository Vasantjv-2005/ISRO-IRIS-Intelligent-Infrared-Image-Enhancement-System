'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, Zap, FileDown, CheckCircle2, Sparkles, Sliders, ShieldAlert, Cpu } from 'lucide-react'
import { usePipeline } from '@/lib/context/PipelineContext'
import { useImage } from '@/lib/context/ImageContext'
import { GlassCard } from '@/components/ui/GlassCard'
import { Badge } from '@/components/ui/Badge'
import { Spinner } from '@/components/ui/Spinner'
import { UploadDropzone } from '@/components/visualization/UploadDropzone'
import { ColormapPaletteSelector } from '@/components/visualization/ColormapPaletteSelector'
import { CHANDRA_09_DEMO_DATA } from '@/lib/demoData'

interface StepConfig {
  id: string
  title: string
  icon: React.ReactNode
  description: string
}

const steps: StepConfig[] = [
  {
    id: 'upload',
    title: 'Step 1: Upload Image',
    icon: '📤',
    description: 'Load thermal infrared imagery',
  },
  {
    id: 'preprocessing',
    title: 'Step 2: Preprocessing',
    icon: '🔧',
    description: 'Denoise & enhance contrast',
  },
  {
    id: 'enhancement',
    title: 'Step 3: AI Enhancement',
    icon: '⚡',
    description: 'Super-resolution processing',
  },
  {
    id: 'colorization',
    title: 'Step 4: Colorization',
    icon: '🎨',
    description: 'Apply thermal palette',
  },
  {
    id: 'detection',
    title: 'Step 5: Detection',
    icon: '🎯',
    description: 'Object detection & tracking',
  },
  {
    id: 'analysis',
    title: 'Step 6: Analysis',
    icon: '🧠',
    description: 'Gemini AI interpretation',
  },
]

export function PipelinePanel() {
  const { state, settings, updateSettings, setIsProcessing, markStepComplete } = usePipeline()
  const { currentImage, setCurrentImage } = useImage()
  const [expandedStep, setExpandedStep] = useState<string | null>('upload')
  const [exporting, setExporting] = useState(false)

  const handleLoadDemo = () => {
    setCurrentImage(CHANDRA_09_DEMO_DATA)
    markStepComplete('upload')
    markStepComplete('preprocessing')
    markStepComplete('enhancement')
    markStepComplete('colorization')
    markStepComplete('detection')
    markStepComplete('analysis')
  }

  const handleRunFullPipeline = () => {
    if (!currentImage) {
      handleLoadDemo()
    } else {
      markStepComplete('upload')
      markStepComplete('preprocessing')
      markStepComplete('enhancement')
      markStepComplete('colorization')
      markStepComplete('detection')
      markStepComplete('analysis')
    }
  }

  const handleExportPdf = () => {
    setExporting(true)
    setTimeout(() => {
      setExporting(false)
      alert('Generating & Exporting ISRO IRIS Official PDF Dossier...')
    }, 1200)
  }

  return (
    <div className="space-y-4">
      {/* Status Overview */}
      <GlassCard className="p-4 space-y-3.5 border-primary/30 shadow-[0_0_20px_rgba(0,240,255,0.12)]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Cpu className="w-4 h-4 text-primary" />
            <h3 className="text-sm font-extrabold tracking-wide text-foreground uppercase">
              Pipeline Telemetry
            </h3>
          </div>
          {state.isProcessing && <Spinner size="sm" variant="orbital" />}
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-muted-foreground">MISSION PIPELINE SYNC</span>
            <span className="text-primary font-bold">
              {state.completedSteps.length} / 6 STEPS COMPLETED
            </span>
          </div>
          <div className="w-full h-1.5 bg-background/90 rounded-full overflow-hidden border border-border/80">
            <motion.div
              className="h-full bg-gradient-to-r from-primary via-teal-400 to-secondary rounded-full shadow-[0_0_10px_#00F0FF]"
              animate={{ width: `${(state.completedSteps.length / 6) * 100}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>

        {/* Instant Demo Trigger */}
        <button
          onClick={handleLoadDemo}
          className="w-full py-2 px-3 rounded-lg bg-primary/15 hover:bg-primary/25 border border-primary/40 text-primary text-xs font-mono font-bold transition-all flex items-center justify-center gap-2 shadow-[0_0_15px_rgba(0,240,255,0.15)]"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>⚡ LOAD CHANDRA-09 SAMPLE FEED</span>
        </button>

        {state.processingStatus && (
          <p className="text-xs text-muted-foreground font-mono">{state.processingStatus}</p>
        )}

        {state.error && (
          <div className="p-2.5 rounded-lg bg-destructive/15 border border-destructive/40">
            <p className="text-xs text-destructive font-mono">{state.error}</p>
          </div>
        )}
      </GlassCard>

      {/* Steps Accordion */}
      <div className="space-y-2.5">
        {steps.map((step, idx) => {
          const isCompleted = state.completedSteps.includes(step.id as any)
          const isActive = state.currentStep === step.id

          return (
            <motion.div
              key={step.id}
              layout
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.04 }}
            >
              <GlassCard compact hover={isActive} className={isCompleted ? 'border-secondary/40' : ''}>
                <button
                  onClick={() => setExpandedStep(expandedStep === step.id ? null : step.id)}
                  className={`w-full p-4 transition-all ${isActive ? 'ring-1 ring-primary rounded-xl' : ''}`}
                >
                  <div className="flex items-center gap-3">
                    {/* Status indicator */}
                    <div className="text-lg">{step.icon}</div>

                    {/* Title and description */}
                    <div className="flex-1 text-left min-w-0">
                      <h4 className="text-sm font-bold text-foreground line-clamp-1">{step.title}</h4>
                      <p className="text-xs text-muted-foreground line-clamp-1">{step.description}</p>
                    </div>

                    {/* Badges */}
                    <div className="flex items-center gap-2">
                      {isCompleted && (
                        <CheckCircle2 className="w-4 h-4 text-secondary drop-shadow-[0_0_6px_rgba(0,210,180,0.8)]" />
                      )}
                      {isActive && !isCompleted && <Spinner size="sm" variant="dots" />}
                      <ChevronDown
                        className={`w-4 h-4 text-muted-foreground transition-transform ${
                          expandedStep === step.id ? 'rotate-180' : ''
                        }`}
                      />
                    </div>
                  </div>
                </button>

                {/* Expanded content */}
                <AnimatePresence>
                  {expandedStep === step.id && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="border-t border-border/80 overflow-hidden"
                    >
                      <div className="p-4 space-y-3.5 bg-background/40">
                        {step.id === 'upload' && (
                          <div className="space-y-3">
                            <UploadDropzone />
                            <div className="text-center">
                              <span className="text-xs text-muted-foreground font-mono">
                                — OR TEST WITH ISRO ARCHIVE SAMPLE —
                              </span>
                            </div>
                            <button
                              onClick={handleLoadDemo}
                              className="w-full py-2 rounded-lg bg-secondary/15 hover:bg-secondary/25 text-secondary border border-secondary/40 text-xs font-mono font-bold transition-all"
                            >
                              🚀 LOAD CHANDRA-09 THERMAL TIFF
                            </button>
                          </div>
                        )}

                        {step.id === 'preprocessing' && (
                          <div className="space-y-3">
                            <label className="flex items-center justify-between p-2.5 rounded-lg bg-background/60 border border-border/80 cursor-pointer hover:border-primary/50 transition-all">
                              <span className="text-sm font-semibold text-foreground">Spatial Denoising</span>
                              <input
                                type="checkbox"
                                checked={settings.denoise}
                                onChange={(e) => updateSettings({ denoise: e.target.checked })}
                                className="w-4 h-4 accent-primary"
                              />
                            </label>
                            <label className="flex items-center justify-between p-2.5 rounded-lg bg-background/60 border border-border/80 cursor-pointer hover:border-primary/50 transition-all">
                              <span className="text-sm font-semibold text-foreground">Contrast Enhancement</span>
                              <input
                                type="checkbox"
                                checked={settings.contrastEnhancement}
                                onChange={(e) => updateSettings({ contrastEnhancement: e.target.checked })}
                                className="w-4 h-4 accent-primary"
                              />
                            </label>
                          </div>
                        )}

                        {step.id === 'enhancement' && (
                          <div className="space-y-3 p-3 rounded-lg bg-background/60 border border-border/80">
                            <div className="flex items-center justify-between">
                              <span className="text-sm font-semibold text-foreground">Super-Resolution</span>
                              <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-primary/20 text-primary border border-primary/40">
                                {settings.enhancementLevel}X UPSAMPLE
                              </span>
                            </div>
                            <input
                              type="range"
                              min="1"
                              max="4"
                              value={settings.enhancementLevel}
                              onChange={(e) => updateSettings({ enhancementLevel: parseInt(e.target.value) })}
                              className="w-full accent-primary cursor-pointer"
                            />
                            <div className="flex justify-between text-[10px] font-mono text-muted-foreground">
                              <span>1X (Standard)</span>
                              <span>2X (Bicubic)</span>
                              <span>4X (Deep Residual AI)</span>
                            </div>
                          </div>
                        )}

                        {step.id === 'colorization' && (
                          <ColormapPaletteSelector
                            selectedColormap={settings.colormap}
                            onSelect={(id) => updateSettings({ colormap: id })}
                            compact
                          />
                        )}

                        {step.id === 'detection' && (
                          <div className="space-y-3 p-3 rounded-lg bg-background/60 border border-border/80">
                            <div className="flex items-center justify-between">
                              <span className="text-sm font-semibold text-foreground">YOLOv8 Threshold</span>
                              <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-iris-orange/20 text-iris-orange border border-iris-orange/40">
                                {(settings.detectionConfidence * 100).toFixed(0)}% CONFIDENCE
                              </span>
                            </div>
                            <input
                              type="range"
                              min="0.1"
                              max="0.95"
                              step="0.05"
                              value={settings.detectionConfidence}
                              onChange={(e) =>
                                updateSettings({ detectionConfidence: parseFloat(e.target.value) })
                              }
                              className="w-full accent-iris-orange cursor-pointer"
                            />
                            <p className="text-[11px] font-mono text-muted-foreground">
                              Filters out background thermal clutter below {(settings.detectionConfidence * 100).toFixed(0)}%.
                            </p>
                          </div>
                        )}

                        {step.id === 'analysis' && (
                          <div className="space-y-2">
                            <textarea
                              placeholder="Optional: Enter mission brief context or target coordinates for Gemini AI..."
                              value={settings.geminiContext}
                              onChange={(e) => updateSettings({ geminiContext: e.target.value })}
                              className="w-full p-3 rounded-xl bg-background/80 border border-border text-xs text-foreground font-mono placeholder-muted-foreground focus:outline-none focus:border-primary shadow-inner"
                              rows={3}
                            />
                          </div>
                        )}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </GlassCard>
            </motion.div>
          )
        })}
      </div>

      {/* Action buttons */}
      <div className="space-y-2.5 pt-2">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleRunFullPipeline}
          className="w-full py-3.5 rounded-xl bg-gradient-to-r from-primary via-teal-400 to-secondary text-background font-extrabold text-sm shadow-[0_0_25px_rgba(0,240,255,0.4)] hover:shadow-[0_0_35px_rgba(0,240,255,0.7)] transition-all flex items-center justify-center gap-2"
        >
          <Zap className="w-5 h-5" />
          <span>RUN FULL INTELLIGENT PIPELINE</span>
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleExportPdf}
          disabled={exporting}
          className="w-full py-3.5 rounded-xl bg-gradient-to-r from-iris-orange to-iris-amber text-background font-extrabold text-sm shadow-[0_0_25px_rgba(255,107,0,0.35)] hover:shadow-[0_0_35px_rgba(255,107,0,0.6)] transition-all flex items-center justify-center gap-2"
        >
          <FileDown className="w-5 h-5" />
          <span>{exporting ? 'EXPORTING PDF DOSSIER...' : 'EXPORT MISSION DOSSIER (PDF)'}</span>
        </motion.button>
      </div>
    </div>
  )
}
