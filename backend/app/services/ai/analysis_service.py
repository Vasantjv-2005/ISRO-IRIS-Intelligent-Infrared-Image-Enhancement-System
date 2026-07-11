"""
AI Analysis Service

Uses Google Gemini to analyze infrared images and detected objects,
integrating with the repository layer for persistence.
"""

from __future__ import annotations

from typing import Any

import google.generativeai as genai

from app.core.settings import settings
from app.middleware.error_handler import AIModelException
from app.models.analysis_model import (
    AnalysisModel,
    AnalysisStatus,
    DetectedObject,
    utc_now,
)
from app.repositories.analysis_repository import analysis_repository
from app.repositories.upload_repository import upload_repository
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class AnalysisService:
    """
    Service responsible for scene analysis using Gemini.
    """

    def __init__(self) -> None:
        """
        Initialize the AnalysisService and configure Gemini.
        """
        self.model: Any = None
        self._initialize()

    def _initialize(self) -> None:
        """
        Initialize the Gemini model SDK.
        """
        try:
            if settings.GEMINI_API_KEY:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel("gemini-2.5-flash")
                logger.info("Gemini GenerativeModel successfully initialized.")
            else:
                logger.warning("GEMINI_API_KEY is not set. Relying on Groq fallback.")
        except Exception as exc:
            logger.warning("Failed to initialize Gemini SDK (%s). Relying on Groq fallback.", exc)

    def analyze(
        self,
        detected_objects: list[dict[str, Any]],
        image_name: str,
        output_directory: str = "outputs/analyzed",
        input_image_path: str | None = None,
    ) -> dict[str, Any]:
        """
        Analyze detected objects using Gemini with automatic fallback to Groq AI.

        Args:
            detected_objects: Objects detected by YOLO.
            image_name: Image filename.
            output_directory: Directory to save analysis outputs.
            input_image_path: Path to input image being analyzed.

        Returns:
            Dictionary containing AI analysis results and output paths.
        """
        try:
            logger.info("Starting AI scene analysis for image: %s", image_name)

            if not detected_objects:
                prompt = f"""You are an expert scientific infrared image analyst evaluating image '{image_name}'.

CRITICAL CONSTRAINT: No objects were detected by the YOLO detection engine in this infrared image. Do NOT invent or hallucinate any objects.

Please provide your analysis structured under the following exact headings:
### Scene Summary
Provide a concise overview stating that no discrete thermal structures were detected above threshold.

### Important Findings
Discuss background thermal characteristics or ambient emissivity patterns.

### Possible Hazards
State whether any thermal anomalies or safety hazards are apparent.

### Confidence Assessment
Explain the confidence level of the negative detection result.

### Recommendations
Suggest adjustments to detection thresholds or imaging parameters if needed.
"""
            else:
                def _fmt_item(idx: int, item: dict[str, Any]) -> str:
                    bbox = item.get("bbox", {})
                    if isinstance(bbox, dict):
                        x1, y1, x2, y2 = float(bbox.get("x1", 0)), float(bbox.get("y1", 0)), float(bbox.get("x2", 0)), float(bbox.get("y2", 0))
                    elif isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                        x1, y1, x2, y2 = float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
                    else:
                        x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
                    return f"- [{idx+1}] Object: {str(item.get('class_name', 'UNKNOWN')).upper()} | Confidence: {float(item.get('confidence', 0.0))*100:.1f}% | Bounding Box (x1, y1, x2, y2): ({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})"

                formatted_objects = "\n".join(
                    _fmt_item(idx, item)
                    for idx, item in enumerate(detected_objects)
                )

                prompt = f"""You are an expert scientific infrared image interpretation specialist evaluating image '{image_name}'.

Total Objects Detected by YOLO Engine: {len(detected_objects)}

Detected Objects Inventory (Class | Confidence | Bounding Box):
{formatted_objects}

CRITICAL CONSTRAINT: You must NEVER invent, hallucinate, or assume any objects that are not listed in the Detected Objects Inventory above. You must ONLY analyze the exact objects returned by the YOLO detection engine above.

Provide a comprehensive, professional scientific interpretation structured under the following exact headings:
### Scene Summary
Provide an executive summary of the infrared scene based strictly on the detected thermal features and object layout.

### Important Findings
Detail each detected object, correlating its bounding box location and confidence score with its thermal characteristics.

### Possible Hazards
Assess any potential environmental, structural, thermal, or operational risks associated with these detected features.

### Confidence Assessment
Evaluate the reliability of the interpretation given the YOLO confidence scores.

### Recommendations
Provide actionable recommendations or follow-up procedures based on the scene interpretation.
"""

            analysis_text = ""
            if self.model and settings.GEMINI_API_KEY:
                try:
                    response = self.model.generate_content(prompt)
                    analysis_text = getattr(response, "text", str(response)).strip()
                    logger.info("Successfully completed Gemini scene analysis for: %s", image_name)
                except Exception as gemini_err:
                    logger.warning("Gemini analysis failed (%s). Attempting fallback to Groq AI...", gemini_err)

            if not analysis_text and settings.GROQ_API_KEY:
                try:
                    from groq import Groq
                    groq_client = Groq(api_key=settings.GROQ_API_KEY)
                    completion = groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=settings.GROQ_MODEL or "llama-3.3-70b-versatile",
                    )
                    if completion.choices and completion.choices[0].message.content:
                        analysis_text = completion.choices[0].message.content.strip()
                        logger.info("Successfully completed Groq AI scene analysis for: %s", image_name)
                except Exception as groq_err:
                    logger.error("Groq AI analysis failed for %s: %s", image_name, groq_err, exc_info=True)
                    raise AIModelException(f"Both Gemini and Groq analysis failed. Groq error: {groq_err}") from groq_err

            if not analysis_text:
                raise AIModelException("AI analysis failed: Neither Gemini nor Groq produced valid output or API keys are missing.")

            from pathlib import Path
            import json, shutil
            out_dir = Path(output_directory)
            out_dir.mkdir(parents=True, exist_ok=True)
            stem = Path(image_name).stem
            json_path = out_dir / f"{stem}.json"

            output_img_path = out_dir / image_name
            if input_image_path and Path(input_image_path).exists():
                if Path(input_image_path) != output_img_path:
                    shutil.copy(str(input_image_path), str(output_img_path))
            elif not output_img_path.exists():
                output_img_path = json_path

            result_dict = {
                "success": True,
                "image": image_name,
                "analysis": analysis_text,
                "output_path": str(output_img_path),
                "json_path": str(json_path),
            }
            try:
                json_path.write_text(json.dumps(result_dict, indent=2), encoding="utf-8")
            except Exception as e:
                logger.warning("Failed to save analysis json: %s", e)

            return result_dict

        except Exception as exc:
            logger.error("AI scene analysis failed for %s: %s", image_name, exc, exc_info=True)
            if isinstance(exc, AIModelException):
                raise
            raise AIModelException(f"AI analysis failed: {exc}") from exc

    async def analyze_async(
        self,
        detected_objects: list[dict[str, Any]],
        image_name: str,
        upload_id: str | None = None,
        output_directory: str = "outputs/analyzed",
        input_image_path: str | None = None,
    ) -> dict[str, Any]:
        """
        Execute analysis and persist the results in the database repositories.

        Args:
            detected_objects: Objects detected by YOLO.
            image_name: Image filename.
            upload_id: Optional upload identifier for repository persistence.
            output_directory: Directory to save analysis outputs.
            input_image_path: Path to input image being analyzed.

        Returns:
            Dictionary containing AI analysis results and output paths.
        """
        result = self.analyze(
            detected_objects=detected_objects,
            image_name=image_name,
            output_directory=output_directory,
            input_image_path=input_image_path,
        )

        target_upload_id = upload_id or image_name
        try:
            def _extract_bbox(b: Any) -> list[float]:
                if isinstance(b, dict):
                    return [
                        float(b.get("x1", 0.0)),
                        float(b.get("y1", 0.0)),
                        float(b.get("x2", 0.0)),
                        float(b.get("y2", 0.0)),
                    ]
                if isinstance(b, (list, tuple)) and len(b) >= 4:
                    return [float(x) for x in b[:4]]
                return [0.0, 0.0, 0.0, 0.0]

            converted_objects = [
                DetectedObject(
                    label=str(obj.get("class_name", "unknown")),
                    confidence=float(obj.get("confidence", 0.0)),
                    bounding_box=_extract_bbox(obj.get("bbox", {})),
                )
                for obj in detected_objects
            ]

            analysis_doc = AnalysisModel(
                upload_id=target_upload_id,
                image_name=image_name,
                status=AnalysisStatus.COMPLETED,
                scene_summary=result["analysis"][:200] + "..." if len(result["analysis"]) > 200 else result["analysis"],
                detailed_analysis=result["analysis"],
                detected_objects=converted_objects,
                object_count=len(converted_objects),
                confidence_score=0.85 if converted_objects else 0.50,
                analyzed_at=utc_now(),
            )

            await analysis_repository.create(analysis_doc)
            if upload_id:
                await upload_repository.save_analysis(
                    upload_id=upload_id,
                    objects_detected=detected_objects,
                    scene_summary=analysis_doc.scene_summary or "",
                    analyzed_path=result.get("output_path"),
                )
            logger.info("Persisted analysis results to database for upload: %s", target_upload_id)
        except Exception as exc:
            logger.error("Failed to persist analysis to DB for upload %s: %s", target_upload_id, exc, exc_info=True)

        return result


analysis_service = AnalysisService()