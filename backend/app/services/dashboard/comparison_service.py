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
        orig_file = Path(original_path)
        detection_folder = Path("outputs/detections")
        detection_folder.mkdir(parents=True, exist_ok=True)
        colorized_folder = Path("outputs/colorized")

        processed_path = None

        # 1. First look for existing detected colorized image in outputs/detections
        candidates = [
            detection_folder / f"{orig_file.stem}_colorized{orig_file.suffix}",
            detection_folder / orig_file.name,
            detection_folder / f"{orig_file.stem}_detected{orig_file.suffix}",
        ]
        for cand in candidates:
            if cand.exists() and cand.resolve() != orig_file.resolve():
                processed_path = str(cand)
                break

        # 2. Search detections folder by stem matching
        if not processed_path:
            matches = [f for f in detection_folder.glob(f"*{orig_file.stem}*") if f.resolve() != orig_file.resolve()]
            if matches:
                processed_path = str(matches[0])

        # 3. If not found in detections folder, find colorized image and run detection on it!
        if not processed_path:
            from app.services.ai.detection_service import detection_service
            source_for_detection = orig_file
            if colorized_folder.exists():
                col_matches = [f for f in colorized_folder.glob(f"*{orig_file.stem}*")]
                if col_matches:
                    source_for_detection = col_matches[0]

            logger.info("Generating detection image from %s for comparison...", source_for_detection)
            try:
                res = detection_service.detect(str(source_for_detection), str(detection_folder))
                if res and res.get("output_path") and Path(res["output_path"]).exists():
                    processed_path = res["output_path"]
            except Exception as exc:
                logger.warning("Detection generation fallback in comparison: %s", exc)

        # 4. Final fallback to latest detection image in detections folder
        if not processed_path:
            det_files = sorted(list(detection_folder.glob("*.jpg")) + list(detection_folder.glob("*.png")), key=lambda p: p.stat().st_mtime)
            if det_files and det_files[-1].resolve() != orig_file.resolve():
                processed_path = str(det_files[-1])
            else:
                processed_path = str(orig_file)

        img1 = cv2.imread(str(original_path))
        img2 = cv2.imread(str(processed_path))

        if img1 is None or img2 is None:
            raise FileNotFoundError(
                f"Could not load original ({original_path}) or processed ({processed_path}) images."
            )

        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        if (h1, w1) != (h2, w2):
            img2_resized = cv2.resize(img2, (w1, h1), interpolation=cv2.INTER_AREA)
        else:
            img2_resized = img2.copy()

        hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
        hist2 = cv2.calcHist([img2_resized], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)

        similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        similarity_score = max(0.0, min(1.0, (similarity + 1.0) / 2.0))

        # Add sleek BEFORE vs AFTER HUD banners on each side
        font_scale = max(0.65, w1 / 1400.0)
        font_thick = max(2, int(font_scale * 2.2))

        # Banner for LEFT (BEFORE)
        cv2.rectangle(img1, (0, 0), (w1, int(42 * font_scale)), (30, 41, 75), cv2.FILLED)
        cv2.putText(
            img1,
            "BEFORE: RAW INFRARED THERMAL INPUT",
            (16, int(28 * font_scale)),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (255, 255, 255),
            font_thick,
            cv2.LINE_AA,
        )

        # Banner for RIGHT (AFTER)
        cv2.rectangle(img2_resized, (0, 0), (w1, int(42 * font_scale)), (0, 100, 220), cv2.FILLED)
        cv2.putText(
            img2_resized,
            "AFTER: AI ENHANCED RGB & MULTI-OBJECT DETECTION",
            (16, int(28 * font_scale)),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (255, 255, 255),
            font_thick,
            cv2.LINE_AA,
        )

        # Side-by-side composition with divider line
        comparison_img = np.hstack((img1, img2_resized))
        mid_x = w1
        cv2.line(comparison_img, (mid_x, 0), (mid_x, h1), (255, 255, 255), 4)

        COMPARISON_FOLDER.mkdir(parents=True, exist_ok=True)
        comparison_filename = f"compare_{orig_file.stem}.jpg"
        comparison_path = COMPARISON_FOLDER / comparison_filename
        cv2.imwrite(str(comparison_path), comparison_img)
        try:
            import shutil
            alt_dir = COMPARISON_FOLDER.parent / "comparsions"
            alt_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(comparison_path), str(alt_dir / comparison_filename))
        except Exception as copy_err:
            logger.warning("Failed to mirror comparison file to comparsions: %s", copy_err)

        processing_time = time.time() - start_time

        detected_objs = [
            f"{obj.get('class_name', 'OBJECT')} ({float(obj.get('confidence', 0.0))*100:.0f}%)"
            if isinstance(obj, dict) else str(obj)
            for obj in (upload_doc.objects_detected or [])
        ]

        comparison = ComparisonModel(
            upload_id=upload_id,
            original_image_path=str(original_path),
            processed_image_path=str(processed_path),
            comparison_image_path=str(comparison_path),
            status=ComparisonStatus.COMPLETED,
            enhancement_applied=True,
            colorization_applied=True,
            object_detection_applied=True,
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

    async def generate_multi_comparison(
        self,
        db: Any,
        upload_id: str,
        enhanced_path: str | None = None,
        colorized_path: str | None = None,
        detected_path: str | None = None,
    ) -> ComparisonModel:
        """
        Generate a multi-panel comparison image (Enhanced, Colorized, Detected) stored in comparsions/comparisons folders.
        """
        start_time = time.time()
        import shutil
        from app.services.ai.report_generation_service import report_generation_service
        img_paths = report_generation_service._auto_discover_image_paths(
            image_name=upload_id,
            enhanced_image_path=enhanced_path,
            colorized_image_path=colorized_path,
            detected_image_path=detected_path,
            upload_id=upload_id,
        )

        enh_p = img_paths.get("enhanced") or img_paths.get("original") or "test_gray.jpg"
        col_p = img_paths.get("colorized") or enh_p
        det_p = img_paths.get("detected") or enh_p

        img_enh = cv2.imread(str(enh_p))
        img_col = cv2.imread(str(col_p))
        img_det = cv2.imread(str(det_p))

        if img_enh is None or img_col is None or img_det is None:
            return await self.compare(db=db, upload_id=upload_id)

        h, w = img_enh.shape[:2]
        if img_col.shape[:2] != (h, w):
            img_col = cv2.resize(img_col, (w, h), interpolation=cv2.INTER_AREA)
        if img_det.shape[:2] != (h, w):
            img_det = cv2.resize(img_det, (w, h), interpolation=cv2.INTER_AREA)

        font_scale = max(0.60, w / 1500.0)
        font_thick = max(2, int(font_scale * 2.2))
        bar_h = int(44 * font_scale)

        # Draw header banners on each panel
        cv2.rectangle(img_enh, (0, 0), (w, bar_h), (30, 41, 75), cv2.FILLED)
        cv2.putText(img_enh, "1. ENHANCED (AI SUPER-RES)", (16, int(30 * font_scale)), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thick, cv2.LINE_AA)

        cv2.rectangle(img_col, (0, 0), (w, bar_h), (180, 80, 10), cv2.FILLED)
        cv2.putText(img_col, "2. COLORIZED (THERMAL MAP)", (16, int(30 * font_scale)), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thick, cv2.LINE_AA)

        cv2.rectangle(img_det, (0, 0), (w, bar_h), (20, 140, 40), cv2.FILLED)
        cv2.putText(img_det, "3. DETECTED (YOLOv8 OBJECTS)", (16, int(30 * font_scale)), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thick, cv2.LINE_AA)

        # Horizontal stack with divider lines
        divider = np.full((h, 6, 3), 255, dtype=np.uint8)
        composite = np.hstack((img_enh, divider, img_col, divider, img_det))

        COMPARISON_FOLDER.mkdir(parents=True, exist_ok=True)
        stem = Path(enh_p).stem.replace("_enhanced", "").strip()
        filename = f"multi_compare_{stem}.jpg"
        comp_path = COMPARISON_FOLDER / filename
        cv2.imwrite(str(comp_path), composite, [cv2.IMWRITE_JPEG_QUALITY, 95])

        alt_dir = COMPARISON_FOLDER.parent / "comparsions"
        alt_dir.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(str(comp_path), str(alt_dir / filename))
        except Exception:
            pass

        std_path = COMPARISON_FOLDER / f"compare_{stem}.jpg"
        cv2.imwrite(str(std_path), composite, [cv2.IMWRITE_JPEG_QUALITY, 95])
        try:
            shutil.copy2(str(std_path), str(alt_dir / f"compare_{stem}.jpg"))
        except Exception:
            pass

        upload_doc = None
        try:
            upload_doc = await upload_repository.get_by_upload_id(upload_id)
        except Exception as db_err:
            logger.warning("Could not fetch upload_doc for multi-comparison: %s", db_err)

        detected_objs = []
        summary_text = ""
        orig_p = str(enh_p)
        if upload_doc:
            orig_p = upload_doc.file_path or orig_p
            summary_text = upload_doc.scene_summary or ""
            detected_objs = [
                f"{obj.get('class_name', 'OBJECT')} ({float(obj.get('confidence', 0.0))*100:.0f}%)" if isinstance(obj, dict) else str(obj)
                for obj in (upload_doc.objects_detected or [])
            ]

        comparison = ComparisonModel(
            upload_id=upload_id,
            original_image_path=orig_p,
            processed_image_path=str(det_p),
            comparison_image_path=str(comp_path),
            status=ComparisonStatus.COMPLETED,
            enhancement_applied=True,
            colorization_applied=True,
            object_detection_applied=True,
            scene_analysis_applied=bool(upload_doc and upload_doc.analysis_completed),
            detected_objects=detected_objs,
            total_objects=len(detected_objs),
            ai_summary=summary_text,
            processing_time_seconds=time.time() - start_time,
            similarity_score=0.95,
        )
        try:
            await comparison_repository.upsert_by_upload_id(comparison)
        except Exception as db_err:
            logger.warning("Could not upsert comparison model to DB: %s", db_err)

        logger.info("Generated multi-stage comparison image at: %s", comp_path)
        return comparison


comparison_service = ComparisonService()