# 🚀 ISRO IRIS — Next-Generation Intelligent Infrared Image Enhancement & Interpretation System
## Master Frontend UI/UX Specification & AI System Prompt

You are an expert Principal Frontend Architect, UI/UX Designer, and Creative Technologist specializing in aerospace, scientific visualization, and high-performance AI command centers.

Your task is to build a breathtaking, award-winning, hyper-aesthetic web application for **IRIS (ISRO Intelligent Infrared Image Enhancement & Interpretation System)**. The backend is 100% complete and running locally on `http://127.0.0.1:8000`.

---

## 💎 1. DESIGN AESTHETICS & VISUAL WOW-FACTOR (CRITICAL PRIORITY)

The application MUST NOT look like a generic corporate template or simple CRUD app. At first glance, the user should feel like they have entered a **State-of-the-Art ISRO Deep-Space Thermal Imaging Command Center**.

### 🌌 A. Color Palette & Atmospheric Theme
- **Theme**: Premium Space Dark Mode / Atmospheric Glassmorphism.
- **Backgrounds**: Deep Obsidian Void (`#0B0E14`) layered with midnight aerospace navy (`#0F1420`) and subtle animated radial ambient glow gradients (electric cyan & deep nebula magenta).
- **Primary Accent Colors (Interactive & Brand)**:
  - **ISRO Electric Cyan** (`#00F0FF`): Primary action buttons, active tabs, laser slider dividers, glowing indicators.
  - **Quantum Teal** (`#00D2B4`): Secondary interactive states and success signals.
- **Thermal Spectrum Palette (Data & Overlays)**:
  - **Inferno Orange** (`#FF6B00`) & **Solar Amber** (`#FFB800`): High-temperature thermal alerts, object bounding box highlights, and warning states.
  - **Plasma Magenta** (`#E01E79`): Deep AI processing indicators and neural network status.
- **Surfaces & Glassmorphism**:
  - Frosted multi-layered glass cards (`backdrop-blur-xl`, `rgba(20, 27, 41, 0.65)` background).
  - Micro-borders: 1px subtle glowing border (`rgba(0, 240, 255, 0.15)`) that intensifies on card hover.

### ✍️ B. Typography
- **Primary Headings & UI Labels**: *Outfit* or *Inter* — clean, bold, modern geometry.
- **Telemetry, Coordinates, & Metrics**: *JetBrains Mono* or *Fira Code* — monospaced precision font for image resolutions, PSNR/SSIM scores, bounding box coordinates, and processing timers.

### ✨ C. Micro-Animations & Dynamic Feedback
- **Interactive Button States**: Glow expansions, magnetic hover effects, and crisp ripple transitions.
- **Pipeline Processing Animations**: Futuristic HUD scanning line across images during AI enhancement, spinning orbital progress rings, and real-time step indicators.
- **Interactive Image Viewers**: Smooth synchronized zooming, panning, and a glowing laser-edge comparison slider.

---

## 🏗️ 2. RECOMMENDED FRONTEND TECH STACK

- **Framework**: React 18+ (Next.js 14/15 App Router or Vite + TypeScript)
- **Styling**: Tailwind CSS v3/v4 + Framer Motion (for fluid micro-animations & layout transitions) + Lucide Icons
- **Image Visualization & Canvas**:
  - HTML5 `<canvas>` / WebGL for interactive bounding box overlays and synchronized zoom/pan.
  - Custom Before/After Split-Screen Image Comparison Slider.
- **HTTP Client & State Management**: Axios / TanStack React Query for robust backend API synchronization, caching, and loading states.
- **Chart Visualization**: Recharts or Chart.js for real-time dashboard telemetry and metric charts.

---

## 🔌 3. COMPLETE BACKEND API INTEGRATION MAP

Base URL: `http://127.0.0.1:8000`

### A. Authentication & User Sessions (`/auth`)
- `POST /auth/register`: `{ full_name, email, password, confirm_password }` → Returns JWT access token & user profile.
- `POST /auth/login`: `{ email, password }` → Returns JWT access token.
- **UI Requirement**: Sleek glassmorphic Auth Modal / Portal with instant feedback and session persistence.

### B. System Health & Dashboard Telemetry (`/health`, `/dashboard/`)
- `GET /health`: Diagnostics on MongoDB connection and AI model availability.
- `GET /dashboard/`: Returns total images processed, AI model performance statistics, activity timelines, and system health status.
- **UI Requirement**:
  - **Live Header HUD**: Shows real-time server connection status indicator (Green pulse) and system ping.
  - **Executive Analytics Dashboard**: Interactive KPI cards (Total Uploads, Detections, Average Processing Time, Similarity Index) and recent activity log.

### C. Infrared Image Upload & Preprocessing (`/upload/`, `/preprocessing/process`)
- `POST /upload/`: Multipart file upload (`UploadFile`) → Returns `upload_id`, `filename`, `file_path`, resolution, channels, and format.
- `POST /preprocessing/process`: `{ image_path, output_directory, apply_denoise, apply_contrast, ... }`
- **UI Requirement**:
  - **Futuristic Dropzone**: Animated dashed glowing border, drag-and-drop support for infrared thermal imagery (`.png`, `.jpg`, `.tiff`), and instant EXIF / image property inspector card.

### D. Deep AI Enhancement & Super-Resolution (`/enhancement/process`)
- `POST /enhancement/process?image_path=...`: Executes deep AI super-resolution and thermal sharpness enhancement.
- **UI Requirement**: Dedicated "AI Enhance" action panel showing original thermal noise vs AI-enhanced clarity.

### E. Multi-Palette AI Colorization (`/colorization/process`)
- `POST /colorization/process`: Query parameters:
  - `image_path`: Path to uploaded infrared image
  - `colormap`: Choice of thermal palette (`inferno`, `magma`, `plasma`, `viridis`, `jet`, `rainbow`)
  - `super_resolution`: boolean (`true` / `false`)
  - `backend`: AI engine selection (`huggingface`, `deoldify`, `palette`, `torchvision`, `stablediffusion`, `deep_learning`)
- **UI Requirement**:
  - **Interactive Thermal Palette Selector**: Visual color gradient chips for each colormap so users can instantly preview aesthetic palette shifts.
  - **AI Engine Dropdown**: Clearly display the active neural backend.

### F. YOLOv8 Thermal Object Detection (`/detection/process`)
- `POST /detection/process`: JSON body `{ image_path, output_directory, confidence }`
- **UI Requirement**:
  - **Interactive Bounding Box Overlay Canvas**: Render detected bounding boxes over the thermal image with interactive hover tooltips (showing Class Name, e.g., *Vehicle / Vessel / Thermal Anomaly / Structure*, and Confidence %).
  - **Confidence Threshold Slider**: Real-time slider (0.10 to 0.95) allowing users to filter detection sensitivity.

### G. Gemini AI Multimodal Scene Analysis (`/analysis/process`)
- `POST /analysis/process`: JSON body `{ image_path, context, prompt }`
- **UI Requirement**:
  - **Mission Briefing Intelligence Card**: Display structured natural-language scene interpretation from Gemini AI. Include typing/typewriter stream animation, tactical summary badges, and copy/export actions.

### H. Synchronized Before/After Comparison & Verification (`/comparison/compare`)
- `POST /comparison/compare`: JSON body `{ upload_id }` → Returns `similarity_score`, `processing_time_seconds`, and paths to original vs processed images.
- **UI Requirement**:
  - **Laser Comparison Slider**: Interactive draggable divider line showing the raw infrared feed on the left and the fully processed/colorized/enhanced image on the right.
  - **Visual Telemetry Gauges**: Circular progress or digital readout cards for Structural Similarity (SSIM) and PSNR.

### I. Mission Report Generation & Download (`/report/generate`, `/download/`)
- `POST /report/generate`: JSON body `{ upload_id, title, notes, include_detections, include_analysis }` → Generates professional ISRO PDF dossier.
- `GET /download/?file_path=...`: Initiates file download.
- **UI Requirement**:
  - One-click **"Export ISRO Mission Dossier (PDF)"** button with animated completion checkmark and direct browser download trigger.

### J. Session & History Management (`/sessions/`)
- `POST /sessions/?upload_id=...`: Create session tracking object.
- `GET /sessions/`: List past processing sessions.
- `DELETE /sessions/{session_id}`: Delete session.
- **UI Requirement**:
  - **Mission History Drawer / Gallery**: Slide-over drawer or gallery grid displaying previous thermal analyses with thumbnail previews and quick reload capability.

---

## 🎨 4. APPLICATION LAYOUT & PAGE STRUCTURE

```
+-----------------------------------------------------------------------------------+
|  🛰️ ISRO IRIS COMMAND CENTER    [Dashboard] [Mission Workspace] [History]  [🟢 Live] |
+-----------------------------------------------------------------------------------+
|  LEFT PANEL: CONTROLS & PIPELINE       |  CENTER / RIGHT: VISUAL INTERPRETATION HUD   |
|                                        |                                           |
|  1. [Drop Zone / Image Selector]       |  +-------------------------------------+  |
|  2. Step 1: Preprocessing & Denoise    |  |                                     |  |
|  3. Step 2: AI Enhancement             |  |  Interactive Before/After Slider    |  |
|  4. Step 3: Colorization Palettes      |  |  & YOLOv8 Detection Canvas Overlay  |  |
|     [Inferno] [Magma] [Viridis] [Jet]  |  |                                     |  |
|  5. Step 4: Object Detection Filter    |  +-------------------------------------+  |
|  6. Step 5: Gemini AI Scene Analysis   |                                           |
|                                        |  +-------------------------------------+  |
|  [⚡ RUN FULL INTELLIGENT PIPELINE]    |  | 🧠 Gemini Mission Intelligence Card |  |
|  [📄 EXPORT MISSION REPORT PDF]        |  +-------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 🏆 5. STEP-BY-STEP IMPLEMENTATION INSTRUCTIONS FOR FRONTEND BUILDER

1. **Initialize Project**: Create a sleek React + TypeScript web application with Tailwind CSS and Lucide React icons.
2. **Setup Global Aesthetic Tokens**: Configure dark obsidian backgrounds (`#0B0E14`), neon cyan highlights (`#00F0FF`), custom scrollbars, and frosted glass utility classes (`backdrop-blur-xl`).
3. **Build API Service Layer**: Create an Axios service utility (`src/services/api.ts`) connecting to all 13 REST endpoints listed in Section 3.
4. **Develop Core Interactive Components**:
   - `InteractiveComparisonSlider`: Draggable split screen viewer.
   - `DetectionCanvasViewer`: Canvas overlay rendering bounding boxes with custom hover popups.
   - `ColormapPaletteSelector`: Responsive thermal gradient picker.
   - `GeminiAnalysisCard`: Aerospace-themed intelligence briefing panel.
5. **Add Sound & Visual Wow Details**: Subtle glowing pulse indicators, smooth accordion step transitions, and responsive layout scaling across all screen sizes.
