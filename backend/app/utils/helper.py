"""
Helper Utilities

Common reusable helper functions for the
IRIS Backend.
"""

from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class Helper:
    """
    General helper utilities.
    """

    # =====================================================
    # UUID
    # =====================================================

    @staticmethod
    def generate_uuid() -> str:
        """
        Generate a UUID4 string.
        """

        return str(uuid.uuid4())

    # =====================================================
    # UTC Timestamp
    # =====================================================

    @staticmethod
    def utc_now() -> datetime:
        """
        Return current UTC datetime.
        """

        return datetime.now(timezone.utc)

    # =====================================================
    # ISO Timestamp
    # =====================================================

    @staticmethod
    def iso_timestamp() -> str:
        """
        Return ISO formatted UTC timestamp.
        """

        return Helper.utc_now().isoformat()

    # =====================================================
    # File Size Formatter
    # =====================================================

    @staticmethod
    def format_file_size(
        size_bytes: int,
    ) -> str:
        """
        Convert bytes into a human readable format.
        """

        units = [
            "B",
            "KB",
            "MB",
            "GB",
            "TB",
        ]

        size = float(size_bytes)

        for unit in units:

            if size < 1024 or unit == units[-1]:
                return f"{size:.2f} {unit}"

            size /= 1024

        return "0 B"

    # =====================================================
    # Percentage
    # =====================================================

    @staticmethod
    def percentage(
        value: float,
        total: float,
    ) -> float:
        """
        Calculate percentage safely.
        """

        if total <= 0:
            return 0.0

        return round(
            (value / total) * 100,
            2,
        )

    # =====================================================
    # Execution Timer
    # =====================================================

    @staticmethod
    def timer() -> float:
        """
        Return high precision timer.
        """

        return time.perf_counter()

    @staticmethod
    def elapsed(
        start_time: float,
    ) -> float:
        """
        Return elapsed time in seconds.
        """

        return round(
            time.perf_counter() - start_time,
            4,
        )

    # =====================================================
    # JSON Serializer
    # =====================================================

    @staticmethod
    def to_json(
        data: Any,
        indent: int = 4,
    ) -> str:
        """
        Serialize object to JSON.
        """

        return json.dumps(
            data,
            indent=indent,
            default=str,
            ensure_ascii=False,
        )

    # =====================================================
    # JSON Loader
    # =====================================================

    @staticmethod
    def from_json(
        text: str,
    ) -> Any:
        """
        Deserialize JSON string.
        """

        return json.loads(text)

    # =====================================================
    # Safe Dictionary Get
    # =====================================================

    @staticmethod
    def safe_get(
        dictionary: dict,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Safe dictionary lookup.
        """

        return dictionary.get(
            key,
            default,
        )

    # =====================================================
    # File Name
    # =====================================================

    @staticmethod
    def filename(
        path: str,
    ) -> str:
        """
        Return filename from path.
        """

        return Path(path).name

    # =====================================================
    # File Stem
    # =====================================================

    @staticmethod
    def stem(
        path: str,
    ) -> str:
        """
        Return filename without extension.
        """

        return Path(path).stem

    # =====================================================
    # Flatten List
    # =====================================================

    @staticmethod
    def flatten(
        nested: list[list[Any]],
    ) -> list[Any]:
        """
        Flatten nested list.
        """

        return [
            item
            for sublist in nested
            for item in sublist
        ]

    # =====================================================
    # Chunk List
    # =====================================================

    @staticmethod
    def chunk(
        items: list[Any],
        size: int,
    ) -> list[list[Any]]:
        """
        Split a list into chunks.
        """

        if size <= 0:
            raise ValueError(
                "Chunk size must be greater than zero."
            )

        return [
            items[index:index + size]
            for index in range(
                0,
                len(items),
                size,
            )
        ]


helper = Helper()