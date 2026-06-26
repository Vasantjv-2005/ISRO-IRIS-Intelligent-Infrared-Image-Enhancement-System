## BACKEND FOLDER STRUCTURE
backend/
├── app/                        # Main FastAPI application package
│   ├── ai_models/              # AI model loading, inference wrappers, and Gemini API client
│   │   ├── colorization_model.py
│   │   ├── enhancement_model.py
│   │   ├── gemini_client.py
│   │   ├── inference.py
│   │   ├── model_loader.py
│   │   └── yolov8_model.py
│   ├── api/                    # API Routers and Route Endpoints
│   │   ├── routes/             # Feature-specific endpoints (upload, colorization, report, etc.)
│   │   └── router.py           # Main API router combining all routes
│   ├── core/                   # Security, settings, and logging configurations
│   ├── database/               # Database connection managers (MongoDB)
│   ├── middleware/             # CORS, global exceptions, and request loggers
│   ├── models/                 # MongoDB collections/documents schemas (ODM)
│   ├── schemas/                # Pydantic request/response validation schemas
│   ├── services/               # Core business logic services
│   │   ├── ai/                 # Core AI service wrappers (YOLO, Enhancement, scene analysis)
│   │   ├── dashboard/          # Dashboard analytics & comparison service
│   │   ├── download/           # Download management
│   │   ├── preprocessing/      # Preprocessors (contrast, noise reduction, crop, normalization)
│   │   ├── session/            # User sessions management
│   │   ├── storage/            # File storage handlers (saving images & reports)
│   │   └── upload/             # Upload handling & validations
│   ├── utils/                  # Miscellaneous helper utilities (image processing, file helper, formatting)
│   └── dependencies.py         # FastAPI dependency injection definitions
├── prompts/                    # LLM System Prompts (e.g., scene_analysis_prompt.txt)
├── tests/                      # Automated unit test suite
├── weights/                    # Local storage folder for AI model weight files (.pt, .pth)
├── uploads/                    # Temporary storage for uploaded source files (ignored by git)
├── outputs/                    # Temporary storage for generated results/reports (ignored by git)
├── static/                     # Static files directory
├── Dockerfile                  # Container configuration for the backend service
├── docker-compose.yml          # Docker compose file for multi-container orchestration
├── requirements.txt            # Python packages dependencies
├── .env.example                # Example environment configuration file
└── README.md                   # Backend README documentation
