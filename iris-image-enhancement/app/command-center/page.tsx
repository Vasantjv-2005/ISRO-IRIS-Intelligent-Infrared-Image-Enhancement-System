'use client'

import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { AuthProvider } from '@/lib/context/AuthContext'
import { ImageProvider } from '@/lib/context/ImageContext'
import { PipelineProvider } from '@/lib/context/PipelineContext'
import { ViewProvider, useView, CommandView } from '@/lib/context/ViewContext'
import { Header } from '@/components/layout/Header'
import { PipelinePanel } from '@/components/layout/PipelinePanel'
import { WorkspaceViewport } from '@/components/visualization/WorkspaceViewport'
import { TacticalDashboard } from '@/components/dashboard/TacticalDashboard'
import { MissionDossierGallery } from '@/components/history/MissionDossierGallery'
import { GlassCard } from '@/components/ui/GlassCard'

export function IRISCommandCenter() {
  const { activeView } = useView()

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="pt-20 pb-12">
        <div className="mx-auto px-4 max-w-[1440px]">
          <AnimatePresence mode="wait">
            {activeView === 'workspace' && (
              <motion.div
                key="workspace"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.3 }}
              >
                {/* Workspace Title */}
                <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h2 className="text-2xl md:text-3xl font-extrabold text-foreground tracking-tight">
                      Neural Infrared Enhancement Studio
                    </h2>
                    <p className="text-sm text-muted-foreground">
                      Execute multi-stage AI super-resolution, thermal colormaps, YOLOv8 detection, and Gemini scene interpretation
                    </p>
                  </div>
                  <div className="flex items-center gap-2 font-mono text-xs text-primary bg-primary/10 border border-primary/30 px-3 py-1.5 rounded-lg self-start">
                    <span className="w-2 h-2 rounded-full bg-primary animate-ping" />
                    <span>CHANDRA-09 WORKSPACE ONLINE</span>
                  </div>
                </div>

                {/* Main Grid Layout */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                  {/* Left Panel - Controls */}
                  <div className="lg:col-span-3 xl:col-span-3">
                    <div className="sticky top-24">
                      <PipelinePanel />
                    </div>
                  </div>

                  {/* Right Panel - Visualization Viewport (NEURAL VISUALIZATION HUD) */}
                  <div className="lg:col-span-9 xl:col-span-9">
                    <WorkspaceViewport />
                  </div>
                </div>
              </motion.div>
            )}

            {activeView === 'dashboard' && (
              <motion.div
                key="dashboard"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.3 }}
              >
                <TacticalDashboard />
              </motion.div>
            )}

            {activeView === 'history' && (
              <motion.div
                key="history"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.3 }}
              >
                <MissionDossierGallery />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Global System Footer */}
          <footer className="mt-12 pt-6 border-t border-border/40">
            <GlassCard compact hover={false}>
              <div className="px-6 py-4 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs font-mono text-muted-foreground">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-green-400" />
                  <span>ISRO IRIS — CHANDRA-09 THERMAL INTERPRETATION SYSTEM // RUNNING ON LOCAL ENGINE 127.0.0.1:8000</span>
                </div>
                <div>
                  <span>HIGH-PRECISION RADIOMETRY & MULTIMODAL AI COMMAND CENTER</span>
                </div>
              </div>
            </GlassCard>
          </footer>
        </div>
      </main>
    </div>
  )
}

export default function CommandCenterPage({ initialView = 'workspace' }: { initialView?: CommandView }) {
  return (
    <AuthProvider>
      <ViewProvider initialView={initialView}>
        <ImageProvider>
          <PipelineProvider>
            <IRISCommandCenter />
          </PipelineProvider>
        </ImageProvider>
      </ViewProvider>
    </AuthProvider>
  )
}
