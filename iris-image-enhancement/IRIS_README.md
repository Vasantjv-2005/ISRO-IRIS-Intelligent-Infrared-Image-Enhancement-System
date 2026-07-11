# 🛰️ ISRO IRIS - Thermal Imaging Command Center

## Overview

**IRIS** (Intelligent Infrared Image Enhancement & Interpretation System) is a state-of-the-art aerospace-grade web application for real-time thermal image processing, AI-powered object detection, and scene analysis. Built with a premium dark-mode aesthetic inspired by deep-space mission control centers.

### Key Features

✨ **Interactive Thermal Processing Pipeline**
- 6-step AI enhancement workflow
- Real-time progress tracking
- Drag-and-drop image upload with validation

🎨 **Advanced Visualization Suite**
- Interactive before/after comparison slider with synchronized zoom/pan
- Canvas-based bounding box overlay with YOLOv8 detection
- Multi-palette thermal colorization (Inferno, Magma, Plasma, Viridis, Jet, Rainbow)
- Real-time metric gauges (PSNR, SSIM, processing time, object count)

🧠 **AI-Powered Scene Analysis**
- Gemini multimodal AI for natural-language interpretation
- Typewriter streaming animation for analysis results
- Tactical summary badges and insights export

🎯 **Premium UI/UX Design**
- Electric cyan (#00F0FF) + thermal spectrum accents
- Glassmorphic cards with backdrop blur effects
- Smooth 60 FPS animations powered by Framer Motion
- Responsive layout scaling (mobile → desktop)
- Dark obsidian space aesthetic

---

## Tech Stack

### Frontend
- **Framework**: Next.js 16 + React 19 with App Router
- **Styling**: Tailwind CSS v4 with custom dark theme
- **Animations**: Framer Motion (smooth, performant interactions)
- **Icons**: Lucide React (24+ aerospace-themed icons)
- **HTTP Client**: Axios with interceptors for JWT auth
- **Charts**: Recharts (for future telemetry dashboards)

### State Management
- React Context API (Auth, Image, Pipeline contexts)
- No external state library needed for simplicity

### Architecture
- Component-based modular design
- API service layer abstraction (`lib/api.ts`)
- Custom hooks for auth & image processing
- Type-safe with full TypeScript support

---

## Project Structure

```
/vercel/share/v0-project/
├── app/
│   ├── layout.tsx              # Root layout with fonts & metadata
│   ├── page.tsx                # Main IRIS command center
│   └── globals.css             # Dark theme tokens & utilities
├── components/
│   ├── layout/
│   │   ├── Header.tsx          # Top bar with branding & status
│   │   └── PipelinePanel.tsx   # Left control panel with accordion steps
│   ├── visualization/
│   │   ├── UploadDropzone.tsx          # Animated drag-drop uploader
│   │   ├── ImageComparisonViewer.tsx   # Before/after slider
│   │   ├── ColormapPaletteSelector.tsx # 6 thermal palette picker
│   │   ├── GeminiAnalysisCard.tsx      # AI interpretation display
│   │   ├── DetectionCanvasOverlay.tsx  # Canvas-based bounding boxes
│   │   ├── MetricsGauge.tsx            # Animated metric cards
│   │   └── ActivityTimeline.tsx        # Recent activity log
│   └── ui/
│       ├── GlassCard.tsx       # Reusable glassmorphic container
│       ├── Badge.tsx           # Status & metadata badges
│       └── Spinner.tsx         # Orbital & dot loaders
├── lib/
│   ├── api.ts                  # Axios + endpoint definitions
│   └── context/
│       ├── AuthContext.tsx     # JWT token & user state
│       ├── ImageContext.tsx    # Current image & metadata
│       └── PipelineContext.tsx # Pipeline step tracking
├── hooks/
│   └── (custom React hooks for reuse)
└── types/
    └── index.ts                # TypeScript interfaces
```

---

## Component Showcase

### 1. Header Component
- **ISRO IRIS** branding with animated satellite icon
- Navigation tabs (Dashboard, Workspace, History)
- Live server status indicator with ping latency
- User info & logout button

```typescript
<Header />
```

### 2. Pipeline Panel (Left Sidebar)
- **Step-by-step accordion** with expandable controls
- Real-time progress bar (0/6 steps)
- Preprocessing toggles (denoise, contrast)
- AI enhancement slider
- Colormap quick selector
- Detection confidence threshold
- Gemini context input

### 3. Image Comparison Viewer
- Draggable vertical divider with laser-edge glow
- Synchronized zoom/pan between before and after
- Before/After labels with backdrop blur background
- Smooth transitions & hover effects

### 4. Metrics Gauges
- **PSNR**: Peak Signal-to-Noise Ratio (dB)
- **SSIM**: Structural Similarity Index (0-1 score)
- **Processing Time**: Real-time timer (ms)
- **Object Count**: Detected thermal objects

Each gauge features:
- Animated value counters
- Gradient progress bars
- Color-coded variants (primary, secondary, accent, warning)
- Icon indicators

### 5. Thermal Colormap Selector
6 professional palettes with hover previews:
- **Inferno** - Classic hot-to-cold thermal
- **Magma** - Perceptually uniform
- **Plasma** - High contrast spectrum
- **Viridis** - Optimal perception
- **Jet** - Traditional thermal map
- **Rainbow** - Full spectrum

### 6. Gemini Analysis Card
- Spinning brain icon animation
- Typewriter text streaming effect
- Copy-to-clipboard button with success feedback
- Tactical summary badges
- Error retry mechanism
- Responsive height based on content

### 7. Detection Canvas Overlay
- Real-time canvas rendering of bounding boxes
- Class-specific colors (Vehicle, Vessel, Anomaly, etc.)
- Interactive hover with confidence display
- Glow effects for enhanced visibility
- Confidence threshold slider support

---

## API Integration Map

All endpoints connect to backend at `http://127.0.0.1:8000`:

| Endpoint | Purpose | UI Component |
|----------|---------|--------------|
| `/auth/register` | User registration | (Future Auth Modal) |
| `/auth/login` | User login | (Future Auth Modal) |
| `/health` | System diagnostics | Header Status Badge |
| `/dashboard/` | Analytics data | (Future Dashboard) |
| `/upload/` | Image upload | UploadDropzone |
| `/preprocessing/process` | Denoise & contrast | Step 2 Controls |
| `/enhancement/process` | AI super-resolution | Step 3 Slider |
| `/colorization/process` | Thermal palettes | Step 4 Selector |
| `/detection/process` | YOLOv8 detection | DetectionCanvasOverlay |
| `/analysis/process` | Gemini scene analysis | GeminiAnalysisCard |
| `/comparison/compare` | SSIM/PSNR metrics | Metrics Gauges |
| `/report/generate` | PDF mission dossier | (Export Button) |
| `/sessions/` | History management | (Activity Timeline) |

---

## Design System

### Color Palette
- **Primary**: ISRO Electric Cyan `#00F0FF`
- **Secondary**: Quantum Teal `#00D2B4`
- **Accent**: Plasma Magenta `#E01E79`
- **Background**: Obsidian Void `#0B0E14`
- **Thermal Orange**: `#FF6B00` (alerts)
- **Solar Amber**: `#FFB800` (warnings)

### Typography
- **Headings**: Inter (modern, clean geometry)
- **Body**: Inter (consistent, readable)
- **Monospace**: JetBrains Mono (precision telemetry)

### Spacing & Radius
- Grid-based spacing: 4px, 8px, 12px, 16px, 20px, 24px
- Border radius: 8px (sm), 12px (md), 16px (lg), 20px (xl)

### Animations
- Entrance: Fade + slide (200-300ms)
- Hover: Scale + glow (150ms)
- Loading: Orbital rings, dot pulse
- Transitions: Easing (ease-out for snappy feel)

---

## Getting Started

### Installation
```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev

# Build for production
pnpm build
pnpm start

# Run type checking
pnpm tsc --noEmit
```

### Environment Variables
```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

# Optional: Gemini API key
NEXT_PUBLIC_GEMINI_API_KEY=your_key_here
```

### First Run
1. Open `http://localhost:3000`
2. Drag a thermal image (.png, .jpg, .tiff) onto the upload dropzone
3. Click through the 6-step pipeline
4. View metrics and AI analysis in real-time
5. Export mission report (PDF)

---

## Advanced Features

### State Management Flow
```
AuthContext → JWT token + user profile
  ↓
ImageContext → Current image + processing metadata
  ↓
PipelineContext → Step tracking + settings (colormap, confidence, etc.)
  ↓
API Layer → HTTP calls with auto-token injection
  ↓
Components → Real-time UI updates
```

### Performance Optimizations
- Canvas rendering debounced during zoom/pan
- Image lazy loading with blur placeholders
- Framer Motion GPU-accelerated animations
- React.memo for comparison slider components
- No unnecessary re-renders via useCallback hooks

### Accessibility
- Semantic HTML (main, header, nav)
- ARIA labels on interactive elements
- Keyboard navigation support
- High contrast text (WCAG AA+)
- Screen reader friendly

---

## Future Enhancements

🚀 **Planned Features**
- Authentication flow (login/register modals)
- Mission history dashboard with search/filter
- Multi-image batch processing
- Real-time WebSocket updates for long operations
- Export to multiple formats (PNG, PDF, GeoTIFF)
- Custom thermal palette creator
- 3D thermal visualization (Three.js/R3F)
- Dark mode toggle (already dark, add light mode)
- Mobile app (React Native)

---

## Troubleshooting

### Application not loading?
1. Check if backend is running: `curl http://127.0.0.1:8000/health`
2. Verify `NEXT_PUBLIC_API_URL` environment variable
3. Clear browser cache and reload

### Images not uploading?
1. Verify file format: PNG, JPEG, TIFF only
2. Check file size < 50MB
3. Confirm backend is accepting multipart requests

### Animations are laggy?
1. Check browser hardware acceleration is enabled
2. Reduce number of simultaneous animations
3. Profile with Chrome DevTools Performance tab

### Metrics not updating?
1. Verify API endpoints are callable
2. Check browser console for CORS errors
3. Ensure JWT token is valid

---

## License & Attribution

Built with ❤️ for ISRO's thermal imaging initiatives.

**Tech Stack Credits:**
- Next.js / React (Vercel)
- Tailwind CSS (JIT)
- Framer Motion (animation library)
- Lucide React (icons)
- Axios (HTTP client)

---

## Contact & Support

For questions or feature requests, contact the IRIS development team.

**Status**: 🟢 Active Development
**Last Updated**: December 2024
**Version**: 1.0.0-alpha

---

Made with 🛰️ for aerospace thermal imaging excellence.
