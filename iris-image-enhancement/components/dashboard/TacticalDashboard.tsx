'use client'

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import {
  Satellite,
  Activity,
  Target,
  TrendingUp,
  Cpu,
  Radio,
  Sparkles,
  ArrowRight,
  Database,
  Layers,
} from 'lucide-react'
import { GlassCard } from '@/components/ui/GlassCard'
import { Badge } from '@/components/ui/Badge'
import { useView } from '@/lib/context/ViewContext'
import { useImage } from '@/lib/context/ImageContext'
import { CHANDRA_09_DEMO_DATA } from '@/lib/demoData'

const telemetryData = [
  { band: 'SWIR 1.4µm', raw: 24.2, enhanced: 33.8, gain: '+9.6 dB', ssim: 0.88 },
  { band: 'MWIR 3.4µm', raw: 27.5, enhanced: 36.4, gain: '+8.9 dB', ssim: 0.92 },
  { band: 'MWIR 4.8µm', raw: 28.1, enhanced: 38.1, gain: '+10.0 dB', ssim: 0.94 },
  { band: 'LWIR 8.4µm', raw: 30.0, enhanced: 38.4, gain: '+8.4 dB', ssim: 0.942 },
  { band: 'LWIR 11.2µm', raw: 29.4, enhanced: 37.9, gain: '+8.5 dB', ssim: 0.93 },
  { band: 'Far-IR 14µm', raw: 26.8, enhanced: 35.6, gain: '+8.8 dB', ssim: 0.91 },
]

const recentAnalyses = [
  {
    id: 'T-8842',
    sector: 'Chandra-09 Lunar South Ridge',
    timestamp: '2 mins ago',
    resolution: '3840x2160 (16-bit TIFF)',
    psnrGain: '+8.42 dB',
    targets: 4,
    status: 'COMPLETED',
  },
  {
    id: 'T-8839',
    sector: 'Orbital Thermal Array Delta-4',
    timestamp: '18 mins ago',
    resolution: '2048x2048 (MWIR Feed)',
    psnrGain: '+7.85 dB',
    targets: 6,
    status: 'COMPLETED',
  },
  {
    id: 'T-8834',
    sector: 'Deep Space Cryo-Plume Capture',
    timestamp: '42 mins ago',
    resolution: '4096x4096 (LWIR Radiometric)',
    psnrGain: '+9.14 dB',
    targets: 2,
    status: 'ARCHIVED',
  },
]

export function TacticalDashboard() {
  const { setActiveView } = useView()
  const { setCurrentImage } = useImage()
  const [hoveredBandIndex, setHoveredBandIndex] = useState<number | null>(null)

  const handleLaunchSample = () => {
    setCurrentImage(CHANDRA_09_DEMO_DATA)
    setActiveView('workspace')
  }

  // Generate SVG coordinates for 6 points between X=40 and X=600, Y=20 to Y=180
  // Value range 15 to 45 -> Y = 180 - ((val - 15) / 30) * 160
  const getX = (i: number) => 50 + i * 110
  const getY = (val: number) => 190 - ((val - 15) / 30) * 160

  const enhancedPoints = telemetryData.map((d, idx) => `${getX(idx)},${getY(d.enhanced)}`).join(' ')
  const rawPoints = telemetryData.map((d, idx) => `${getX(idx)},${getY(d.raw)}`).join(' ')

  const enhancedArea = `M 50,190 L ${enhancedPoints} L 600,190 Z`
  const rawArea = `M 50,190 L ${rawPoints} L 600,190 Z`

  return (
    <div className="space-y-6">
      {/* Top Banner HUD */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative overflow-hidden rounded-2xl border border-primary/40 bg-gradient-to-r from-card/90 via-navy/80 to-card/90 p-6 shadow-[0_0_40px_rgba(0,240,255,0.15)] backdrop-blur-2xl"
      >
        <div className="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-primary/10 blur-3xl pointer-events-none" />
        <div className="absolute -left-20 -bottom-20 h-64 w-64 rounded-full bg-accent/10 blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-primary/20 text-primary border border-primary/40 flex items-center gap-1.5">
                <Radio className="w-3 h-3 animate-pulse" />
                ISRO TELEMETRY DOWNLINK ACTIVE
              </span>
              <span className="text-xs font-mono text-muted-foreground">MISSION CODE: IRIS-CHANDRA09</span>
            </div>
            <h2 className="text-2xl md:text-3xl font-extrabold text-foreground tracking-tight">
              Tactical Deep-Space Infrared Command HUD
            </h2>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Real-time radiometric telemetry monitoring, AI super-resolution performance analytics, and object classification across ISRO orbital thermal sensors.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full md:w-auto">
            <motion.button
              whileHover={{ scale: 1.04 }}
              whileTap={{ scale: 0.96 }}
              onClick={handleLaunchSample}
              className="px-5 py-3 rounded-xl bg-gradient-to-r from-primary via-teal-300 to-secondary text-background font-extrabold text-sm shadow-[0_0_25px_rgba(0,240,255,0.4)] hover:shadow-[0_0_35px_rgba(0,240,255,0.7)] flex items-center justify-center gap-2"
            >
              <Sparkles className="w-4 h-4" />
              <span>Launch Neural Workspace</span>
              <ArrowRight className="w-4 h-4" />
            </motion.button>
          </div>
        </div>
      </motion.div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          {
            title: 'Thermal Captures Processed',
            value: '1,428',
            change: '+24 today',
            icon: <Database className="w-5 h-5 text-primary" />,
            borderColor: 'hover:border-primary/60',
            glowColor: 'group-hover:shadow-[0_0_25px_rgba(0,240,255,0.2)]',
          },
          {
            title: 'YOLOv8 Targets Tracked',
            value: '3,892',
            change: '98.4% precision',
            icon: <Target className="w-5 h-5 text-iris-orange" />,
            borderColor: 'hover:border-iris-orange/60',
            glowColor: 'group-hover:shadow-[0_0_25px_rgba(255,107,0,0.2)]',
          },
          {
            title: 'Super-Resolution PSNR Gain',
            value: '+8.42 dB',
            change: '4x Upsampling',
            icon: <TrendingUp className="w-5 h-5 text-secondary" />,
            borderColor: 'hover:border-secondary/60',
            glowColor: 'group-hover:shadow-[0_0_25px_rgba(0,210,180,0.2)]',
          },
          {
            title: 'Mean Structural Similarity',
            value: '0.941 SSIM',
            change: 'Radiometric Fidelity',
            icon: <Layers className="w-5 h-5 text-accent" />,
            borderColor: 'hover:border-accent/60',
            glowColor: 'group-hover:shadow-[0_0_25px_rgba(224,30,121,0.2)]',
          },
        ].map((kpi, idx) => (
          <motion.div
            key={kpi.title}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + idx * 0.08 }}
            className="group"
          >
            <GlassCard className={`p-5 transition-all duration-300 ${kpi.borderColor} ${kpi.glowColor}`}>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  {kpi.title}
                </span>
                <div className="p-2.5 rounded-xl bg-background/70 border border-border/80">
                  {kpi.icon}
                </div>
              </div>
              <div className="flex items-baseline justify-between">
                <h3 className="text-2xl font-mono font-extrabold text-foreground tracking-tight">
                  {kpi.value}
                </h3>
                <span className="text-xs font-mono text-secondary font-bold bg-secondary/15 px-2 py-0.5 rounded border border-secondary/30">
                  {kpi.change}
                </span>
              </div>
            </GlassCard>
          </motion.div>
        ))}
      </div>

      {/* Main Charts & Orbital Telemetry Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Custom Aerospace Spectral Band Super-Resolution Chart */}
        <motion.div
          initial={{ opacity: 0, x: -15 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="lg:col-span-8"
        >
          <GlassCard className="p-6 h-full flex flex-col justify-between">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
              <div>
                <h3 className="text-base font-bold text-foreground flex items-center gap-2">
                  <Activity className="w-4 h-4 text-primary" />
                  AI Super-Resolution Gain Across Infrared Spectral Bands
                </h3>
                <p className="text-xs text-muted-foreground">
                  Comparison of raw sensor PSNR (dB) vs Deep Residual AI enhanced PSNR (dB)
                </p>
              </div>
              <div className="flex items-center gap-3 text-xs font-mono">
                <div className="flex items-center gap-1.5">
                  <span className="w-3 h-3 rounded bg-primary inline-block shadow-[0_0_8px_#00F0FF]" />
                  <span>AI Enhanced PSNR</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-3 h-3 rounded bg-slate-500 inline-block" />
                  <span>Raw Sensor Feed</span>
                </div>
              </div>
            </div>

            {/* Futuristic Custom Interactive SVG Chart */}
            <div className="relative w-full overflow-x-auto py-2">
              <svg viewBox="0 0 650 220" className="w-full h-64 select-none">
                <defs>
                  <linearGradient id="neonCyanArea" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#00F0FF" stopOpacity="0.45" />
                    <stop offset="100%" stopColor="#00F0FF" stopOpacity="0.02" />
                  </linearGradient>
                  <linearGradient id="rawGrayArea" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#64748B" stopOpacity="0.3" />
                    <stop offset="100%" stopColor="#64748B" stopOpacity="0.02" />
                  </linearGradient>
                </defs>

                {/* Grid horizontal lines */}
                {[20, 60, 100, 140, 180].map((y, idx) => (
                  <line
                    key={y}
                    x1="45"
                    y1={y}
                    x2="615"
                    y2={y}
                    stroke="rgba(0, 240, 255, 0.12)"
                    strokeDasharray="4,4"
                  />
                ))}

                {/* Y Axis labels */}
                <text x="12" y="24" fill="#94A3B8" fontSize="10" fontFamily="monospace">45 dB</text>
                <text x="12" y="104" fill="#94A3B8" fontSize="10" fontFamily="monospace">35 dB</text>
                <text x="12" y="184" fill="#94A3B8" fontSize="10" fontFamily="monospace">15 dB</text>

                {/* Raw Sensor Area & Line */}
                <path d={rawArea} fill="url(#rawGrayArea)" />
                <polyline
                  fill="none"
                  stroke="#64748B"
                  strokeWidth="2"
                  points={rawPoints}
                />

                {/* AI Enhanced Area & Line */}
                <path d={enhancedArea} fill="url(#neonCyanArea)" />
                <polyline
                  fill="none"
                  stroke="#00F0FF"
                  strokeWidth="3"
                  points={enhancedPoints}
                />

                {/* Data points & X Axis labels */}
                {telemetryData.map((d, idx) => {
                  const x = getX(idx)
                  const yEnhanced = getY(d.enhanced)
                  const yRaw = getY(d.raw)
                  const isHovered = hoveredBandIndex === idx

                  return (
                    <g key={d.band} className="cursor-pointer" onMouseEnter={() => setHoveredBandIndex(idx)}>
                      {/* X Axis Label */}
                      <text
                        x={x}
                        y="208"
                        textAnchor="middle"
                        fill={isHovered ? '#00F0FF' : '#94A3B8'}
                        fontSize="10"
                        fontFamily="monospace"
                        fontWeight={isHovered ? 'bold' : 'normal'}
                      >
                        {d.band}
                      </text>

                      {/* Raw Point */}
                      <circle cx={x} cy={yRaw} r="3.5" fill="#64748B" />

                      {/* Enhanced Point */}
                      <circle
                        cx={x}
                        cy={yEnhanced}
                        r={isHovered ? '7' : '5'}
                        fill="#00F0FF"
                        stroke="#0B0E14"
                        strokeWidth="2"
                      />

                      {/* Hover guideline */}
                      {isHovered && (
                        <line
                          x1={x}
                          y1="20"
                          x2={x}
                          y2="190"
                          stroke="#00F0FF"
                          strokeWidth="1"
                          strokeDasharray="2,2"
                        />
                      )}
                    </g>
                  )
                })}
              </svg>

              {/* Hover Tooltip Banner */}
              {hoveredBandIndex !== null && (
                <motion.div
                  initial={{ opacity: 0, y: -4 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-2 p-3 rounded-xl bg-background/90 border border-primary/50 flex flex-wrap items-center justify-between text-xs font-mono shadow-lg"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-primary font-bold">
                      {telemetryData[hoveredBandIndex].band}
                    </span>
                    <span className="text-muted-foreground">|</span>
                    <span>Raw: {telemetryData[hoveredBandIndex].raw} dB</span>
                    <span className="text-muted-foreground">→</span>
                    <span className="text-primary font-bold">
                      Enhanced: {telemetryData[hoveredBandIndex].enhanced} dB
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-secondary font-bold">
                      Gain: {telemetryData[hoveredBandIndex].gain}
                    </span>
                    <span className="text-accent font-bold">
                      SSIM: {telemetryData[hoveredBandIndex].ssim}
                    </span>
                  </div>
                </motion.div>
              )}
            </div>
          </GlassCard>
        </motion.div>

        {/* Right: Orbital Telemetry & Sensor Array Status */}
        <motion.div
          initial={{ opacity: 0, x: 15 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.25 }}
          className="lg:col-span-4"
        >
          <GlassCard className="p-6 h-full flex flex-col justify-between space-y-5">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold uppercase tracking-wider text-foreground flex items-center gap-2">
                  <Satellite className="w-4 h-4 text-secondary" />
                  Orbital Array Telemetry
                </h3>
                <Badge variant="success" size="sm">NOMINAL</Badge>
              </div>

              {/* Orbital Radar Graphic */}
              <div className="relative flex items-center justify-center h-36 rounded-xl border border-primary/25 bg-background/70 overflow-hidden mb-4">
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 8, repeat: Infinity, ease: 'linear' }}
                  className="absolute inset-4 rounded-full border border-dashed border-primary/40"
                />
                <motion.div
                  animate={{ rotate: -360 }}
                  transition={{ duration: 16, repeat: Infinity, ease: 'linear' }}
                  className="absolute inset-8 rounded-full border border-secondary/30"
                />
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-2.5 h-2.5 rounded-full bg-primary shadow-[0_0_12px_#00F0FF] animate-ping" />
                </div>
                <div className="absolute bottom-2 left-3 right-3 flex justify-between text-[10px] font-mono text-primary">
                  <span>ALT: 540 KM</span>
                  <span>SYNC: 100%</span>
                </div>
              </div>

              {/* Sensor Diagnostics */}
              <div className="space-y-3 font-mono text-xs">
                <div className="flex justify-between items-center py-1.5 border-b border-border/60">
                  <span className="text-muted-foreground">LWIR Sensor Array</span>
                  <span className="text-green-400 font-bold">CRYOGENIC 77K</span>
                </div>
                <div className="flex justify-between items-center py-1.5 border-b border-border/60">
                  <span className="text-muted-foreground">Downlink Bandwidth</span>
                  <span className="text-primary font-bold">1.24 GB/sec</span>
                </div>
                <div className="flex justify-between items-center py-1.5 border-b border-border/60">
                  <span className="text-muted-foreground">Neural Engine Status</span>
                  <span className="text-secondary font-bold">YOLOv8 + GEMINI LIVE</span>
                </div>
                <div className="flex justify-between items-center py-1.5">
                  <span className="text-muted-foreground">Colormap Resolution</span>
                  <span className="text-foreground font-bold">16-BIT HDR</span>
                </div>
              </div>
            </div>

            <button
              onClick={handleLaunchSample}
              className="w-full py-2.5 rounded-xl bg-primary/15 text-primary border border-primary/40 text-xs font-mono font-bold hover:bg-primary/25 transition-all shadow-[0_0_15px_rgba(0,240,255,0.15)]"
            >
              INSPECT CHANDRA-09 FEED
            </button>
          </GlassCard>
        </motion.div>
      </div>

      {/* Recent Mission Telemetry Log */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <GlassCard className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-foreground flex items-center gap-2">
              <Cpu className="w-4 h-4 text-accent" />
              Recent Infrared Mission Analyses
            </h3>
            <span className="text-xs font-mono text-muted-foreground">SYNCED WITH MONGODB TELEMETRY</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {recentAnalyses.map((item) => (
              <div
                key={item.id}
                onClick={handleLaunchSample}
                className="p-4 rounded-xl bg-background/60 border border-border/80 hover:border-primary/60 hover:shadow-[0_0_20px_rgba(0,240,255,0.15)] transition-all cursor-pointer group"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono font-bold text-xs text-primary">{item.id}</span>
                  <span className="text-[10px] font-mono text-muted-foreground">{item.timestamp}</span>
                </div>
                <h4 className="text-sm font-semibold text-foreground mb-1 group-hover:text-primary transition-colors">
                  {item.sector}
                </h4>
                <p className="text-xs text-muted-foreground mb-3">{item.resolution}</p>
                <div className="flex items-center justify-between pt-2 border-t border-border/60 text-xs font-mono">
                  <span className="text-secondary font-bold">Gain: {item.psnrGain}</span>
                  <span className="px-2 py-0.5 rounded bg-primary/10 text-primary">
                    {item.targets} Targets
                  </span>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </motion.div>
    </div>
  )
}
