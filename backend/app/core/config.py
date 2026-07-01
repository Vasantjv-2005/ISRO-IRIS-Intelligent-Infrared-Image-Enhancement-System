"""
Application Configuration

Provides centralized access to project
configuration and application paths.
"""

from pathlib import Path

from app.core.settings import settings

# =====================================================
# Project
# =====================================================

PROJECT_NAME = settings.PROJECT_NAME

PROJECT_DESCRIPTION = settings.PROJECT_DESCRIPTION

PROJECT_VERSION = settings.PROJECT_VERSION

# =====================================================
# API
# =====================================================

API_PREFIX = settings.API_PREFIX

# =====================================================
# Server
# =====================================================

HOST = settings.HOST

PORT = settings.PORT

DEBUG = settings.DEBUG

# =====================================================
# MongoDB
# =====================================================

MONGODB_URI = settings.MONGODB_URI

DATABASE_NAME = settings.DATABASE_NAME

# =====================================================
# Gemini
# =====================================================

GEMINI_API_KEY = settings.GEMINI_API_KEY

# =====================================================
# Upload Configuration
# =====================================================

MAX_FILE_SIZE = settings.MAX_FILE_SIZE

ALLOWED_IMAGE_TYPES = settings.ALLOWED_IMAGE_TYPES

# =====================================================
# Base Directory
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =====================================================
# Upload Directories
# =====================================================

UPLOAD_FOLDER = BASE_DIR / "uploads" / "raw"

VALIDATED_FOLDER = BASE_DIR / "uploads" / "validated"

RESIZED_FOLDER = BASE_DIR / "uploads" / "resized"

TEMP_FOLDER = BASE_DIR / "uploads" / "temp"

# =====================================================
# Output Directories
# =====================================================

OUTPUT_FOLDER = BASE_DIR / "outputs"

ENHANCED_FOLDER = OUTPUT_FOLDER / "enhanced"

COLORIZED_FOLDER = OUTPUT_FOLDER / "colorized"

DETECTED_FOLDER = OUTPUT_FOLDER / "detected"

ANALYZED_FOLDER = OUTPUT_FOLDER / "analyzed"

REPORTS_FOLDER = OUTPUT_FOLDER / "reports"

COMPARISON_FOLDER = OUTPUT_FOLDER / "comparisons"

FINAL_FOLDER = OUTPUT_FOLDER / "final"

# =====================================================
# AI Models
# =====================================================

WEIGHTS_FOLDER = BASE_DIR / "weights"

YOLO_MODEL_PATH = BASE_DIR / settings.YOLO_MODEL_PATH

COLORIZATION_MODEL_PATH = BASE_DIR / settings.COLORIZATION_MODEL_PATH

ENHANCEMENT_MODEL_PATH = BASE_DIR / settings.ENHANCEMENT_MODEL_PATH

COLORIZATION_BACKEND = settings.COLORIZATION_BACKEND

ENHANCEMENT_BACKEND = settings.ENHANCEMENT_BACKEND

# =====================================================
# Create Required Directories
# =====================================================

DIRECTORIES = [
    UPLOAD_FOLDER,
    VALIDATED_FOLDER,
    RESIZED_FOLDER,
    TEMP_FOLDER,
    ENHANCED_FOLDER,
    COLORIZED_FOLDER,
    DETECTED_FOLDER,
    ANALYZED_FOLDER,
    REPORTS_FOLDER,
    COMPARISON_FOLDER,
    FINAL_FOLDER,
]

for directory in DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)