"""
Comparison Service

Provides image comparison functionality between original and processed images,
generating similarity scores and side-by-side comparison images.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from app.core.config import COMPARISON_FOLDER
from app.models.comparison_model import ComparisonModel, ComparisonStatus
from app.repositories.comparison_repository import comparison_repository
from app.repositories.upload_repository import upload_repository
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class ComparisonService:
    """
    Service responsible for comparing original and processed infrared images.
    """

    COLLECTION = "comparisons"

    async def compare(
        self,
        db: Any,
        upload_id: str,
    ) -> ComparisonModel:
        """
        Compare the original and processed image for an upload.

        Args:
            db: Optional database reference (ignored; kept for API compatibility).
            upload_id: The unique identifier of the upload.

        Returns:
            The created or updated ComparisonModel.
        """
        start_time = time.time()

        upload_doc = await upload_repository.get_by_upload_id(upload_id)
        if not upload_doc:
            raise FileNotFoundError(f"Upload with ID {upload_id} not found.")

        original_path = upload_doc.file_path
        processed_path = original_path  # Default fallback
        orig_file = Path(original_path)

        from app.core.config import COLORIZED_FOLDER, ENHANCED_FOLDER

        colorized_file = COLORIZED_FOLDER / orig_file.name
        enhanced_file = ENHANCED_FOLDER / orig_file.name

        if colorized_file.exists():
            processed_path = str(colorized_file)
        elif enhanced_file.exists():
            processed_path = str(enhanced_file)

        img1 = cv2.imread(str(original_path))
        img2 = cv2.imread(str(processed_path))

        if img1 is None or img2 is None:
            raise FileNotFoundError(
                f"Could not load original ({original_path}) or processed ({processed_path}) images."
            )

        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        if (h1, w1) != (h2, w2):
            img2_resized = cv2.resize(img2, (w1, h1))
        else:
            img2_resized = img2

        hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
        hist2 = cv2.calcHist([img2_resized], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)

        similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        similarity_score = max(0.0, min(1.0, (similarity + 1.0) / 2.0))

        comparison_img = np.hstack((img1, img2_resized))

        COMPARISON_FOLDER.mkdir(parents=True, exist_ok=True)
        comparison_filename = f"compare_{orig_file.stem}.jpg"
        comparison_path = COMPARISON_FOLDER / comparison_filename
        cv2.imwrite(str(comparison_path), comparison_img)

        processing_time = time.time() - start_time

        detected_objs = [str(obj) for obj in (upload_doc.objects_detected or [])]

        comparison = ComparisonModel(
            upload_id=upload_id,
            original_image_path=str(original_path),
            processed_image_path=str(processed_path),
            comparison_image_path=str(comparison_path),
            status=ComparisonStatus.COMPLETED,
            enhancement_applied=bool(upload_doc.enhancement_completed),
            colorization_applied=bool(upload_doc.colorization_completed),
            object_detection_applied=bool(upload_doc.detection_completed),
            scene_analysis_applied=bool(upload_doc.analysis_completed),
            detected_objects=detected_objs,
            total_objects=len(detected_objs),
            ai_summary=upload_doc.scene_summary,
            processing_time_seconds=processing_time,
            similarity_score=float(similarity_score),
        )

        await comparison_repository.upsert_by_upload_id(comparison)
        logger.info("Successfully compared and saved comparison for upload: %s", upload_id)
        return comparison

    async def get_comparison(
        self,
        db: Any,
        upload_id: str,
    ) -> ComparisonModel | None:
        """
        Get comparison details from repository by upload ID.

        Args:
            db: Optional database reference (ignored; kept for API compatibility).
            upload_id: The unique identifier of the upload.

        Returns:
            The found ComparisonModel or None.
        """
        return await comparison_repository.get_by_upload_id(upload_id)


comparison_service = ComparisonService()