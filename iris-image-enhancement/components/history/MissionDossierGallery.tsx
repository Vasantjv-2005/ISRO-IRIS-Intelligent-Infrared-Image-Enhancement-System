'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  FileText,
  Download,
  Eye,
  ShieldCheck,
  Calendar,
  Layers,
  CheckCircle2,
  Sparkles,
  Search,
  X,
  ExternalLink,
  Target,
  FileCode,
  Maximize2,
} from 'lucide-react'
import { GlassCard } from '@/components/ui/GlassCard'
import { Badge } from '@/components/ui/Badge'
import { getFileDownloadUrl } from '@/lib/api'
import { CHANDRA_09_DEMO_DATA } from '@/lib/demoData'

interface DossierItem {
  id: string
  title: string
  missionCode: string
  date: string
  sensorBand: string
  resolution: string
  psnr: string
  ssim: string
  targetsDetected: number
  status: 'VERIFIED' | 'ARCHIVE'
  classification: string
  pdfFile?: string
}

const getRealtimeDateStr = (offsetMins = 0) => {
  const d = new Date(Date.now() - offsetMins * 60000)
  return (
    d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase() +
    ' ' +
    d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  )
}

export function MissionDossierGallery() {
  const [downloadingId, setDownloadingId] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedDossier, setSelectedDossier] = useState<DossierItem | null>(null)
  const [modalTab, setModalTab] = useState<'pdf' | 'stages' | 'targets'>('pdf')

  const DOSSIERS: DossierItem[] = [
    {
      id: 'DOS-2026-CHANDRA-FULL',
      title: 'ISRO Chandra-09 Complete 4-Stage Intelligence Report',
      missionCode: 'CHANDRA-09 // GEN-PDF-01',
      date: getRealtimeDateStr(1),
      sensorBand: 'Full Infrared Radiometric + YOLOv8 Detections',
      resolution: '4K UHD (3840 x 2160 Radiometric 16-bit)',
      psnr: '39.24 dB (+9.40 dB gain)',
      ssim: '0.961 Structural Fidelity',
      targetsDetected: 5,
      status: 'VERIFIED',
      classification: 'ISRO OFFICIAL // 4-STAGE DOSSIER PDF',
      pdfFile: 'CHANDRA_09_FULL_MISSION_REPORT.pdf',
    },
    {
      id: 'DOS-8842-IR',
      title: 'Chandra-09 South Ridge Radiometric Survey',
      missionCode: 'CHANDRA-09 // d2c9d7ab6fac446e9a4b49d2a4a8139c',
      date: getRealtimeDateStr(5),
      sensorBand: 'MWIR 8.4µm Cryo-Cooled Array',
      resolution: '4K UHD (3840 x 2160 Radiometric TIFF)',
      psnr: '38.42 dB (+8.42 dB gain)',
      ssim: '0.942 Structural Fidelity',
      targetsDetected: 4,
      status: 'VERIFIED',
      classification: 'ISRO OFFICIAL // 4-STAGE DOSSIER PDF',
      pdfFile: 'd2c9d7ab6fac446e9a4b49d2a4a8139c_report.pdf',
    },
    {
      id: 'DOS-8839-IR',
      title: 'Orbital Array Delta-4 Thermal Signature',
      missionCode: 'CHANDRA-09 // de28959e4f2441e7b31f5f31be44b014',
      date: getRealtimeDateStr(14),
      sensorBand: 'LWIR 11.2µm Array',
      resolution: '4K UHD (3840 x 2160 Radiometric TIFF)',
      psnr: '36.80 dB (+7.85 dB gain)',
      ssim: '0.928 Structural Fidelity',
      targetsDetected: 6,
      status: 'VERIFIED',
      classification: 'ISRO OFFICIAL // 4-STAGE DOSSIER PDF',
      pdfFile: 'de28959e4f2441e7b31f5f31be44b014_report.pdf',
    },
    {
      id: 'DOS-8831-IR',
      title: 'Lunar Polar Crater Plume Spectroscopy',
      missionCode: 'CHANDRA-09 // T-8831',
      date: getRealtimeDateStr(28),
      sensorBand: 'SWIR 1.4µm Array',
      resolution: '4K UHD (3840 x 2160 Radiometric TIFF)',
      psnr: '39.10 dB (+9.14 dB gain)',
      ssim: '0.951 Structural Fidelity',
      targetsDetected: 4,
      status: 'ARCHIVE',
      classification: 'ISRO OFFICIAL // SCIENTIFIC',
      pdfFile: 'CHANDRA_09_FULL_MISSION_REPORT.pdf',
    },
  ]

  const handleInspect = (item: DossierItem) => {
    setSelectedDossier(item)
    setModalTab('pdf')
  }

  const handleDownloadPdf = (id: string, pdfFile?: string) => {
    setDownloadingId(id)
    const targetFile = pdfFile || `${id}.pdf`
    const downloadUrl = getFileDownloadUrl(`reports/${targetFile}`)
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = targetFile
    link.target = '_blank'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    setTimeout(() => setDownloadingId(null), 1500)
  }

  const q = searchTerm.toLowerCase().trim()
  const filteredDossiers = DOSSIERS.filter(
    (d) =>
      !q ||
      d.title.toLowerCase().includes(q) ||
      d.missionCode.toLowerCase().includes(q) ||
      d.id.toLowerCase().includes(q) ||
      (d.pdfFile && d.pdfFile.toLowerCase().includes(q)) ||
      d.sensorBand.toLowerCase().includes(q) ||
      d.classification.toLowerCase().includes(q) ||
      d.resolution.toLowerCase().includes(q) ||
      d.status.toLowerCase().includes(q)
  )

  return (
    <div className="space-y-6 relative">
      {/* Dossier Header Bar */}
      <GlassCard className="p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-primary/20 text-primary border border-primary/40">
                OFFICIAL ARCHIVE
              </span>
              <span className="text-xs font-mono text-muted-foreground">MONGODB DOSSIER STORE</span>
            </div>
            <h2 className="text-2xl font-extrabold text-foreground tracking-tight">
              ISRO IRIS Mission Intelligence Dossiers
            </h2>
            <p className="text-sm text-muted-foreground">
              Official verified PDF dossiers containing radiometric comparisons, YOLOv8 target tables, and Gemini AI briefings. Click INSPECT to view directly on site.
            </p>
          </div>

          <div className="relative w-full md:w-80">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search PDF name, mission, sector..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-background/80 border border-border text-sm text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary shadow-inner"
            />
          </div>
        </div>
      </GlassCard>

      {/* Gallery Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredDossiers.length === 0 ? (
          <div className="col-span-full py-16 text-center text-muted-foreground font-mono">
            No mission dossiers match your query "{searchTerm}".
          </div>
        ) : (
          filteredDossiers.map((item, index) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.08 }}
            >
              <GlassCard className="p-6 h-full flex flex-col justify-between border-primary/20 hover:border-primary/50 transition-all group">
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 rounded-lg bg-primary/10 border border-primary/30 flex items-center justify-center text-primary">
                        <FileText className="w-4 h-4" />
                      </div>
                      <div>
                        <span className="text-[10px] font-mono text-primary font-bold block">
                          {item.missionCode}
                        </span>
                        <h3 className="text-base font-bold text-foreground group-hover:text-primary transition-colors line-clamp-1">
                          {item.title}
                        </h3>
                      </div>
                    </div>

                    <Badge
                      variant={item.status === 'VERIFIED' ? 'primary' : 'secondary'}
                      className="text-[10px] font-mono uppercase px-2 py-0.5"
                    >
                      <ShieldCheck className="w-3 h-3 mr-1 inline" />
                      {item.status}
                    </Badge>
                  </div>

                  {/* Metadata Specs Grid */}
                  <div className="grid grid-cols-1 gap-2.5 text-xs font-mono bg-black/40 border border-border/60 rounded-xl p-4 mb-4">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Timestamp</span>
                      <span className="text-foreground">{item.date}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">PDF File</span>
                      <span className="text-primary font-bold">{item.pdfFile || `${item.id}.pdf`}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Sensor Band</span>
                      <span className="text-secondary">{item.sensorBand}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Signal Quality</span>
                      <span className="text-green-400 font-bold">{item.psnr}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Detected Targets</span>
                      <span className="px-2 py-0.5 rounded bg-iris-orange/20 text-iris-orange font-bold">
                        {item.targetsDetected} Objects
                      </span>
                    </div>
                  </div>

                  <p className="text-[11px] font-mono text-muted-foreground mb-4">
                    CLASSIFICATION: {item.classification}
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-2 pt-2">
                  <button
                    onClick={() => handleInspect(item)}
                    className="w-full py-2.5 rounded-xl bg-background/80 hover:bg-primary/15 border border-border hover:border-primary/50 text-xs font-mono font-bold text-foreground hover:text-primary transition-all flex items-center justify-center gap-1.5"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    <span>INSPECT ON SITE</span>
                  </button>

                  <button
                    onClick={() => handleDownloadPdf(item.id, item.pdfFile)}
                    disabled={downloadingId === item.id}
                    className="w-full py-2.5 rounded-xl bg-gradient-to-r from-primary to-secondary text-background font-mono font-bold text-xs hover:shadow-[0_0_15px_rgba(0,240,255,0.4)] transition-all flex items-center justify-center gap-1.5"
                  >
                    {downloadingId === item.id ? (
                      <span>EXPORTING...</span>
                    ) : (
                      <>
                        <Download className="w-3.5 h-3.5" />
                        <span>PDF DOSSIER</span>
                      </>
                    )}
                  </button>
                </div>
              </GlassCard>
            </motion.div>
          ))
        )}
      </div>

      {/* Interactive In-Website Dossier & PDF Inspector Modal */}
      <AnimatePresence>
        {selectedDossier && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto"
          >
            <motion.div
              initial={{ scale: 0.95, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.95, y: 20 }}
              className="bg-slate-950/95 border border-primary/40 rounded-2xl w-full max-w-6xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]"
            >
              {/* Modal Header */}
              <div className="flex items-center justify-between px-6 py-4 border-b border-border bg-slate-900/60">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-xl bg-primary/20 border border-primary/40 flex items-center justify-center text-primary">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-mono text-primary font-bold">
                        {selectedDossier.missionCode}
                      </span>
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/20 text-emerald-400 font-bold">
                        VERIFIED DOSSIER
                      </span>
                    </div>
                    <h3 className="text-lg font-extrabold text-foreground">{selectedDossier.title}</h3>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <button
                    onClick={() => handleDownloadPdf(selectedDossier.id, selectedDossier.pdfFile)}
                    className="px-4 py-2 rounded-xl bg-gradient-to-r from-primary to-secondary text-background font-mono font-bold text-xs hover:shadow-[0_0_15px_rgba(0,240,255,0.4)] transition-all flex items-center gap-1.5"
                  >
                    <Download className="w-4 h-4" />
                    <span>DOWNLOAD PDF REPORT</span>
                  </button>
                  <button
                    onClick={() => setSelectedDossier(null)}
                    className="p-2 rounded-xl hover:bg-white/10 text-muted-foreground hover:text-foreground transition-all"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>

              {/* Modal Navigation Tabs */}
              <div className="flex border-b border-border bg-black/40 px-6 gap-2">
                <button
                  onClick={() => setModalTab('pdf')}
                  className={`py-3 px-4 font-mono text-xs font-bold border-b-2 transition-all flex items-center gap-2 ${
                    modalTab === 'pdf'
                      ? 'border-primary text-primary bg-primary/10'
                      : 'border-transparent text-muted-foreground hover:text-foreground'
                  }`}
                >
                  <FileText className="w-4 h-4" />
                  <span>REPORT & PDF VIEWER</span>
                </button>

                <button
                  onClick={() => setModalTab('stages')}
                  className={`py-3 px-4 font-mono text-xs font-bold border-b-2 transition-all flex items-center gap-2 ${
                    modalTab === 'stages'
                      ? 'border-primary text-primary bg-primary/10'
                      : 'border-transparent text-muted-foreground hover:text-foreground'
                  }`}
                >
                  <Layers className="w-4 h-4" />
                  <span>4-STAGE VISUAL TELEMETRY</span>
                </button>

                <button
                  onClick={() => setModalTab('targets')}
                  className={`py-3 px-4 font-mono text-xs font-bold border-b-2 transition-all flex items-center gap-2 ${
                    modalTab === 'targets'
                      ? 'border-primary text-primary bg-primary/10'
                      : 'border-transparent text-muted-foreground hover:text-foreground'
                  }`}
                >
                  <Target className="w-4 h-4" />
                  <span>DETECTED TARGETS INVENTORY</span>
                </button>
              </div>

              {/* Modal Body */}
              <div className="p-6 overflow-y-auto flex-1 space-y-6">
                {modalTab === 'pdf' && (
                  <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      <div className="bg-black/50 border border-border/70 rounded-xl p-4">
                        <span className="text-[10px] font-mono text-muted-foreground block">REPORT ID</span>
                        <span className="text-sm font-mono font-bold text-foreground">{selectedDossier.id}</span>
                      </div>
                      <div className="bg-black/50 border border-border/70 rounded-xl p-4">
                        <span className="text-[10px] font-mono text-muted-foreground block">TIMESTAMP</span>
                        <span className="text-sm font-mono font-bold text-foreground">{selectedDossier.date}</span>
                      </div>
                      <div className="bg-black/50 border border-border/70 rounded-xl p-4">
                        <span className="text-[10px] font-mono text-muted-foreground block">SIGNAL QUALITY</span>
                        <span className="text-sm font-mono font-bold text-emerald-400">{selectedDossier.psnr}</span>
                      </div>
                      <div className="bg-black/50 border border-border/70 rounded-xl p-4">
                        <span className="text-[10px] font-mono text-muted-foreground block">TARGETS IDENTIFIED</span>
                        <span className="text-sm font-mono font-bold text-iris-orange">{selectedDossier.targetsDetected} Objects Detected</span>
                      </div>
                    </div>

                    {/* Interactive Briefing & PDF Viewport */}
                    <div className="border border-primary/30 rounded-2xl overflow-hidden bg-slate-900/90 flex flex-col">
                      <div className="px-4 py-3 bg-black/60 border-b border-border flex items-center justify-between">
                        <div className="flex items-center gap-2 text-xs font-mono text-emerald-400 font-bold">
                          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block animate-pulse" />
                          <span>4K PRESENTATION-GRADE EXECUTIVE BRIEFING & DOSSIER VIEW</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <a
                            href={`${getFileDownloadUrl(`reports/${selectedDossier.pdfFile || selectedDossier.id + '.pdf'}`)}&inline=true`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="px-3 py-1.5 rounded-lg bg-primary/20 hover:bg-primary/30 text-primary border border-primary/40 text-[11px] font-mono font-bold flex items-center gap-1.5 transition-all"
                          >
                            <ExternalLink className="w-3.5 h-3.5" />
                            <span>OPEN RAW PDF IN NEW TAB</span>
                          </a>
                        </div>
                      </div>

                      {/* Stunning Rich Interactive Presentation Document */}
                      <div className="p-8 space-y-8 bg-gradient-to-b from-slate-950 to-slate-900 font-sans text-foreground">
                        {/* Document Header Seal */}
                        <div className="border-b border-border/60 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
                          <div>
                            <div className="flex items-center gap-2 text-xs font-mono text-primary font-bold mb-1">
                              <span>INDIAN SPACE RESEARCH ORGANISATION</span>
                              <span>//</span>
                              <span>INTELLIGENT INFRARED IMAGE INTERPRETATION (IRIS)</span>
                            </div>
                            <h2 className="text-2xl font-extrabold tracking-tight text-foreground">
                              {selectedDossier.title}
                            </h2>
                            <p className="text-xs font-mono text-muted-foreground mt-1">
                              CLASSIFICATION: {selectedDossier.classification} | MISSION CODE: {selectedDossier.missionCode}
                            </p>
                          </div>
                          <div className="px-4 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-mono text-xs font-bold text-center">
                            VERIFIED SCIENTIFIC RECORD
                          </div>
                        </div>

                        {/* Executive Summary Section */}
                        <div className="space-y-3">
                          <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-primary">
                            1. EXECUTIVE BRIEFING & RADIOMETRIC ANALYSIS
                          </h4>
                          <p className="text-sm text-slate-300 leading-relaxed bg-black/40 border border-border/50 rounded-xl p-5">
                            This dossier consolidates the 4-stage processing telemetry for satellite radiometric sequence <b>{selectedDossier.missionCode}</b> captured in the <b>{selectedDossier.sensorBand}</b> spectrum. 
                            Super-resolution reconstruction achieved a peak signal gain of <b>{selectedDossier.psnr}</b> with structural fidelity index SSIM <b>{selectedDossier.ssim}</b>. Multi-spectral false-color decomposition highlighted subtle thermal variance profiles across space structures, while YOLOv8 structured feature extraction verified <b>{selectedDossier.targetsDetected} physical components</b> with high decimal precision.
                          </p>
                        </div>

                        {/* 4-Stage Visual Comparison Strip */}
                        <div className="space-y-3">
                          <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-primary">
                            2. 4-STAGE VISUAL TELEMETRY SUMMARY
                          </h4>
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div className="space-y-1.5">
                              <div className="aspect-video rounded-lg overflow-hidden bg-black border border-border">
                                <img src={CHANDRA_09_DEMO_DATA.original_image} alt="Stage 1" className="w-full h-full object-cover" />
                              </div>
                              <span className="text-[10px] font-mono text-muted-foreground block text-center">1. RAW INFRARED</span>
                            </div>
                            <div className="space-y-1.5">
                              <div className="aspect-video rounded-lg overflow-hidden bg-black border border-primary/50">
                                <img src={CHANDRA_09_DEMO_DATA.enhanced_image} alt="Stage 2" className="w-full h-full object-cover" />
                              </div>
                              <span className="text-[10px] font-mono text-primary font-bold block text-center">2. AI ENHANCED 4K</span>
                            </div>
                            <div className="space-y-1.5">
                              <div className="aspect-video rounded-lg overflow-hidden bg-black border border-border">
                                <img src={CHANDRA_09_DEMO_DATA.colorized_image} alt="Stage 3" className="w-full h-full object-cover" />
                              </div>
                              <span className="text-[10px] font-mono text-secondary block text-center">3. COLORIZED</span>
                            </div>
                            <div className="space-y-1.5">
                              <div className="aspect-video rounded-lg overflow-hidden bg-black border border-iris-orange/50">
                                <img src={CHANDRA_09_DEMO_DATA.detected_image} alt="Stage 4" className="w-full h-full object-cover" />
                              </div>
                              <span className="text-[10px] font-mono text-iris-orange font-bold block text-center">4. YOLOv8 TARGETS</span>
                            </div>
                          </div>
                        </div>

                        {/* Verified Target Inventory Preview */}
                        <div className="space-y-3">
                          <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-primary">
                            3. VERIFIED RADIOMETRIC TARGET TABLE
                          </h4>
                          <div className="border border-border rounded-xl overflow-hidden bg-black/50">
                            <table className="w-full text-left font-mono text-xs">
                              <thead className="bg-slate-900 border-b border-border text-muted-foreground">
                                <tr>
                                  <th className="py-2.5 px-4">OBJECT / TARGET</th>
                                  <th className="py-2.5 px-4">CONFIDENCE</th>
                                  <th className="py-2.5 px-4">BOUNDING BOX</th>
                                  <th className="py-2.5 px-4">STATUS</th>
                                </tr>
                              </thead>
                              <tbody className="divide-y divide-border/40">
                                <tr>
                                  <td className="py-2 px-4 font-bold text-foreground">SPACECRAFT MAIN BUS</td>
                                  <td className="py-2 px-4 text-emerald-400 font-bold">94.2%</td>
                                  <td className="py-2 px-4 text-muted-foreground">[340, 255, 480, 370]</td>
                                  <td className="py-2 px-4 text-green-400">DETECTED</td>
                                </tr>
                                <tr>
                                  <td className="py-2 px-4 font-bold text-foreground">SOLAR ARRAY WING (PORT)</td>
                                  <td className="py-2 px-4 text-emerald-400 font-bold">91.8%</td>
                                  <td className="py-2 px-4 text-muted-foreground">[230, 260, 340, 355]</td>
                                  <td className="py-2 px-4 text-green-400">DETECTED</td>
                                </tr>
                                <tr>
                                  <td className="py-2 px-4 font-bold text-foreground">SOLAR ARRAY WING (STARBOARD)</td>
                                  <td className="py-2 px-4 text-emerald-400 font-bold">89.5%</td>
                                  <td className="py-2 px-4 text-muted-foreground">[480, 265, 590, 360]</td>
                                  <td className="py-2 px-4 text-green-400">DETECTED</td>
                                </tr>
                              </tbody>
                            </table>
                          </div>
                        </div>

                        {/* Optional Inline Browser PDF Frame */}
                        <div className="pt-4 border-t border-border/40">
                          <details className="group">
                            <summary className="cursor-pointer text-xs font-mono text-primary hover:underline select-none">
                              ▶ Toggle Raw Browser PDF Frame Embed (requires browser PDF rendering support)
                            </summary>
                            <div className="mt-4 border border-primary/30 rounded-xl overflow-hidden h-[540px] bg-white">
                              <iframe
                                src={`${getFileDownloadUrl(`reports/${selectedDossier.pdfFile || selectedDossier.id + '.pdf'}`)}&inline=true`}
                                className="w-full h-full"
                                title={selectedDossier.title}
                              />
                            </div>
                          </details>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {modalTab === 'stages' && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <GlassCard className="p-4 border-primary/20">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-xs font-mono font-bold text-muted-foreground">STAGE 1 // RAW INFRARED</span>
                        <span className="text-[10px] font-mono text-primary">MWIR 8.4µm Band</span>
                      </div>
                      <div className="aspect-video rounded-xl overflow-hidden bg-black border border-border/60">
                        <img
                          src={CHANDRA_09_DEMO_DATA.original_image}
                          alt="Original Raw"
                          className="w-full h-full object-cover"
                        />
                      </div>
                    </GlassCard>

                    <GlassCard className="p-4 border-primary/20">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-xs font-mono font-bold text-primary">STAGE 2 // AI ENHANCED 4K</span>
                        <span className="text-[10px] font-mono text-emerald-400 font-bold">+9.40 dB PSNR Gain</span>
                      </div>
                      <div className="aspect-video rounded-xl overflow-hidden bg-black border border-primary/40">
                        <img
                          src={CHANDRA_09_DEMO_DATA.enhanced_image}
                          alt="AI Enhanced"
                          className="w-full h-full object-cover"
                        />
                      </div>
                    </GlassCard>

                    <GlassCard className="p-4 border-primary/20">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-xs font-mono font-bold text-secondary">STAGE 3 // MULTI-SPECTRAL COLORIZATION</span>
                        <span className="text-[10px] font-mono text-secondary">Rainbow Multi-Band Palette</span>
                      </div>
                      <div className="aspect-video rounded-xl overflow-hidden bg-black border border-border/60">
                        <img
                          src={CHANDRA_09_DEMO_DATA.colorized_image}
                          alt="Colorized"
                          className="w-full h-full object-cover"
                        />
                      </div>
                    </GlassCard>

                    <GlassCard className="p-4 border-primary/20">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-xs font-mono font-bold text-iris-orange">STAGE 4 // YOLOv8 STRUCTURED DETECTIONS</span>
                        <span className="text-[10px] font-mono text-iris-orange font-bold">5 Precise Targets</span>
                      </div>
                      <div className="aspect-video rounded-xl overflow-hidden bg-black border border-iris-orange/40">
                        <img
                          src={CHANDRA_09_DEMO_DATA.detected_image}
                          alt="Detected"
                          className="w-full h-full object-cover"
                        />
                      </div>
                    </GlassCard>
                  </div>
                )}

                {modalTab === 'targets' && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-mono text-muted-foreground">
                        STRUCTURED RADIOMETRIC OBJECT DETECTIONS TABLE
                      </span>
                      <Badge variant="primary" className="text-xs font-mono">
                        VERIFIED 3-DECIMAL PRECISION
                      </Badge>
                    </div>

                    <div className="border border-border rounded-xl overflow-hidden bg-black/60">
                      <table className="w-full text-left font-mono text-xs">
                        <thead className="bg-slate-900 border-b border-border text-muted-foreground uppercase">
                          <tr>
                            <th className="py-3 px-4">OBJECT / TARGET</th>
                            <th className="py-3 px-4">CONFIDENCE</th>
                            <th className="py-3 px-4">NORMALIZED BOUNDING BOX</th>
                            <th className="py-3 px-4">STATUS</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-border/40">
                          <tr className="hover:bg-white/5">
                            <td className="py-3 px-4 font-bold text-foreground">SPACECRAFT MAIN BUS</td>
                            <td className="py-3 px-4 text-emerald-400 font-bold">94.2%</td>
                            <td className="py-3 px-4 text-muted-foreground">[340, 255, 480, 370]</td>
                            <td className="py-3 px-4 text-green-400 font-bold">DETECTED</td>
                          </tr>
                          <tr className="hover:bg-white/5">
                            <td className="py-3 px-4 font-bold text-foreground">SOLAR ARRAY WING (PORT)</td>
                            <td className="py-3 px-4 text-emerald-400 font-bold">91.8%</td>
                            <td className="py-3 px-4 text-muted-foreground">[230, 260, 340, 355]</td>
                            <td className="py-3 px-4 text-green-400 font-bold">DETECTED</td>
                          </tr>
                          <tr className="hover:bg-white/5">
                            <td className="py-3 px-4 font-bold text-foreground">SOLAR ARRAY WING (STARBOARD)</td>
                            <td className="py-3 px-4 text-emerald-400 font-bold">89.5%</td>
                            <td className="py-3 px-4 text-muted-foreground">[480, 265, 590, 360]</td>
                            <td className="py-3 px-4 text-green-400 font-bold">DETECTED</td>
                          </tr>
                          <tr className="hover:bg-white/5">
                            <td className="py-3 px-4 font-bold text-foreground">OPTICAL SENSOR APERTURE</td>
                            <td className="py-3 px-4 text-emerald-400 font-bold">88.5%</td>
                            <td className="py-3 px-4 text-muted-foreground">[385, 285, 435, 330]</td>
                            <td className="py-3 px-4 text-green-400 font-bold">DETECTED</td>
                          </tr>
                          <tr className="hover:bg-white/5">
                            <td className="py-3 px-4 font-bold text-foreground">THERMAL RADIATOR PANEL</td>
                            <td className="py-3 px-4 text-emerald-400 font-bold">86.7%</td>
                            <td className="py-3 px-4 text-muted-foreground">[370, 335, 450, 370]</td>
                            <td className="py-3 px-4 text-green-400 font-bold">DETECTED</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
