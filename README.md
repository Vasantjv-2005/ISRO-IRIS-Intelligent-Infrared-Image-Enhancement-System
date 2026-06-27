# IRIS - Intelligent Infrared Image Enhancement & Interpretation System

## Backend Folder Structure

```text
backend/
│
├── app/
│   │
│   ├── main.py
│   ├── dependencies.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── routes/
│   │       ├── health.py
│   │       ├── upload.py
│   │       ├── preprocessing.py
│   │       ├── enhancement.py
│   │       ├── colorization.py
│   │       ├── detection.py
│   │       ├── analysis.py
│   │       ├── report.py
│   │       ├── comparison.py
│   │       ├── dashboard.py
│   │       ├── download.py
│   │       └── session.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── logging.py
│   │   ├── security.py
│   │   └── settings.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── mongodb.py
│   │   └── indexes.py
│   │
│   ├── middleware/
│   │   ├── cors.py
│   │   ├── error_handler.py
│   │   ├── request_logger.py
│   │   └── exception_handler.py
│   │
│   ├── models/
│   │   ├── image_model.py
│   │   ├── report_model.py
│   │   ├── comparison_model.py
│   │   ├── analysis_model.py
│   │   ├── dashboard_model.py
│   │   └── session_model.py
│   │
│   ├── schemas/
│   │   ├── upload_schema.py
│   │   ├── preprocessing_schema.py
│   │   ├── enhancement_schema.py
│   │   ├── colorization_schema.py
│   │   ├── detection_schema.py
│   │   ├── analysis_schema.py
│   │   ├── report_schema.py
│   │   ├── comparison_schema.py
│   │   ├── dashboard_schema.py
│   │   └── response_schema.py
│   │
│   ├── services/
│   │   ├── upload/
│   │   │   ├── upload_service.py
│   │   │   └── validation_service.py
│   │   │
│   │   ├── preprocessing/
│   │   │   ├── crop_service.py
│   │   │   ├── resize_service.py
│   │   │   ├── noise_reduction.py
│   │   │   ├── contrast_enhancement.py
│   │   │   └── normalization.py
│   │   │
│   │   ├── ai/
│   │   │   ├── enhancement_service.py
│   │   │   ├── colorization_service.py
│   │   │   ├── object_detection_service.py
│   │   │   ├── scene_analysis_service.py
│   │   │   └── report_generation_service.py
│   │   │
│   │   ├── dashboard/
│   │   │   ├── dashboard_service.py
│   │   │   └── comparison_service.py
│   │   │
│   │   ├── storage/
│   │   │   ├── image_storage.py
│   │   │   ├── report_storage.py
│   │   │   └── metadata_storage.py
│   │   │
│   │   ├── download/
│   │   │   └── download_service.py
│   │   │
│   │   └── session/
│   │       └── session_service.py
│   │
│   ├── ai_models/
│   │   ├── model_loader.py
│   │   ├── enhancement_model.py
│   │   ├── colorization_model.py
│   │   ├── yolov8_model.py
│   │   ├── gemini_client.py
│   │   └── inference.py
│   │
│   ├── utils/
│   │   ├── image_utils.py
│   │   ├── file_utils.py
│   │   ├── report_utils.py
│   │   ├── validation_utils.py
│   │   ├── helper.py
│   │   ├── logger.py
│   │   └── response.py
│
├── uploads/
│   ├── raw/
│   ├── validated/
│   ├── resized/
│   └── temp/
│
├── outputs/
│   ├── enhanced/
│   ├── colorized/
│   ├── detected/
│   ├── analyzed/
│   ├── reports/
│   ├── comparisons/
│   └── final/
│
├── prompts/
│   └── scene_analysis_prompt.txt
│
├── weights/
│   ├── enhancement_model.pth
│   ├── colorization_model.pth
│   └── yolov8.pt
│
├── static/
├── tests/
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Backend Modules

- **API** – REST API endpoints using FastAPI.
- **Core** – Application configuration and settings.
- **Database** – MongoDB connection and database operations.
- **Middleware** – Error handling, CORS, and request logging.
- **Models** – Database models.
- **Schemas** – Request and response validation using Pydantic.
- **Services** – Business logic for image processing and AI workflows.
- **AI Models** – Image enhancement, colorization, object detection, and scene analysis.
- **Utils** – Helper functions and reusable utilities.
- **Uploads** – Stores uploaded infrared images.
- **Outputs** – Stores processed images, reports, and results.
- **Prompts** – Gemini prompts for scene understanding.
- **Weights** – AI model weight files.
- **Tests** – Unit and integration tests.

---

## Technology Stack

- **Backend:** FastAPI, Python
- **Database:** MongoDB Atlas
- **AI Models:** PyTorch, YOLOv8, Gemini API
- **Image Processing:** OpenCV, Pillow, NumPy
- **PDF Reports:** ReportLab
- **Containerization:** Docker
- **Version Control:** Git & GitHub
