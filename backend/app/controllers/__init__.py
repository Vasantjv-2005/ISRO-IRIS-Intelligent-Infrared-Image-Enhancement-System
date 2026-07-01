"""
Controllers Package

Exports all application controllers.
"""

from app.controllers.analysis_controller import analysis_controller
from app.controllers.colorization_controller import colorization_controller
from app.controllers.detection_controller import detection_controller
from app.controllers.enhancement_controller import enhancement_controller
from app.controllers.health_controller import health_controller
from app.controllers.preprocessing_controller import preprocessing_controller
from app.controllers.report_controller import report_controller
from app.controllers.upload_controller import upload_controller

__all__ = [
    "analysis_controller",
    "colorization_controller",
    "detection_controller",
    "enhancement_controller",
    "health_controller",
    "preprocessing_controller",
    "report_controller",
    "upload_controller",
]
