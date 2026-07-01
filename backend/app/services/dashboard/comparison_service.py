"""
Comparison Service

Provides image comparison functionality between original and processed images,
generating similarity scores and side-by-side comparison images.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import COMPARISON_FOLDER
from app.models.comparison_model import ComparisonModel, ComparisonStatus

logger = logging.getLogger("iris")


class ComparisonService:
    """
    Service responsible for comparing original and processed infrared images.
    """

    COLLECTION = "comparisons"

    async def compare(
        self,
        db: AsyncIOMotorDatabase,
        upload_id: str,
    ) -> ComparisonModel:
        """
        Compare the original and processed image for an upload.
        """
        start_time = time.time()

        # Find upload
        upload_doc = await db["uploads"].find_one({"upload_id": upload_id})
        if not upload_doc:
            # Check by _id if upload_id wasn't stored
            upload_doc = await db["uploads"].find_one({"_id": upload_id})

        if not upload_doc:
            raise FileNotFoundError(f"Upload with ID {upload_id} not found.")

        original_path = upload_doc.get("file_path")
        processed_path = original_path  # Default fallback
        orig_file = Path(original_path)

        # Check in outputs/colorized/ or uploads/colorized/ or check UPLOAD_FOLDER config
        from app.core.config import COLORIZED_FOLDER, ENHANCED_FOLDER
        
        colorized_file = COLORIZED_FOLDER / orig_file.name
        enhanced_file = ENHANCED_FOLDER / orig_file.name
        
        if colorized_file.exists():
            processed_path = str(colorized_file)
        elif enhanced_file.exists():
            processed_path = str(enhanced_file)

        # Load images with OpenCV
        img1 = cv2.imread(str(original_path))
        img2 = cv2.imread(str(processed_path))

        if img1 is None or img2 is None:
            raise FileNotFoundError(
                f"Could not load original ({original_path}) or processed ({processed_path}) images."
            )

        # Ensure same size for calculations
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        if (h1, w1) != (h2, w2):
            img2_resized = cv2.resize(img2, (w1, h1))
        else:
            img2_resized = img2

        # Calculate similarity score using histogram comparison (correlation)
        hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
        hist2 = cv2.calcHist([img2_resized], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
        
        similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        # normalize correlation from [-1, 1] to [0, 1]
        similarity_score = max(0.0, min(1.0, (similarity + 1.0) / 2.0))

        # Generate comparison side-by-side visualization
        comparison_img = np.hstack((img1, img2_resized))
        
        # Save comparison image
        COMPARISON_FOLDER.mkdir(parents=True, exist_ok=True)
        comparison_filename = f"compare_{orig_file.stem}.jpg"
        comparison_path = COMPARISON_FOLDER / comparison_filename
        cv2.imwrite(str(comparison_path), comparison_img)

        processing_time = time.time() - start_time

        # Build comparison model
        comparison = ComparisonModel(
            upload_id=upload_id,
            original_image_path=str(original_path),
            processed_image_path=str(processed_path),
            comparison_image_path=str(comparison_path),
            status=ComparisonStatus.COMPLETED,
            enhancement_applied=upload_doc.get("enhancement_completed", False),
            colorization_applied=upload_doc.get("colorization_completed", False),
            object_detection_applied=upload_doc.get("detection_completed", False),
            scene_analysis_applied=upload_doc.get("analysis_completed", False),
            detected_objects=[str(obj) for obj in upload_doc.get("objects_detected", [])],
            total_objects=len(upload_doc.get("objects_detected", [])),
            ai_summary=upload_doc.get("scene_summary"),
            processing_time_seconds=processing_time,
            similarity_score=float(similarity_score),
        )

        # Save to database
        await db[self.COLLECTION].update_one(
            {"upload_id": upload_id},
            {"$set": comparison.model_dump()},
            upsert=True,
        )

        return comparison

    async def get_comparison(
        self,
        db: AsyncIOMotorDatabase,
        upload_id: str,
    ) -> ComparisonModel | None:
        """
        Get comparison details from database by upload ID.
        """
        doc = await db[self.COLLECTION].find_one({"upload_id": upload_id})
        if not doc:
            return None
        doc.pop("_id", None)
        return ComparisonModel(**doc)


comparison_service = ComparisonService()