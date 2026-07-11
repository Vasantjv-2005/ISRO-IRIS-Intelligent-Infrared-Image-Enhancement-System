'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, Zap, FileDown, CheckCircle2 } from 'lucide-react'
import { usePipeline } from '@/lib/context/PipelineContext'
import { useImage } from '@/lib/context/ImageContext'
import { GlassCard } from '@/components/ui/GlassCard'
import { Badge } from '@/components/ui/Badge'
import { Spinner } from '@/components/ui/Spinner'
import { UploadDropzone } from '@/components/visualization/UploadDropzone'
import { ColormapPaletteSelector } from '@/components/visualization/ColormapPaletteSelector'

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
  const { currentImage } = useImage()
  const [expandedStep, setExpandedStep] = useState<string | null>('upload')

  return (
    <div className="space-y-4">
      {/* Status Overview */}
      <GlassCard>
        <div className="p-4 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-foreground">Pipeline Status</h3>
            {state.isProcessing && <Spinner size="sm" variant="orbital" />}
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">Progress</span>
              <span className="text-primary font-bold">{state.completedSteps.length} / 6</span>
            </div>
            <div className="w-full h-1 bg-background rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-primary to-secondary rounded-full"
                animate={{ width: `${(state.completedSteps.length / 6) * 100}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
          </div>

          {state.processingStatus && (
            <p className="text-xs text-muted-foreground">{state.processingStatus}</p>
          )}

          {state.error && (
            <div className="p-2 rounded-lg bg-destructive/10 border border-destructive/30">
              <p className="text-xs text-destructive">{state.error}</p>
            </div>
          )}
        </div>
      </GlassCard>

      {/* Steps Accordion */}
      <div className="space-y-2">
        {steps.map((step, idx) => {
          const isCompleted = state.completedSteps.includes(step.id as any)
          const isActive = state.currentStep === step.id

          return (
            <motion.div
              key={step.id}
              layout
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.05 }}
            >
              <GlassCard compact hover={isActive}>
                <button
                  onClick={() => setExpandedStep(expandedStep === step.id ? null : step.id)}
                  className={`w-full p-4 transition-all ${isActive ? 'ring-1 ring-primary' : ''}`}
                >
                  <div className="flex items-center gap-3">
                    {/* Status indicator */}
                    <div className="text-lg">{step.icon}</div>

                    {/* Title and description */}
                    <div className="flex-1 text-left min-w-0">
                      <h4 className="text-sm font-semibold text-foreground line-clamp-1">{step.title}</h4>
                      <p className="text-xs text-muted-foreground line-clamp-1">{step.description}</p>
                    </div>

                    {/* Badges */}
                    <div className="flex items-center gap-2">
                      {isCompleted && <CheckCircle2 className="w-4 h-4 text-secondary" />}
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
                      className="border-t border-border overflow-hidden"
                    >
                      <div className="p-4 space-y-3">
                        {step.id === 'upload' && <UploadDropzone />}

                        {step.id === 'preprocessing' && currentImage && (
                          <div className="space-y-3">
                            <label className="flex items-center gap-2 cursor-pointer">
                              <input
                                type="checkbox"
                                checked={settings.denoise}
                                onChange={(e) => updateSettings({ denoise: e.target.checked })}
                                className="w-4 h-4"
                              />
                              <span className="text-sm text-foreground">Denoise</span>
                            </label>
                            <label className="flex items-center gap-2 cursor-pointer">
                              <input
                                type="checkbox"
                                checked={settings.contrastEnhancement}
                                onChange={(e) => updateSettings({ contrastEnhancement: e.target.checked })}
                                className="w-4 h-4"
                              />
                              <span className="text-sm text-foreground">Contrast Enhancement</span>
                            </label>
                          </div>
                        )}

                        {step.id === 'enhancement' && currentImage && (
                          <div className="space-y-2">
                            <label className="text-sm text-foreground">Enhancement Level</label>
                            <input
                              type="range"
                              min="1"
                              max="4"
                              value={settings.enhancementLevel}
                              onChange={(e) => updateSettings({ enhancementLevel: parseInt(e.target.value) })}
                              className="w-full"
                            />
                            <p className="text-xs text-muted-foreground">Level: {settings.enhancementLevel}</p>
                          </div>
                        )}

                        {step.id === 'colorization' && currentImage && (
                          <ColormapPaletteSelector
                            selectedColormap={settings.colormap}
                            onSelect={(id) => updateSettings({ colormap: id })}
                            compact
                          />
                        )}

                        {step.id === 'detection' && currentImage && (
                          <div className="space-y-2">
                            <label className="text-sm text-foreground">Confidence Threshold</label>
                            <input
                              type="range"
                              min="0.1"
                              max="0.95"
                              step="0.05"
                              value={settings.detectionConfidence}
                              onChange={(e) => updateSettings({ detectionConfidence: parseFloat(e.target.value) })}
                              className="w-full"
                            />
                            <p className="text-xs text-muted-foreground">{(settings.detectionConfidence * 100).toFixed(0)}% confidence</p>
                          </div>
                        )}

                        {step.id === 'analysis' && currentImage && (
                          <textarea
                            placeholder="Optional: Add context for Gemini analysis"
                            value={settings.geminiContext}
                            onChange={(e) => updateSettings({ geminiContext: e.target.value })}
                            className="w-full p-2 rounded-lg bg-background/50 border border-border text-sm text-foreground placeholder-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
                            rows={3}
                          />
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
      <div className="space-y-2 pt-4">
        <button className="w-full py-3 rounded-lg bg-gradient-to-r from-primary to-secondary text-background font-bold text-sm hover:shadow-[0_0_20px_rgba(0,240,255,0.5)] transition-all active:scale-95 flex items-center justify-center gap-2">
          <Zap className="w-5 h-5" />
          Run Full Pipeline
        </button>

        {currentImage && state.completedSteps.length > 0 && (
          <button className="w-full py-3 rounded-lg bg-gradient-to-r from-orange-600 to-amber-600 text-background font-bold text-sm hover:shadow-[0_0_20px_rgba(255,107,0,0.5)] transition-all active:scale-95 flex items-center justify-center gap-2">
            <FileDown className="w-5 h-5" />
            Export Report (PDF)
          </button>
        )}
      </div>
    </div>
  )
}
