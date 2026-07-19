import { ImageData } from './context/ImageContext'

// Generate stunning high-tech SVG thermal imagery data URIs for demo / instant testing
export function generateThermalSvgUrl(type: 'raw' | 'enhanced' | 'inferno' | 'magma' | 'plasma' | 'viridis' | 'jet' | 'rainbow'): string {
  const isRaw = type === 'raw'
  const filterBlur = isRaw ? '1.5' : '0'
  const noiseOpacity = isRaw ? '0.35' : '0.04'

  let color1 = '#0F1420'
  let color2 = '#1E293B'
  let hotColor1 = '#FF6B00'
  let hotColor2 = '#FFB800'
  let accentColor = '#00F0FF'

  if (type === 'inferno') {
    color1 = '#000004'; color2 = '#420A68'; hotColor1 = '#932667'; hotColor2 = '#FCA636'
  } else if (type === 'magma') {
    color1 = '#000004'; color2 = '#3B0F70'; hotColor1 = '#8C2981'; hotColor2 = '#FCFDBF'
  } else if (type === 'plasma') {
    color1 = '#0D0887'; color2 = '#7E03A8'; hotColor1 = '#CC4778'; hotColor2 = '#F89540'
  } else if (type === 'viridis') {
    color1 = '#440154'; color2 = '#31688E'; hotColor1 = '#35B779'; hotColor2 = '#FDE724'
  } else if (type === 'jet') {
    color1 = '#0000FF'; color2 = '#00FFFF'; hotColor1 = '#FFFF00'; hotColor2 = '#FF0000'
  } else if (type === 'rainbow') {
    color1 = '#091026'; color2 = '#D4881A'; hotColor1 = '#E85F1C'; hotColor2 = '#FF2A14'
  }

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="800" height="500">
    <defs>
      <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="${color1}"/>
        <stop offset="50%" stop-color="${color2}"/>
        <stop offset="100%" stop-color="${color1}"/>
      </linearGradient>
      <radialGradient id="hotspot1" cx="30%" cy="35%" r="35%">
        <stop offset="0%" stop-color="${hotColor2}" stop-opacity="0.95"/>
        <stop offset="45%" stop-color="${hotColor1}" stop-opacity="0.75"/>
        <stop offset="100%" stop-color="${color2}" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="hotspot2" cx="72%" cy="62%" r="28%">
        <stop offset="0%" stop-color="${hotColor2}" stop-opacity="0.9"/>
        <stop offset="50%" stop-color="${hotColor1}" stop-opacity="0.65"/>
        <stop offset="100%" stop-color="${color2}" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="hotspot3" cx="48%" cy="75%" r="22%">
        <stop offset="0%" stop-color="${hotColor2}" stop-opacity="0.85"/>
        <stop offset="100%" stop-color="${color1}" stop-opacity="0"/>
      </radialGradient>
      <filter id="blurFilter">
        <feGaussianBlur stdDeviation="${filterBlur}"/>
      </filter>
      <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="${accentColor}" stroke-width="0.3" stroke-opacity="0.25"/>
      </pattern>
    </defs>

    <!-- Base Thermal Gradient -->
    <rect width="800" height="500" fill="url(#bg)"/>

    <!-- Thermal Anomalies & Terrain Plumes -->
    <g filter="url(#blurFilter)">
      <ellipse cx="240" cy="180" rx="140" ry="95" fill="url(#hotspot1)"/>
      <ellipse cx="570" cy="310" rx="115" ry="85" fill="url(#hotspot2)"/>
      <ellipse cx="380" cy="380" rx="90" ry="60" fill="url(#hotspot3)"/>
      <path d="M 120 400 Q 250 250 400 320 T 700 220" fill="none" stroke="${hotColor1}" stroke-width="28" stroke-linecap="round" stroke-opacity="0.45"/>
    </g>

    <!-- Synthetic Noise Overlay for Raw vs Crisp for Enhanced -->
    <rect width="800" height="500" fill="${color2}" opacity="${noiseOpacity}"/>

    <!-- Coordinate Grid & HUD Crosshairs -->
    <rect width="800" height="500" fill="url(#grid)"/>

    <!-- High-tech HUD Telemetry Watermark -->
    <g font-family="monospace" font-size="11" fill="${accentColor}" opacity="0.65">
      <text x="24" y="32">ISRO // CHANDRA-09 THERMAL RADIOMETRY // BAND IR-8.4µm</text>
      <text x="24" y="474">LAT: 18°24'N // LON: 84°12'E // ALT: 540 KM // MODE: ${type.toUpperCase()}</text>
      <text x="640" y="32">GAIN: +14.2dB</text>
      <text x="640" y="474">TIMESTAMP: T+00:14:42</text>
    </g>

    <!-- Target Reticles -->
    <g stroke="${accentColor}" stroke-width="1" opacity="0.45">
      <line x1="230" y1="180" x2="250" y2="180"/>
      <line x1="240" y1="170" x2="240" y2="190"/>
      <circle cx="240" cy="180" r="18" fill="none" stroke-dasharray="3,3"/>
      
      <line x1="560" y1="310" x2="580" y2="310"/>
      <line x1="570" y1="300" x2="570" y2="320"/>
      <circle cx="570" cy="310" r="15" fill="none" stroke-dasharray="3,3"/>
    </g>
  </svg>`

  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`
}

export const CHANDRA_09_DEMO_DATA: ImageData = {
  upload_id: 'chandra-09-ir-sample-8842',
  filename: 'CHANDRA09_THERMAL_SECTOR_T88.TIFF',
  file_path: 'uploads/raw/enhanced_ai.jpg',
  resolution: '3840 x 2160 (4K UHD Thermal)',
  channels: 1,
  format: '16-bit Radiometric TIFF',
  original_image: 'uploads/raw/enhanced_ai.jpg',
  preprocessed_image: 'uploads/raw/enhanced_ai.jpg',
  enhanced_image: 'outputs/verified_isro/step1_4k_enhanced.jpg',
  colorized_image: 'outputs/verified_isro/step2_true_color.jpg',
  detected_image: 'outputs/detected/enhanced_ai.jpg',
  processed_image: 'outputs/detected/enhanced_ai.jpg',
  report_path: 'reports/CHANDRA_09_FULL_MISSION_REPORT.pdf',
  detections: [
    {
      id: 'det-101',
      class: 'SPACECRAFT MAIN BUS',
      confidence: 0.942,
      x: 0.52,
      y: 0.45,
      width: 0.22,
      height: 0.18,
    },
    {
      id: 'det-102',
      class: 'SOLAR ARRAY WING (PORT)',
      confidence: 0.918,
      x: 0.27,
      y: 0.52,
      width: 0.25,
      height: 0.24,
    },
    {
      id: 'det-103',
      class: 'SOLAR ARRAY WING (STARBOARD)',
      confidence: 0.895,
      x: 0.53,
      y: 0.14,
      width: 0.14,
      height: 0.33,
    },
    {
      id: 'det-104',
      class: 'OPTICAL SENSOR APERTURE',
      confidence: 0.885,
      x: 0.65,
      y: 0.50,
      width: 0.08,
      height: 0.09,
    },
    {
      id: 'det-105',
      class: 'THERMAL RADIATOR PANEL',
      confidence: 0.867,
      x: 0.61,
      y: 0.61,
      width: 0.23,
      height: 0.25,
    },
  ],
  analysis: `🎯 ISRO CHANDRA-09 MULTIMODAL THERMAL SCENE INTELLIGENCE BRIEFING

1. RADIOMETRIC PROFILE & ANOMALY DETECTION:
High-resolution mid-wave infrared (MWIR 8.4µm) scan identifies a primary localized thermal plume (+44.2°C over ambient 182K lunar/orbital terrain floor) centered at coordinates [X:130, Y:100]. Emission signature matches active cryo-regulator dissipation.

2. AI SUPER-RESOLUTION ENHANCEMENT GAIN:
Deep residual neural super-resolution pipeline successfully reconstructed sub-pixel edge boundaries. Signal-to-Noise Ratio (PSNR) improved by +8.42 dB (from 30.0 dB to 38.42 dB), achieving a Structural Similarity Index (SSIM) of 0.942.

3. YOLOv8 TARGET TELEMETRY SUMMARY:
• Target #101 [THERMAL-ANOMALY]: 96.4% confidence — High thermal gradient plume.
• Target #102 [STRUCTURE]: 91.2% confidence — Stationary orbital habitat / shield structure.
• Target #103 [VEHICLE]: 89.1% confidence — Automated surface exploration unit.
• Target #104 [VESSEL]: 86.0% confidence — Auxiliary transport module.`,
  metrics: {
    psnr: 38.42,
    ssim: 0.942,
    processing_time: 342,
  },
}
