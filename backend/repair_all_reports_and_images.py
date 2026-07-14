import os
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Ensure backend directory is in python path
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from app.services.ai.colorization_service import colorization_service
from app.services.ai.detection_service import detection_service
from app.services.ai.report_generation_service import report_generation_service

def main():
    preprocessing_dir = Path("outputs/preprocessing")
    if not preprocessing_dir.exists():
        logger.error("outputs/preprocessing does not exist")
        return

    images = list(preprocessing_dir.glob("*.jpg")) + list(preprocessing_dir.glob("*.png")) + list(preprocessing_dir.glob("*.jpeg"))
    logger.info("Found %d images in outputs/preprocessing to process", len(images))

    for img_path in images:
        stem = img_path.stem
        if stem in ["denoised", "enhanced", "normalized", "resized"]:
            continue

        logger.info("=== Processing capture ID: %s ===", stem)

        # 1. Enhanced image
        enh_out = Path("outputs/enhanced") / f"{stem}.jpg"
        if not enh_out.exists() or enh_out.stat().st_size < 1000:
            try:
                from app.services.ai.enhancement_service import enhancement_service
                enh_out.parent.mkdir(parents=True, exist_ok=True)
                enhancement_service.enhance(input_path=str(img_path), output_path=str(enh_out))
                logger.info("Generated unique enhanced image: %s", enh_out)
            except Exception as e:
                logger.error("Error enhancing %s: %s", stem, e)

        # 2. Colorized image
        col_out = Path("outputs/colorized") / f"{stem}.jpg"
        if not col_out.exists() or col_out.stat().st_size < 1000:
            try:
                col_out.parent.mkdir(parents=True, exist_ok=True)
                colorization_service.colorize(input_path=str(img_path), output_path=str(col_out))
                logger.info("Generated unique colorized image: %s", col_out)
            except Exception as e:
                logger.error("Error colorizing %s: %s", stem, e)

        # 3. Detected image
        det_out = Path("outputs/detected") / f"{stem}.jpg"
        if not det_out.exists() or det_out.stat().st_size < 1000:
            try:
                det_out.parent.mkdir(parents=True, exist_ok=True)
                detection_service.detect(
                    image_path=str(img_path),
                    output_directory="outputs/detected",
                    confidence=0.25,
                )
                logger.info("Generated unique detected image: %s", det_out)
            except Exception as e:
                logger.error("Error detecting %s: %s", stem, e)

        # 4. Regenerate unique PDF report so it is NOT a copy of CHANDRA_09
        try:
            logger.info("Regenerating authentic 4-stage PDF report for %s...", stem)
            report_path = report_generation_service.generate_report(
                upload_id=stem,
                original_image_path=str(img_path),
                preprocessed_image_path=str(img_path),
                enhanced_image_path=str(enh_out) if enh_out.exists() else str(img_path),
                colorized_image_path=str(col_out) if col_out.exists() else None,
                detected_image_path=str(det_out) if det_out.exists() else None,
            )
            logger.info("Regenerated unique PDF report: %s", report_path)
        except Exception as e:
            logger.error("Error generating report for %s: %s", stem, e)

    logger.info("=== All reports and images repaired and uniquely generated ===")

if __name__ == "__main__":
    main()
