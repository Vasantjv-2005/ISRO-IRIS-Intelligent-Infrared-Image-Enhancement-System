'use client'

import React, { useState } from 'react'
import { motion } from 'framer-motion'
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
} from 'lucide-react'
import { GlassCard } from '@/components/ui/GlassCard'
import { Badge } from '@/components/ui/Badge'
import { useView } from '@/lib/context/ViewContext'
import { useImage } from '@/lib/context/ImageContext'
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
}

const DOSSIERS: DossierItem[] = [
  {
    id: 'DOS-8842-IR',
    title: 'Chandra-09 South Ridge Radiometric Survey',
    missionCode: 'CHANDRA-09 // T-8842',
    date: '11 JUL 2026 12:14 UTC',
    sensorBand: 'MWIR 8.4µm Cryo-Cooled',
    resolution: '3840 x 2160 (16-bit Radiometric TIFF)',
    psnr: '38.42 dB (+8.42 dB gain)',
    ssim: '0.942 Structural Fidelity',
    targetsDetected: 4,
    status: 'VERIFIED',
    classification: 'ISRO UNCLASSIFIED // SCIENTIFIC',
  },
  {
    id: 'DOS-8839-IR',
    title: 'Orbital Array Delta-4 Thermal Signature',
    missionCode: 'CHANDRA-09 // T-8839',
    date: '11 JUL 2026 10:48 UTC',
    sensorBand: 'LWIR 11.2µm Array',
    resolution: '2048 x 2048 (MWIR)',
    psnr: '36.80 dB (+7.85 dB gain)',
    ssim: '0.928 Structural Fidelity',
    targetsDetected: 6,
    status: 'VERIFIED',
    classification: 'ISRO UNCLASSIFIED // SCIENTIFIC',
  },
  {
    id: 'DOS-8831-IR',
    title: 'Lunar Polar Crater Plume Spectroscopy',
    missionCode: 'CHANDRA-09 // T-8831',
    date: '10 JUL 2026 21:30 UTC',
    sensorBand: 'SWIR 1.4µm Array',
    resolution: '4096 x 4096 (Radiometric)',
    psnr: '39.10 dB (+9.14 dB gain)',
    ssim: '0.951 Structural Fidelity',
    targetsDetected: 2,
    status: 'ARCHIVE',
    classification: 'ISRO UNCLASSIFIED // SCIENTIFIC',
  },
]

export function MissionDossierGallery() {
  const { setActiveView } = useView()
  const { setCurrentImage } = useImage()
  const [downloadingId, setDownloadingId] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')

  const handleInspect = () => {
    setCurrentImage(CHANDRA_09_DEMO_DATA)
    setActiveView('workspace')
  }

  const handleDownloadPdf = (id: string) => {
    setDownloadingId(id)
    setTimeout(() => {
      setDownloadingId(null)
      // Simulate download trigger
      const link = document.createElement('a')
      link.href = '#'
      link.setAttribute('download', `${id}_ISRO_MISSION_DOSSIER.pdf`)
      alert(`Exporting ISRO Official Mission Dossier [${id}] to PDF...`)
    }, 1200)
  }

  const filteredDossiers = DOSSIERS.filter(
    (d) =>
      d.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.missionCode.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="space-y-6">
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
              Official verified PDF dossiers containing radiometric comparisons, YOLOv8 target tables, and Gemini AI briefings.
            </p>
          </div>

          <div className="relative w-full md:w-72">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search dossiers or sectors..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-background/80 border border-border text-sm text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary shadow-inner"
            />
          </div>
        </div>
      </GlassCard>

      {/* Dossiers Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {filteredDossiers.map((item, idx) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <GlassCard className="p-6 flex flex-col justify-between h-full border-primary/20 hover:border-primary/60 transition-all group">
              <div>
                <div className="flex items-start justify-between mb-3">
                  <div className="p-2.5 rounded-xl bg-primary/10 border border-primary/30 text-primary">
                    <FileText className="w-5 h-5" />
                  </div>
                  <Badge
                    variant={item.status === 'VERIFIED' ? 'success' : 'secondary'}
                    size="sm"
                  >
                    <ShieldCheck className="w-3 h-3" />
                    {item.status}
                  </Badge>
                </div>

                <span className="text-[11px] font-mono font-bold text-primary tracking-wide">
                  {item.missionCode}
                </span>
                <h3 className="text-lg font-bold text-foreground mt-1 mb-2 group-hover:text-primary transition-colors">
                  {item.title}
                </h3>

                <div className="space-y-2 py-3 border-y border-border/60 text-xs font-mono my-3">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Timestamp</span>
                    <span className="text-foreground">{item.date}</span>
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
                  onClick={handleInspect}
                  className="w-full py-2.5 rounded-xl bg-background/80 hover:bg-primary/15 border border-border hover:border-primary/50 text-xs font-mono font-bold text-foreground hover:text-primary transition-all flex items-center justify-center gap-1.5"
                >
                  <Eye className="w-3.5 h-3.5" />
                  <span>INSPECT</span>
                </button>

                <button
                  onClick={() => handleDownloadPdf(item.id)}
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
        ))}
      </div>
    </div>
  )
}
