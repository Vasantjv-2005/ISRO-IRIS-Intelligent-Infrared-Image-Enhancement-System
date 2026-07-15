'use client'

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Satellite, Signal, Sparkles, Activity, LayoutGrid, History, ShieldCheck, LogOut } from 'lucide-react'
import { systemAPI } from '@/lib/api'
import { useView, CommandView } from '@/lib/context/ViewContext'
import { useImage } from '@/lib/context/ImageContext'
import { usePipeline } from '@/lib/context/PipelineContext'
import { useAuth } from '@/lib/context/AuthContext'
import { CHANDRA_09_DEMO_DATA } from '@/lib/demoData'

export function Header() {
  const { activeView, setActiveView } = useView()
  const { setCurrentImage } = useImage()
  const { markStepComplete } = usePipeline()
  const { logout } = useAuth()
  const [isHealthy, setIsHealthy] = useState(false)
  const [latency, setLatency] = useState(0)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const start = Date.now()
        await systemAPI.health()
        setLatency(Date.now() - start)
        setIsHealthy(true)
      } catch {
        setIsHealthy(false)
      }
    }

    checkHealth()
    const interval = setInterval(checkHealth, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleLoadDemoFeed = () => {
    setCurrentImage(CHANDRA_09_DEMO_DATA)
    markStepComplete('upload')
    markStepComplete('preprocessing')
    markStepComplete('enhancement')
    markStepComplete('colorization')
    markStepComplete('detection')
    markStepComplete('analysis')
    setActiveView('workspace')
  }

  const navItems: { label: string; view: CommandView; icon: React.ReactNode }[] = [
    { label: 'Neural Workspace', view: 'workspace', icon: <Activity className="w-3.5 h-3.5" /> },
    { label: 'Tactical Command', view: 'dashboard', icon: <LayoutGrid className="w-3.5 h-3.5" /> },
    { label: 'Mission Dossiers', view: 'history', icon: <History className="w-3.5 h-3.5" /> },
  ]

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-primary/25 bg-background/85 backdrop-blur-2xl shadow-[0_4px_30px_rgba(0,0,0,0.65)]">
      <div className="flex items-center justify-between px-6 py-3">
        {/* Left: Branding & Orbital Radar Emblem with ISRO IRIS Logo Image */}
        <motion.div
          className="flex items-center gap-3.5 cursor-pointer group"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          onClick={() => setActiveView('workspace')}
        >
          <div className="relative flex items-center justify-center w-12 h-12 rounded-xl overflow-hidden bg-gradient-to-br from-primary/30 via-primary/10 to-secondary/20 border border-primary/50 shadow-[0_0_25px_rgba(0,240,255,0.4)] group-hover:shadow-[0_0_35px_rgba(0,240,255,0.7)] transition-all">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 10, repeat: Infinity, ease: 'linear' }}
              className="absolute inset-0 rounded-xl border border-dashed border-primary/50 pointer-events-none z-10"
            />
            <img 
              src="/isro-logo.jpg" 
              alt="ISRO IRIS Emblem" 
              className="w-10 h-10 rounded-lg object-cover z-0 group-hover:scale-105 transition-transform duration-300" 
            />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-extrabold tracking-tight bg-gradient-to-r from-primary via-teal-300 to-white bg-clip-text text-transparent">
                ISRO IRIS
              </h1>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider bg-primary/20 text-primary border border-primary/40 shadow-[0_0_10px_rgba(0,240,255,0.2)]">
                CHANDRA-09
              </span>
            </div>
            <p className="text-[11px] font-medium text-muted-foreground tracking-wide">
              INTELLIGENT INFRARED INTERPRETATION SYSTEM
            </p>
          </div>
        </motion.div>

        {/* Center: Aerospace Navigation Tabs */}
        <nav className="hidden md:flex items-center gap-1.5 p-1 rounded-xl bg-card/70 border border-border/80 backdrop-blur-md shadow-inner">
          {navItems.map((item) => {
            const isActive = activeView === item.view
            return (
              <button
                key={item.view}
                onClick={() => setActiveView(item.view)}
                className={`relative flex items-center gap-2 px-4 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all ${
                  isActive
                    ? 'bg-gradient-to-r from-primary/25 to-secondary/20 text-primary border border-primary/50 shadow-[0_0_15px_rgba(0,240,255,0.25)]'
                    : 'text-muted-foreground hover:text-foreground hover:bg-primary/5'
                }`}
              >
                {item.icon}
                <span>{item.label}</span>
                {isActive && (
                  <motion.span
                    layoutId="activeTabGlow"
                    className="absolute -bottom-1 left-3 right-3 h-0.5 bg-gradient-to-r from-primary to-secondary rounded-full shadow-[0_0_8px_rgba(0,240,255,0.8)]"
                  />
                )}
              </button>
            )
          })}
        </nav>

        {/* Right: Actions & Telemetry Status */}
        <div className="flex items-center gap-3">
          {/* Load Sample Feed Action */}
          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            onClick={handleLoadDemoFeed}
            className="hidden sm:flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold font-mono tracking-wider bg-gradient-to-r from-primary/20 via-teal-400/10 to-secondary/20 text-primary border border-primary/50 shadow-[0_0_15px_rgba(0,240,255,0.2)] hover:shadow-[0_0_25px_rgba(0,240,255,0.5)] transition-all"
          >
            <Sparkles className="w-3.5 h-3.5 text-primary animate-pulse" />
            <span>⚡ LOAD CHANDRA-09 SAMPLE</span>
          </motion.button>

          {/* System Telemetry Status */}
          <motion.div className="flex items-center gap-2" whileHover={{ scale: 1.03 }}>
            <div
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-mono font-semibold shadow-sm ${
                isHealthy
                  ? 'bg-green-500/15 text-green-400 border border-green-500/40 shadow-[0_0_12px_rgba(34,197,94,0.2)]'
                  : 'bg-primary/15 text-primary border border-primary/40 shadow-[0_0_12px_rgba(0,240,255,0.2)]'
              }`}
            >
              <motion.div
                className="w-2 h-2 rounded-full bg-primary status-pulse"
                animate={{ scale: [1, 1.3, 1] }}
                transition={{ duration: 1.8, repeat: Infinity }}
              />
              <Signal className="w-3.5 h-3.5" />
              <span>{latency > 0 ? `TELEMETRY ${latency}ms` : 'RADAR SYNCED'}</span>
            </div>
          </motion.div>

          {/* Quick Logout Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
              logout()
              window.location.href = '/login'
            }}
            title="Terminate Session / Logout"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-destructive/15 hover:bg-destructive/30 text-destructive border border-destructive/40 transition-all shadow-[0_0_10px_rgba(239,68,68,0.2)]"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span className="hidden xl:inline">LOGOUT</span>
          </motion.button>
        </div>
      </div>
    </header>
  )
}
