"""
Report Utilities

Reusable helper functions for report generation.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


class ReportUtils:
    """
    Utility class for report generation.
    """

    # =====================================================
    # Report Filename
    # =====================================================

    @staticmethod
    def generate_report_name(
        image_name: str,
    ) -> str:
        """
        Generate report filename.
        """

        image = Path(image_name)

        timestamp = datetime.utcnow().strftime(
            "%Y%m%d_%H%M%S"
        )

        return (
            f"{image.stem}_{timestamp}.pdf"
        )

    # =====================================================
    # Report Path
    # =====================================================

    @staticmethod
    def report_path(
        report_directory: str,
        image_name: str,
    ) -> str:
        """
        Return complete report path.
        """

        directory = Path(report_directory)

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = ReportUtils.generate_report_name(
            image_name
        )

        return str(
            directory / filename
        )

    # =====================================================
    # Processing Time
    # =====================================================

    @staticmethod
    def format_processing_time(
        seconds: float,
    ) -> str:
        """
        Convert processing time into a
        human-readable format.
        """

        if seconds < 1:
            return f"{seconds * 1000:.0f} ms"

        if seconds < 60:
            return f"{seconds:.2f} sec"

        minutes = int(seconds // 60)
        remaining = seconds % 60

        return (
            f"{minutes} min "
            f"{remaining:.2f} sec"
        )

    # =====================================================
    # Current Timestamp
    # =====================================================

    @staticmethod
    def timestamp() -> str:
        """
        Return current UTC timestamp.
        """

        return datetime.utcnow().isoformat()

    # =====================================================
    # Detection Summary
    # =====================================================

    @staticmethod
    def detection_summary(
        detections: list[dict],
    ) -> dict:
        """
        Create a summary of detected objects.
        """

        summary = {}

        for detection in detections:

            label = detection.get(
                "class_name",
                "Unknown",
            )

            summary[label] = (
                summary.get(label, 0) + 1
            )

        return summary


report_utils = ReportUtils()