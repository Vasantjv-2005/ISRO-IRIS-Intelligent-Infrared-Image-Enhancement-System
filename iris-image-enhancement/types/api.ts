export interface UploadResponseSchema {
  upload_id: string
  filename: string
  original_filename: string
  file_path: string
  file_size: number
  file_type: string
  mime_type: string
  status: string
  uploaded_at: string
  message: string
}

export interface SessionModel {
  session_id: string
  upload_id: string
  status?: string
  created_at?: string
  updated_at?: string
}

export interface PreprocessingRequestSchema {
  image_path: string
  output_directory: string
  apply_crop: boolean
}

export interface PreprocessingResponseSchema {
  success: boolean
  input_image: string
  output_image: string
  message?: string
  processing_time?: number
}

export interface EnhancementResponseSchema {
  success: boolean
  message: string
  input_image: string
  enhanced_image: string
}

export interface ColorizationResponseSchema {
  success: boolean
  backend: string
  input_image: string
  output_image: string
  colorized_image: string
  processing_time?: number
  message?: string
}

export interface BoundingBoxSchema {
  x1: number
  y1: number
  x2: number
  y2: number
}

export interface DetectionObjectSchema {
  class_id: number
  class_name: string
  confidence: number
  bbox: BoundingBoxSchema
}

export interface DetectionRequestSchema {
  image_path: string
  output_directory: string
  confidence: number
}

export interface DetectionResponseSchema {
  success: boolean
  image_path: string
  output_directory: string
  total_objects: number
  detections: DetectionObjectSchema[]
  message: string
}

export interface AnalysisRequestSchema {
  image_name: string
  detected_objects: DetectionObjectSchema[]
}

export interface AnalysisResponseSchema {
  success: boolean
  image: string
  analysis: string
  model: string
  total_detected_objects: number
  message: string
}

export interface ReportRequestSchema {
  image_name: string
  original_image_path?: string
  processed_image_path?: string
  colorized_image_path?: string
  detected_image_path?: string
  upload_id?: string
  detected_objects: DetectionObjectSchema[]
  analysis: string
}

export interface ReportResponseSchema {
  success: boolean
  report_path: string
  image_name: string
  generated_at: string
  total_detected_objects: number
  message: string
}

export interface DashboardStatisticsSchema {
  total_uploads: number
  total_processed_images: number
  total_reports_generated: number
  total_objects_detected: number
  total_completed_analysis: number
  total_failed_jobs: number
  active_sessions: number
  processing_success_rate: number
  average_processing_time_seconds: number
  storage_used_mb: number
}

export interface RecentActivitySchema {
  upload_id: string
  filename: string
  status: string
  uploaded_at: string
}

export interface SystemHealthSchema {
  backend_status: string
  database_status: string
  ai_model_status: string
  uptime: string
  last_updated: string
}

export interface DashboardResponseSchema {
  statistics: DashboardStatisticsSchema
  recent_activities: RecentActivitySchema[]
  recent_reports?: any[]
  system_health: SystemHealthSchema
}

export interface ComparisonRequestSchema {
  upload_id: string
}

export interface ComparisonResponseSchema {
  upload_id: string
  status: string
  original_image_path: string
  processed_image_path: string
  comparison_image_path: string
  enhancement_applied: boolean
  colorization_applied: boolean
  object_detection_applied: boolean
  scene_analysis_applied: boolean
  total_objects: number
  similarity_score: number
  processing_time_seconds: number
  created_at: string
}
