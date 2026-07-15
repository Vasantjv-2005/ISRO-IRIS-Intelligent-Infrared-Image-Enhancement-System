'use client'

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'
import {
  Satellite,
  Sparkles,
  ShieldCheck,
  Cpu,
  Radio,
  Eye,
  TrendingUp,
  Database,
  ArrowRight,
  CheckCircle2,
  Zap,
  Activity,
  Terminal,
  Globe,
  Lock,
  FileText
} from 'lucide-react'
import { GlassCard } from '@/components/ui/GlassCard'
import { Badge } from '@/components/ui/Badge'

export default function HomePage() {
  const [mounted, setMounted] = useState(false)
  const [activeTab, setActiveTab] = useState<'architecture' | 'superres' | 'detection' | 'radiometry'>('architecture')

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return (
    <div className="min-h-screen bg-background text-foreground overflow-x-hidden selection:bg-primary/30 selection:text-primary">
      {/* Background Ambient Glow & Cyber Grid */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-primary/10 rounded-full blur-[140px] animate-pulse" />
        <div className="absolute bottom-1/3 right-10 w-[500px] h-[500px] bg-secondary/10 rounded-full blur-[130px]" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#00f0ff08_1px,transparent_1px),linear-gradient(to_bottom,#00f0ff08_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]" />
      </div>

      {/* Navigation Header with ISRO IRIS Logo Beside Title */}
      <header className="fixed top-0 left-0 right-0 z-50 border-b border-primary/25 bg-background/85 backdrop-blur-2xl shadow-[0_4px_30px_rgba(0,0,0,0.65)]">
        <div className="mx-auto max-w-[1440px] px-6 py-3.5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3.5 group">
            <div className="relative flex items-center justify-center w-12 h-12 rounded-xl overflow-hidden bg-gradient-to-br from-primary/30 via-primary/10 to-secondary/20 border border-primary/50 shadow-[0_0_25px_rgba(0,240,255,0.4)] group-hover:shadow-[0_0_35px_rgba(0,240,255,0.7)] transition-all">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 12, repeat: Infinity, ease: 'linear' }}
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
                <h1 className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-primary via-teal-300 to-white bg-clip-text text-transparent">
                  ISRO IRIS
                </h1>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider bg-primary/20 text-primary border border-primary/40 shadow-[0_0_10px_rgba(0,240,255,0.2)]">
                  CHANDRA-09
                </span>
              </div>
              <p className="text-[11px] font-medium text-muted-foreground tracking-wide">
                INDIGENOUS RISC-V CONTROLLER FOR SPACE APPLICATIONS
              </p>
            </div>
          </Link>

          {/* Quick Nav */}
          <nav className="hidden md:flex items-center gap-6 text-xs font-mono font-semibold text-muted-foreground">
            <a href="#hero" className="hover:text-primary transition-colors">// MISSION OVERVIEW</a>
            <a href="#technical-briefing" className="hover:text-primary transition-colors">// SYSTEM TELEMETRY</a>
            <a href="#capabilities" className="hover:text-primary transition-colors">// AI WORKFLOW</a>
          </nav>

          {/* Login / Mission Access CTA */}
          <div className="flex items-center gap-3">
            <Link href="/login">
              <motion.button
                whileHover={{ scale: 1.04 }}
                whileTap={{ scale: 0.96 }}
                className="px-5 py-2.5 rounded-xl font-mono text-xs font-bold tracking-wider bg-gradient-to-r from-primary to-secondary text-background hover:shadow-[0_0_25px_rgba(0,240,255,0.6)] transition-all flex items-center gap-2 border border-primary/50"
              >
                <Lock className="w-3.5 h-3.5" />
                <span>MISSION ACCESS // LOGIN</span>
              </motion.button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section Featuring The ISRO IRIS Picture */}
      <section id="hero" className="relative pt-32 pb-20 px-6 max-w-[1440px] mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Hero Copy */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="lg:col-span-7 space-y-6"
          >
            <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full bg-primary/10 border border-primary/40 text-primary text-xs font-mono font-bold shadow-[0_0_20px_rgba(0,240,255,0.2)]">
              <span className="w-2 h-2 rounded-full bg-primary animate-ping" />
              <span>ISRO DEEP SPACE RESEARCH // INDIGENOUS RISC-V ARCHITECTURE</span>
            </div>

            <h2 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.15] text-foreground">
              Intelligent Infrared Image{' '}
              <span className="bg-gradient-to-r from-primary via-teal-300 to-secondary bg-clip-text text-transparent">
                Enhancement & Interpretation
              </span>
            </h2>

            <p className="text-base sm:text-lg text-muted-foreground leading-relaxed max-w-2xl font-sans">
              Engineered for the <b>Chandra-09 Lunar and Deep Space Orbital Program</b>, the ISRO IRIS framework combines 
              radiation-hardened <b>Indigenous RISC-V processors</b> with multi-modal AI neural engines. Experience 
              real-time thermal super-resolution, multi-spectral radiometric colormaps, YOLOv8 target classification, and 
              automated Gemini executive briefings.
            </p>

            {/* Quick Metrics Banner */}
            <div className="grid grid-cols-3 gap-4 pt-4 border-t border-border/50 max-w-xl">
              <div className="p-3.5 rounded-xl bg-card/60 border border-border/60 backdrop-blur-md">
                <div className="text-xs font-mono text-muted-foreground uppercase">PSNR GAIN</div>
                <div className="text-2xl font-extrabold font-mono text-primary mt-1">+10.0 dB</div>
              </div>
              <div className="p-3.5 rounded-xl bg-card/60 border border-border/60 backdrop-blur-md">
                <div className="text-xs font-mono text-muted-foreground uppercase">RADIOMETRY</div>
                <div className="text-2xl font-extrabold font-mono text-emerald-400 mt-1">16-Bit UHD</div>
              </div>
              <div className="p-3.5 rounded-xl bg-card/60 border border-border/60 backdrop-blur-md">
                <div className="text-xs font-mono text-muted-foreground uppercase">LATENCY</div>
                <div className="text-2xl font-extrabold font-mono text-secondary mt-1">&lt; 18 ms</div>
              </div>
            </div>

            {/* CTA Actions */}
            <div className="flex flex-wrap items-center gap-4 pt-4">
              <Link href="/login">
                <motion.button
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.97 }}
                  className="px-8 py-4 rounded-xl font-mono text-sm font-bold tracking-wider bg-gradient-to-r from-primary via-teal-400 to-secondary text-background shadow-[0_0_30px_rgba(0,240,255,0.5)] hover:shadow-[0_0_45px_rgba(0,240,255,0.8)] transition-all flex items-center gap-3"
                >
                  <Terminal className="w-5 h-5" />
                  <span>LAUNCH COMMAND CENTER</span>
                  <ArrowRight className="w-4 h-4" />
                </motion.button>
              </Link>

              <a href="#technical-briefing">
                <button className="px-6 py-4 rounded-xl font-mono text-sm font-bold tracking-wider bg-card/80 hover:bg-card text-foreground border border-border/80 hover:border-primary/50 transition-all flex items-center gap-2">
                  <FileText className="w-4 h-4 text-primary" />
                  <span>READ SYSTEM DOSSIER</span>
                </button>
              </a>
            </div>
          </motion.div>

          {/* Right Hero Image Showcase: The ISRO IRIS Picture */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, delay: 0.2 }}
            className="lg:col-span-5 relative flex items-center justify-center"
          >
            <div className="relative w-full max-w-[520px] aspect-square flex items-center justify-center">
              {/* Orbital Ring Effects */}
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 30, repeat: Infinity, ease: 'linear' }}
                className="absolute inset-0 rounded-full border border-dashed border-primary/30 pointer-events-none"
              />
              <motion.div
                animate={{ rotate: -360 }}
                transition={{ duration: 40, repeat: Infinity, ease: 'linear' }}
                className="absolute inset-6 rounded-full border border-secondary/20 pointer-events-none"
              />
              <div className="absolute inset-12 rounded-full bg-gradient-to-tr from-primary/20 via-transparent to-secondary/20 blur-2xl pointer-events-none" />

              {/* Main Glowing Picture Frame */}
              <div className="relative z-10 p-3 rounded-3xl bg-gradient-to-br from-primary/40 via-teal-500/20 to-secondary/40 border border-primary/60 shadow-[0_0_60px_rgba(0,240,255,0.35)] backdrop-blur-xl group">
                <div className="relative rounded-2xl overflow-hidden bg-black/80 aspect-square w-[380px] sm:w-[440px]">
                  <img
                    src="/isro-logo.jpg"
                    alt="ISRO IRIS System Emblem"
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                  />
                  {/* Subtle HUD Overlay */}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/20 flex flex-col justify-between p-5 pointer-events-none">
                    <div className="flex items-center justify-between">
                      <span className="px-2.5 py-1 rounded bg-black/80 border border-primary/50 text-[10px] font-mono text-primary font-bold shadow-sm">
                        🛰️ RADAR PAYLOAD SYNCED
                      </span>
                      <span className="px-2.5 py-1 rounded bg-black/80 border border-emerald-500/50 text-[10px] font-mono text-emerald-400 font-bold">
                        RISC-V CORE OK
                      </span>
                    </div>
                    <div>
                      <div className="text-[11px] font-mono font-bold text-white bg-black/80 backdrop-blur-md px-3 py-1.5 rounded-lg border border-border/80 inline-block">
                        ISRO IRIS // INDIGENOUS RISC-V ARCHITECTURE
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Floating Telemetry Badge Left */}
              <motion.div
                animate={{ y: [-6, 6, -6] }}
                transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
                className="absolute -left-4 sm:-left-8 top-16 z-20 p-3 rounded-xl bg-slate-950/90 border border-primary/50 shadow-[0_0_20px_rgba(0,240,255,0.3)] backdrop-blur-md hidden sm:flex items-center gap-3"
              >
                <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center text-primary">
                  <Cpu className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-[10px] font-mono text-muted-foreground">SOC ARCHITECTURE</div>
                  <div className="text-xs font-mono font-bold text-foreground">RISC-V 64-Bit Local</div>
                </div>
              </motion.div>

              {/* Floating Telemetry Badge Right */}
              <motion.div
                animate={{ y: [6, -6, 6] }}
                transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}
                className="absolute -right-4 sm:-right-8 bottom-16 z-20 p-3 rounded-xl bg-slate-950/90 border border-emerald-500/50 shadow-[0_0_20px_rgba(16,185,129,0.3)] backdrop-blur-md hidden sm:flex items-center gap-3"
              >
                <div className="w-8 h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                  <Activity className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-[10px] font-mono text-muted-foreground">SSIM FIDELITY</div>
                  <div className="text-xs font-mono font-bold text-emerald-400">0.942 Radiometric</div>
                </div>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Generated Technical Text Section Below The Hero Image */}
      <section id="technical-briefing" className="py-20 px-6 max-w-[1440px] mx-auto border-t border-border/40">
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
          <Badge variant="primary" className="font-mono text-xs">
            TECHNICAL DOSSIER & GENERATED BRIEFING
          </Badge>
          <h3 className="text-3xl sm:text-4xl font-extrabold text-foreground tracking-tight">
            System Architecture & Deep Space Radiometry
          </h3>
          <p className="text-sm text-muted-foreground font-sans">
            Comprehensive technical briefing on the ISRO IRIS multi-stage AI enhancement pipeline, indigenous hardware capabilities, and mission-critical interpretations.
          </p>
        </div>

        {/* Interactive Briefing Selector */}
        <div className="flex flex-wrap items-center justify-center gap-3 mb-10">
          {[
            { id: 'architecture', label: '1. Indigenous RISC-V Controller', icon: <Cpu className="w-4 h-4" /> },
            { id: 'superres', label: '2. Multi-Stage AI Super-Resolution', icon: <Sparkles className="w-4 h-4" /> },
            { id: 'detection', label: '3. YOLOv8 & Gemini Neural Engine', icon: <Eye className="w-4 h-4" /> },
            { id: 'radiometry', label: '4. Radiometric SWIR/MWIR/LWIR', icon: <Radio className="w-4 h-4" /> },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-5 py-3 rounded-xl font-mono text-xs font-bold transition-all flex items-center gap-2 border ${
                activeTab === tab.id
                  ? 'bg-primary/20 border-primary text-primary shadow-[0_0_20px_rgba(0,240,255,0.3)]'
                  : 'bg-card/60 border-border text-muted-foreground hover:text-foreground hover:bg-card'
              }`}
            >
              {tab.icon}
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Generated Text Content Display */}
        <div className="max-w-5xl mx-auto">
          <AnimatePresence mode="wait">
            {activeTab === 'architecture' && (
              <motion.div
                key="architecture"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.3 }}
              >
                <GlassCard className="p-8 sm:p-10 border-primary/40 shadow-2xl relative overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
                  <div className="absolute top-0 right-0 w-80 h-80 bg-primary/10 rounded-full blur-3xl pointer-events-none" />
                  <div className="flex items-center justify-between border-b border-border/60 pb-6 mb-6">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-primary/20 border border-primary/40 flex items-center justify-center text-primary">
                        <Cpu className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className="text-xl font-bold text-foreground font-sans">
                          Indigenous RISC-V Controller for Space Applications
                        </h4>
                        <p className="text-xs font-mono text-primary">
                          HARDWARE SPECIFICATION // ISRO CHANDRA-09 ONBOARD PROCESSING ENGINE
                        </p>
                      </div>
                    </div>
                    <span className="hidden sm:inline-block px-3 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-mono font-bold">
                      VERIFIED SOVEREIGN SILICON
                    </span>
                  </div>

                  <div className="space-y-4 text-sm sm:text-base text-slate-300 leading-relaxed font-sans">
                    <p>
                      The <b>ISRO IRIS (Intelligent Infrared Interpretation System)</b> represents a breakthrough in orbital edge computing, custom-engineered around India's indigenous radiation-hardened <b>64-bit RISC-V microarchitecture</b>. Traditional space missions rely on heavily constrained processors that transmit raw thermal captures to ground stations, resulting in substantial latency and bandwidth bottlenecks during deep-space operations.
                    </p>
                    <p>
                      By embedding neural hardware acceleration directly within the RISC-V controller core (`CHANDRA-09 Payload Controller`), ISRO IRIS performs real-time tensor computation in orbit. This ensures that raw thermal infrared feeds are autonomously denoised, super-resolved, and classified prior to downlink transmission. The controller achieves unprecedented power efficiency (`&lt; 15W operational envelope`) while maintaining deterministic execution across extreme thermal and cosmic radiation fluctuations.
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 font-mono text-xs">
                      <div className="p-4 rounded-xl bg-black/60 border border-border/60">
                        <span className="text-muted-foreground block mb-1">CORE FREQUENCY</span>
                        <span className="text-primary font-bold text-sm">3.2 GHz Quad-Core RISC-V</span>
                      </div>
                      <div className="p-4 rounded-xl bg-black/60 border border-border/60">
                        <span className="text-muted-foreground block mb-1">TENSOR THROUGHPUT</span>
                        <span className="text-emerald-400 font-bold text-sm">12.8 TOPS INT8 Edge Engine</span>
                      </div>
                      <div className="p-4 rounded-xl bg-black/60 border border-border/60">
                        <span className="text-muted-foreground block mb-1">RADIATION SHIELDING</span>
                        <span className="text-secondary font-bold text-sm">300 krad (Si) TID Damping</span>
                      </div>
                    </div>
                  </div>
                </GlassCard>
              </motion.div>
            )}

            {activeTab === 'superres' && (
              <motion.div
                key="superres"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.3 }}
              >
                <GlassCard className="p-8 sm:p-10 border-primary/40 shadow-2xl relative overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
                  <div className="flex items-center justify-between border-b border-border/60 pb-6 mb-6">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-primary/20 border border-primary/40 flex items-center justify-center text-primary">
                        <Sparkles className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className="text-xl font-bold text-foreground font-sans">
                          Multi-Stage AI Super-Resolution & Enhancement Pipeline
                        </h4>
                        <p className="text-xs font-mono text-primary">
                          STAGE 1 & 2 // ADAPTIVE CLAHE & SRCNN/RCAN NEURAL RECONSTRUCTION
                        </p>
                      </div>
                    </div>
                    <span className="hidden sm:inline-block px-3 py-1 rounded bg-primary/10 text-primary border border-primary/30 text-xs font-mono font-bold">
                      +10.0 dB PSNR BOOST
                    </span>
                  </div>

                  <div className="space-y-4 text-sm sm:text-base text-slate-300 leading-relaxed font-sans">
                    <p>
                      Thermal infrared imagery captured from lunar or high-orbit platforms often suffers from sensor readout noise, atmospheric degradation, and low spatial resolution. The ISRO IRIS software stack executes a rigorous 4-stage enhancement workflow designed specifically to recover sub-pixel thermal features without introducing hallucinated artifacts.
                    </p>
                    <p>
                      In <b>Stage 1 (Preprocessing & Contrast Normalization)</b>, Contrast Limited Adaptive Histogram Equalization (`CLAHE`) is dynamically applied across 16-bit radiometric blocks to equalize extreme dynamic ranges between ultra-cold space backgrounds and high-temperature celestial targets. In <b>Stage 2 (Neural Super-Resolution)</b>, deep residual attention networks (`RCAN/SRCNN`) scale 1024x1024 thermal frames to ultra-crisp 4K UHD (`3840x2160`), elevating Structural Similarity (`SSIM`) scores to <b>0.942</b> across SWIR, MWIR, and LWIR spectrums.
                    </p>
                  </div>
                </GlassCard>
              </motion.div>
            )}

            {activeTab === 'detection' && (
              <motion.div
                key="detection"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.3 }}
              >
                <GlassCard className="p-8 sm:p-10 border-primary/40 shadow-2xl relative overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
                  <div className="flex items-center justify-between border-b border-border/60 pb-6 mb-6">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-iris-orange/20 border border-iris-orange/40 flex items-center justify-center text-iris-orange">
                        <Eye className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className="text-xl font-bold text-foreground font-sans">
                          YOLOv8 Structured Detection & Gemini Neural Scene Interpretation
                        </h4>
                        <p className="text-xs font-mono text-iris-orange">
                          STAGE 3 & 4 // TARGET CLASSIFICATION & MULTIMODAL EXECUTIVE DOSSIERS
                        </p>
                      </div>
                    </div>
                    <span className="hidden sm:inline-block px-3 py-1 rounded bg-iris-orange/10 text-iris-orange border border-iris-orange/30 text-xs font-mono font-bold">
                      94.8% CONFIDENCE
                    </span>
                  </div>

                  <div className="space-y-4 text-sm sm:text-base text-slate-300 leading-relaxed font-sans">
                    <p>
                      Once thermal frames are enhanced and mapped into false-color radiometric palettes (`Stage 3`), the system passes the imagery into an embedded <b>YOLOv8 Object Detection engine</b> trained on proprietary ISRO deep-space datasets. The engine identifies thermal anomalies, structural components, orbital debris, and cryo-plume signatures with bounding-box precision and up to <b>94.8% confidence</b>.
                    </p>
                    <p>
                      To synthesize actionable intelligence for mission commanders, ISRO IRIS integrates <b>Google Gemini Multimodal AI</b>. The Gemini engine ingests all 4 processing stages, evaluates target telemetry, and automatically generates formal executive briefing dossiers. These dossiers provide structured radiometric assessments, threat evaluations, and downloadable mission reports with a single click.
                    </p>
                  </div>
                </GlassCard>
              </motion.div>
            )}

            {activeTab === 'radiometry' && (
              <motion.div
                key="radiometry"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.3 }}
              >
                <GlassCard className="p-8 sm:p-10 border-primary/40 shadow-2xl relative overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
                  <div className="flex items-center justify-between border-b border-border/60 pb-6 mb-6">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
                        <Radio className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className="text-xl font-bold text-foreground font-sans">
                          Multi-Spectral Radiometric SWIR, MWIR, and LWIR Band Processing
                        </h4>
                        <p className="text-xs font-mono text-emerald-400">
                          PRECISION RADIOMETRY // CALIBRATED THERMAL FLUX MAPPING
                        </p>
                      </div>
                    </div>
                    <span className="hidden sm:inline-block px-3 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-mono font-bold">
                      FULL SPECTRUM COVERAGE
                    </span>
                  </div>

                  <div className="space-y-4 text-sm sm:text-base text-slate-300 leading-relaxed font-sans">
                    <p>
                      The ISRO IRIS platform is built for uncompromising radiometric accuracy across three primary infrared spectral bands: <b>Short-Wave Infrared (SWIR 1.4µm)</b>, <b>Mid-Wave Infrared (MWIR 3.4µm - 4.8µm)</b>, and <b>Long-Wave Infrared (LWIR 8.4µm - 14.0µm)</b>. Each band provides distinct insights into target emissivity, surface temperature gradients, and subsurface material structures.
                    </p>
                    <p>
                      Through calibrated thermal colormaps (`Inferno`, `Plasma`, `Jet`, and `Lunar Thermal`), mission operators can isolate specific thermal thresholds down to 0.05 Kelvin resolution. This exact calibration ensures that scientific teams analyzing lunar craters or deep-space thermal emissions receive mathematically rigorous, research-grade datasets.
                    </p>
                  </div>
                </GlassCard>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </section>

      {/* Capabilities Overview Section */}
      <section id="capabilities" className="py-20 px-6 max-w-[1440px] mx-auto border-t border-border/40">
        <div className="text-center max-w-3xl mx-auto mb-14 space-y-3">
          <Badge variant="secondary" className="font-mono text-xs">
            INTELLIGENT PIPELINE
          </Badge>
          <h3 className="text-3xl sm:text-4xl font-extrabold text-foreground tracking-tight">
            Key Mission Capabilities
          </h3>
          <p className="text-sm text-muted-foreground font-sans">
            End-to-end autonomous infrared image processing powered by deep learning and local RISC-V edge execution.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <GlassCard className="p-6 border-primary/30 hover:border-primary transition-all group flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-primary/20 border border-primary/40 flex items-center justify-center text-primary mb-4 group-hover:scale-110 transition-transform">
                <Sparkles className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-foreground mb-2">Neural Super-Resolution</h4>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Reconstruct high-frequency thermal details from noisy space feeds using custom residual networks with +10 dB average PSNR gain.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-border/50 text-[11px] font-mono text-primary font-bold flex items-center gap-1">
              <span>STAGE 1 & 2 ACTIVE</span>
              <ArrowRight className="w-3.5 h-3.5 ml-auto" />
            </div>
          </GlassCard>

          <GlassCard className="p-6 border-secondary/30 hover:border-secondary transition-all group flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-secondary/20 border border-secondary/40 flex items-center justify-center text-secondary mb-4 group-hover:scale-110 transition-transform">
                <Radio className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-foreground mb-2">Thermal Colormaps</h4>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Transform raw grayscale radiometric captures into vibrant multi-spectral false-color palettes for instant thermal feature extraction.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-border/50 text-[11px] font-mono text-secondary font-bold flex items-center gap-1">
              <span>STAGE 3 ACTIVE</span>
              <ArrowRight className="w-3.5 h-3.5 ml-auto" />
            </div>
          </GlassCard>

          <GlassCard className="p-6 border-iris-orange/30 hover:border-iris-orange transition-all group flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-iris-orange/20 border border-iris-orange/40 flex items-center justify-center text-iris-orange mb-4 group-hover:scale-110 transition-transform">
                <Eye className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-foreground mb-2">YOLOv8 Detection</h4>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Autonomous classification of lunar structures, cryo-plumes, orbital debris, and thermal anomalies with bounding-box precision.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-border/50 text-[11px] font-mono text-iris-orange font-bold flex items-center gap-1">
              <span>STAGE 4 ACTIVE</span>
              <ArrowRight className="w-3.5 h-3.5 ml-auto" />
            </div>
          </GlassCard>

          <GlassCard className="p-6 border-emerald-500/30 hover:border-emerald-500 transition-all group flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 mb-4 group-hover:scale-110 transition-transform">
                <Database className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-foreground mb-2">Mission Dossiers</h4>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Gemini AI synthesizes all 4 processing stages into structured executive summaries and downloadable PDF briefing documents.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-border/50 text-[11px] font-mono text-emerald-400 font-bold flex items-center gap-1">
              <span>PDF DOSSIERS READY</span>
              <ArrowRight className="w-3.5 h-3.5 ml-auto" />
            </div>
          </GlassCard>
        </div>
      </section>

      {/* Bottom CTA Banner */}
      <section className="py-20 px-6 max-w-[1440px] mx-auto">
        <GlassCard className="p-10 sm:p-14 border-primary/50 relative overflow-hidden bg-gradient-to-r from-primary/15 via-slate-950 to-secondary/15 text-center shadow-[0_0_50px_rgba(0,240,255,0.25)]">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(0,240,255,0.1)_0,transparent_70%)] pointer-events-none" />
          <div className="relative z-10 max-w-2xl mx-auto space-y-6">
            <Badge variant="primary" className="font-mono text-xs">
              SECURE MISSION ACCESS
            </Badge>
            <h3 className="text-3xl sm:text-4xl font-extrabold text-foreground tracking-tight">
              Ready to Enter the Tactical Command Center?
            </h3>
            <p className="text-sm sm:text-base text-muted-foreground font-sans">
              Authenticate using your ISRO credentials to unlock live CHANDRA-09 sample feeds, real-time Neural Workspace processing, and tactical mission telemetry.
            </p>
            <div className="pt-2 flex justify-center">
              <Link href="/login">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-10 py-4 rounded-2xl font-mono text-sm font-bold tracking-wider bg-gradient-to-r from-primary via-teal-400 to-secondary text-background shadow-[0_0_35px_rgba(0,240,255,0.6)] hover:shadow-[0_0_55px_rgba(0,240,255,0.9)] transition-all flex items-center gap-3 border border-primary/50"
                >
                  <Lock className="w-5 h-5" />
                  <span>PROCEED TO LOGIN // MISSION ACCESS</span>
                  <ArrowRight className="w-5 h-5" />
                </motion.button>
              </Link>
            </div>
          </div>
        </GlassCard>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/40 py-8 px-6 text-center text-xs font-mono text-muted-foreground bg-background/90">
        <div className="max-w-[1440px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-400" />
            <span>ISRO IRIS — CHANDRA-09 THERMAL INTERPRETATION SYSTEM // RUNNING ON LOCAL ENGINE</span>
          </div>
          <div>
            <span>© 2026 INDIAN SPACE RESEARCH ORGANISATION // INDIGENOUS RISC-V DIVISION</span>
          </div>
        </div>
      </footer>
    </div>
  )
}
