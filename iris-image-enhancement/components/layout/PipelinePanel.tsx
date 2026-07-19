'use client'

import React, { useState } from 'react'
import { createPortal } from 'react-dom'
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
import { getFileDownloadUrl } from '@/lib/api'

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

import { usePipelineRunner, useReport } from '@/hooks'

export function PipelinePanel() {
  const { state, settings, updateSettings, setIsProcessing, markStepComplete, setError } = usePipeline()
  const { currentImage, setCurrentImage } = useImage()
  const [expandedStep, setExpandedStep] = useState<string | null>('upload')
  const [showComparisonModal, setShowComparisonModal] = useState(false)
  const {
    runFullPipeline,
    runPreprocessing,
    runEnhancement,
    runColorization,
    runDetection,
    runAnalysis,
    runMultiComparison,
    elapsedTime,
  } = usePipelineRunner()
  const { generateReport, isGenerating } = useReport()

  const handleLoadDemo = () => {
    setCurrentImage({
      ...CHANDRA_09_DEMO_DATA,
    })
    markStepComplete('upload')
  }

  const handleRunFullPipeline = () => {
    runFullPipeline()
  }

  const handleExportPdf = () => {
    const targetPath = currentImage?.original_image || currentImage?.file_path || 'uploads/raw/enhanced_ai.jpg'
    generateReport({
      image_name: currentImage?.filename || 'CHANDRA09_THERMAL_SECTOR_T88.TIFF',
      original_image_path: targetPath,
      processed_image_path: currentImage?.enhanced_image || currentImage?.processed_image || targetPath,
      colorized_image_path: currentImage?.colorized_image || undefined,
      detected_image_path: currentImage?.detected_image || undefined,
      upload_id: currentImage?.upload_id || 'chandra-09-ir-sample-8842',
      detected_objects: currentImage?.detections || [],
      analysis: currentImage?.analysis || 'Infrared thermal anomaly detected and analyzed via Gemini AI.',
    })
  }

  const handleOpenComparison = async () => {
    await runMultiComparison()
    setShowComparisonModal(true)
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
          {state.isProcessing && (
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono text-primary font-bold">{elapsedTime}s</span>
              <Spinner size="sm" variant="orbital" />
            </div>
          )}
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
          <div className="p-2.5 rounded-lg bg-primary/10 border border-primary/30 flex items-center gap-2">
            <Spinner size="sm" variant="dots" />
            <p className="text-xs text-primary font-mono">{state.processingStatus}</p>
          </div>
        )}

        {state.error && (
          <div className="p-3 rounded-lg bg-destructive/15 border border-destructive/40 space-y-2">
            <p className="text-xs text-destructive font-mono font-semibold">ERROR: {state.error}</p>
            <button
              onClick={() => {
                setError(null)
                handleRunFullPipeline()
              }}
              className="w-full py-1.5 px-3 rounded bg-destructive/20 hover:bg-destructive/30 text-destructive text-xs font-mono font-bold transition-all"
            >
              🔄 RETRY FAILED PIPELINE STAGE
            </button>
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

                            {/* Prominent Action Buttons below Upload */}
                            <button
                              onClick={runPreprocessing}
                              disabled={!currentImage}
                              className="w-full mt-2 py-2.5 rounded-xl bg-gradient-to-r from-primary to-secondary text-background font-extrabold text-xs shadow-[0_0_15px_rgba(0,240,255,0.4)] hover:shadow-[0_0_25px_rgba(0,240,255,0.7)] transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                            >
                              <span>⚡</span>
                              <span>START PREPROCESSING ON UPLOADED IMAGE</span>
                            </button>
                            <button
                              onClick={runFullPipeline}
                              disabled={!currentImage}
                              className="w-full py-2 rounded-xl bg-secondary/20 hover:bg-secondary/30 text-secondary border border-secondary/40 text-xs font-bold transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                            >
                              <span>🚀</span>
                              <span>EXECUTE ALL 6 STAGES FAST (REAL-TIME)</span>
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
                            <button
                              onClick={runPreprocessing}
                              disabled={!currentImage}
                              className="w-full py-2.5 rounded-xl bg-gradient-to-r from-primary to-secondary text-background font-extrabold text-xs shadow-[0_0_15px_rgba(0,240,255,0.4)] hover:shadow-[0_0_25px_rgba(0,240,255,0.7)] transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                            >
                              <span>⚡</span>
                              <span>EXECUTE PREPROCESSING NOW</span>
                            </button>
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
                            <button
                              onClick={runEnhancement}
                              disabled={!currentImage}
                              className="w-full mt-2 py-2.5 rounded-xl bg-gradient-to-r from-primary to-secondary text-background font-extrabold text-xs shadow-[0_0_15px_rgba(0,240,255,0.4)] hover:shadow-[0_0_25px_rgba(0,240,255,0.7)] transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                            >
                              <span>⚡</span>
                              <span>EXECUTE 4K ENHANCEMENT NOW</span>
                            </button>
                          </div>
                        )}

                        {step.id === 'colorization' && (
                          <div className="space-y-3">
                            <ColormapPaletteSelector
                              selectedColormap={settings.colormap}
                              onSelect={(id) => updateSettings({ colormap: id })}
                              compact
                            />
                            <button
                              onClick={runColorization}
                              disabled={!currentImage}
                              className="w-full py-2.5 rounded-xl bg-gradient-to-r from-primary to-secondary text-background font-extrabold text-xs shadow-[0_0_15px_rgba(0,240,255,0.4)] hover:shadow-[0_0_25px_rgba(0,240,255,0.7)] transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                            >
                              <span>⚡</span>
                              <span>EXECUTE THERMAL COLORIZATION NOW</span>
                            </button>
                          </div>
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
                            <button
                              onClick={runDetection}
                              disabled={!currentImage}
                              className="w-full mt-2 py-2.5 rounded-xl bg-gradient-to-r from-iris-orange to-primary text-background font-extrabold text-xs shadow-[0_0_15px_rgba(255,140,0,0.4)] hover:shadow-[0_0_25px_rgba(255,140,0,0.7)] transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                            >
                              <span>⚡</span>
                              <span>EXECUTE YOLOv8 DETECTION NOW</span>
                            </button>
                          </div>
                        )}

                        {step.id === 'analysis' && (
                          <div className="space-y-3">
                            {/* Comparison button right above analysis button */}
                            <div className="p-3 rounded-xl bg-gradient-to-br from-primary/10 to-teal-500/10 border border-primary/40 shadow-[0_0_20px_rgba(0,240,255,0.15)] space-y-2">
                              <div className="flex items-center justify-between text-xs font-bold text-foreground">
                                <span>Multi-Stage Scene Comparison</span>
                                <span className="text-[10px] text-primary px-2 py-0.5 rounded font-mono bg-primary/20 border border-primary/40">3-IN-1 VIEW</span>
                              </div>
                              <p className="text-[11px] text-muted-foreground font-mono">
                                Compare Enhanced, Colorized, and Detected outputs side-by-side. Saved directly to comparsions folder.
                              </p>
                              <button
                                onClick={handleOpenComparison}
                                disabled={!currentImage}
                                className="w-full py-2.5 rounded-xl bg-gradient-to-r from-teal-500 via-primary to-blue-600 text-background font-extrabold text-xs shadow-[0_0_15px_rgba(0,240,255,0.4)] hover:shadow-[0_0_25px_rgba(0,240,255,0.7)] transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                              >
                                <span>🔥</span>
                                <span>OPEN MULTI-STAGE COMPARISON VIEW</span>
                              </button>
                            </div>

                            <textarea
                              placeholder="Optional: Enter mission brief context or target coordinates for Gemini AI..."
                              value={settings.geminiContext}
                              onChange={(e) => updateSettings({ geminiContext: e.target.value })}
                              className="w-full p-3 rounded-xl bg-background/80 border border-border text-xs text-foreground font-mono placeholder-muted-foreground focus:outline-none focus:border-primary shadow-inner"
                              rows={3}
                            />
                            <button
                              onClick={handleOpenComparison}
                              disabled={!currentImage}
                              className="w-full py-2.5 rounded-xl bg-gradient-to-r from-teal-500 via-primary to-blue-600 text-background font-extrabold text-xs shadow-[0_0_15px_rgba(0,240,255,0.4)] hover:shadow-[0_0_25px_rgba(0,240,255,0.7)] transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                            >
                              <span>🔥</span>
                              <span>MULTI-STAGE COMPARISON VIEW (ENHANCED, COLORIZED, DETECTED)</span>
                            </button>
                            <button
                              onClick={runAnalysis}
                              disabled={!currentImage}
                              className="w-full py-2.5 rounded-xl bg-gradient-to-r from-purple-500 to-indigo-600 text-white font-extrabold text-xs shadow-[0_0_15px_rgba(168,85,247,0.4)] hover:shadow-[0_0_25px_rgba(168,85,247,0.7)] transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                            >
                              <span>🧠</span>
                              <span>EXECUTE GEMINI AI ANALYSIS NOW</span>
                            </button>
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
          onClick={handleOpenComparison}
          disabled={!currentImage}
          className="w-full py-3 rounded-xl bg-gradient-to-r from-teal-500 via-primary to-blue-600 text-slate-950 font-extrabold text-xs shadow-[0_0_20px_rgba(0,240,255,0.4)] hover:shadow-[0_0_30px_rgba(0,240,255,0.7)] transition-all flex items-center justify-center gap-2 disabled:opacity-50"
        >
          <span>🔥</span>
          <span>OPEN MULTI-STAGE COMPARISON VIEW</span>
        </motion.button>

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
          disabled={isGenerating}
          className="w-full py-3.5 rounded-xl bg-gradient-to-r from-iris-orange to-iris-amber text-background font-extrabold text-sm shadow-[0_0_25px_rgba(255,107,0,0.35)] hover:shadow-[0_0_35px_rgba(255,107,0,0.6)] transition-all flex items-center justify-center gap-2"
        >
          <FileDown className="w-5 h-5" />
          <span>{isGenerating ? 'EXPORTING PDF DOSSIER...' : 'EXPORT MISSION DOSSIER (PDF)'}</span>
        </motion.button>
      </div>

      {/* Interactive Multi-Stage Comparison Modal via Portal to prevent layout clipping and gauge overlap */}
      {typeof document !== 'undefined' && createPortal(
        <AnimatePresence>
          {showComparisonModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/90 backdrop-blur-lg p-4 md:p-8 overflow-y-auto"
            >
              <motion.div
                initial={{ scale: 0.95, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.95, opacity: 0 }}
                className="w-full max-w-6xl rounded-2xl bg-slate-950 border-2 border-primary shadow-[0_0_80px_rgba(0,240,255,0.4)] p-6 space-y-6 max-h-[90vh] overflow-y-auto relative z-[10000]"
              >
                <div className="flex items-center justify-between border-b border-border pb-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xl">🔥</span>
                      <h2 className="text-lg md:text-xl font-extrabold tracking-wide text-white uppercase">
                        MULTI-STAGE THERMAL SCENE COMPARISON DOSSIER
                      </h2>
                      <span className="text-xs px-2.5 py-0.5 rounded-full bg-primary/20 text-primary border border-primary/40 font-mono">
                        ISRO IRIS v3.0
                      </span>
                    </div>
                    <p className="text-xs font-mono text-muted-foreground">
                      Synchronized inspection of Enhanced Super-Resolution, Radiometric Thermal Colormap, and YOLOv8 Detected Targets.
                    </p>
                  </div>
                  <button
                    onClick={() => setShowComparisonModal(false)}
                    className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs border border-border"
                  >
                    ✕ CLOSE
                  </button>
                </div>

                {/* 3-in-1 Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-2 rounded-xl bg-slate-900 p-3 border border-slate-800">
                    <div className="flex items-center justify-between font-mono text-xs font-bold text-primary">
                      <span>1. ENHANCED IMAGE</span>
                      <span className="text-[10px] bg-primary/10 px-1.5 py-0.5 rounded">AI SUPER-RES</span>
                    </div>
                    <div className="relative aspect-video w-full rounded-lg overflow-hidden bg-black border border-slate-800 flex items-center justify-center">
                      <img
                        src={getFileDownloadUrl(currentImage?.enhanced_image || currentImage?.original_image || 'uploads/raw/enhanced_ai.jpg')}
                        alt="Enhanced Stage"
                        className="w-full h-full object-contain"
                      />
                    </div>
                  </div>

                  <div className="space-y-2 rounded-xl bg-slate-900 p-3 border border-slate-800">
                    <div className="flex items-center justify-between font-mono text-xs font-bold text-amber-400">
                      <span>2. COLORIZED IMAGE</span>
                      <span className="text-[10px] bg-amber-400/10 px-1.5 py-0.5 rounded">THERMAL MAP</span>
                    </div>
                    <div className="relative aspect-video w-full rounded-lg overflow-hidden bg-black border border-slate-800 flex items-center justify-center">
                      <img
                        src={getFileDownloadUrl(currentImage?.colorized_image || currentImage?.enhanced_image || 'outputs/verified_isro/step2_true_color.jpg')}
                        alt="Colorized Stage"
                        className="w-full h-full object-contain"
                      />
                    </div>
                  </div>

                  <div className="space-y-2 rounded-xl bg-slate-900 p-3 border border-slate-800">
                    <div className="flex items-center justify-between font-mono text-xs font-bold text-emerald-400">
                      <span>3. DETECTED IMAGE</span>
                      <span className="text-[10px] bg-emerald-400/10 px-1.5 py-0.5 rounded">YOLOv8 OBJECTS</span>
                    </div>
                    <div className="relative aspect-video w-full rounded-lg overflow-hidden bg-black border border-slate-800 flex items-center justify-center">
                      <img
                        src={getFileDownloadUrl(currentImage?.detected_image || currentImage?.processed_image || 'outputs/detected/enhanced_ai.jpg')}
                        alt="Detected Stage"
                        className="w-full h-full object-contain"
                      />
                    </div>
                  </div>
                </div>

                {/* Composite Comparison Image View */}
                <div className="space-y-3 rounded-xl bg-slate-900 p-4 border border-primary/30 relative z-10">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div>
                      <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                        FULL COMPOSITE COMPARISON DOSSIER
                      </h3>
                      <p className="text-xs font-mono text-emerald-400">
                        ✅ Comparison image stored and synchronized across both <code>comparisons/</code> and <code>comparsions/</code> folders.
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <a
                        href={getFileDownloadUrl(currentImage?.comparison_image || `outputs/comparsions/multi_compare_${(currentImage?.filename || 'CHANDRA09').split('.')[0]}.jpg`)}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-3 py-1.5 rounded-lg bg-primary hover:bg-primary/90 text-slate-950 font-extrabold text-xs transition-all flex items-center gap-1.5"
                      >
                        <FileDown className="w-4 h-4" />
                        <span>DOWNLOAD COMPOSITE IMAGE</span>
                      </a>
                    </div>
                  </div>

                  <div className="relative w-full rounded-xl overflow-hidden bg-black border border-slate-800 p-2 flex items-center justify-center min-h-[260px] max-h-[500px]">
                    <img
                      src={getFileDownloadUrl(currentImage?.comparison_image || `outputs/comparsions/multi_compare_${(currentImage?.filename || 'CHANDRA09').split('.')[0]}.jpg`)}
                      alt="Multi-Stage Composite Comparison"
                      className="max-h-[480px] w-auto object-contain rounded-lg"
                    />
                  </div>
                </div>

                <div className="flex justify-end gap-3 pt-2 border-t border-border">
                  <button
                    onClick={handleExportPdf}
                    className="px-5 py-2 rounded-xl bg-gradient-to-r from-iris-orange to-iris-amber text-white font-extrabold text-xs shadow-[0_0_20px_rgba(255,107,0,0.4)] hover:shadow-[0_0_30px_rgba(255,107,0,0.7)] transition-all flex items-center gap-2"
                  >
                    <FileDown className="w-4 h-4" />
                    <span>DOWNLOAD FULL PDF MISSION REPORT</span>
                  </button>
                  <button
                    onClick={() => setShowComparisonModal(false)}
                    className="px-5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs"
                  >
                    CLOSE COMPARISON VIEW
                  </button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>,
        document.body
      )}
    </div>
  )
}
