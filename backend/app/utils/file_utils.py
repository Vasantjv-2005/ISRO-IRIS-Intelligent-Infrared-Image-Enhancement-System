"""
File Utilities

Reusable file and directory helper functions
for the IRIS Backend.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Iterable


class FileUtils:
    """
    Utility class for file operations.
    """

    # =====================================================
    # Create Directory
    # =====================================================

    @staticmethod
    def create_directory(
        directory: str | Path,
    ) -> Path:
        """
        Create a directory if it does not exist.
        """

        path = Path(directory)

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        return path

    # =====================================================
    # Delete File
    # =====================================================

    @staticmethod
    def delete_file(
        file_path: str | Path,
    ) -> bool:
        """
        Delete a file.
        """

        path = Path(file_path)

        if not path.exists():
            return False

        if not path.is_file():
            return False

        path.unlink()

        return True

    # =====================================================
    # Delete Directory
    # =====================================================

    @staticmethod
    def delete_directory(
        directory: str | Path,
    ) -> bool:
        """
        Delete an entire directory.
        """

        path = Path(directory)

        if not path.exists():
            return False

        shutil.rmtree(path)

        return True

    # =====================================================
    # Copy File
    # =====================================================

    @staticmethod
    def copy_file(
        source: str | Path,
        destination: str | Path,
    ) -> Path:
        """
        Copy a file.
        """

        source_path = Path(source)
        destination_path = Path(destination)

        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source_path,
            destination_path,
        )

        return destination_path

    # =====================================================
    # Move File
    # =====================================================

    @staticmethod
    def move_file(
        source: str | Path,
        destination: str | Path,
    ) -> Path:
        """
        Move a file.
        """

        source_path = Path(source)
        destination_path = Path(destination)

        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.move(
            str(source_path),
            str(destination_path),
        )

        return destination_path

    # =====================================================
    # Rename File
    # =====================================================

    @staticmethod
    def rename_file(
        source: str | Path,
        new_name: str,
    ) -> Path:
        """
        Rename a file.
        """

        source_path = Path(source)

        destination = source_path.with_name(
            new_name
        )

        source_path.rename(destination)

        return destination

    # =====================================================
    # File Exists
    # =====================================================

    @staticmethod
    def exists(
        path: str | Path,
    ) -> bool:
        """
        Check whether a file or directory exists.
        """

        return Path(path).exists()

    # =====================================================
    # Is File
    # =====================================================

    @staticmethod
    def is_file(
        path: str | Path,
    ) -> bool:
        """
        Check whether path is a file.
        """

        return Path(path).is_file()

    # =====================================================
    # Is Directory
    # =====================================================

    @staticmethod
    def is_directory(
        path: str | Path,
    ) -> bool:
        """
        Check whether path is a directory.
        """

        return Path(path).is_dir()

    # =====================================================
    # File Size
    # =====================================================

    @staticmethod
    def file_size(
        file_path: str | Path,
    ) -> int:
        """
        Return file size in bytes.
        """

        return Path(file_path).stat().st_size

    # =====================================================
    # File Extension
    # =====================================================

    @staticmethod
    def extension(
        file_path: str | Path,
    ) -> str:
        """
        Return file extension.
        """

        return Path(file_path).suffix.lower()

    # =====================================================
    # File Name
    # =====================================================

    @staticmethod
    def filename(
        file_path: str | Path,
    ) -> str:
        """
        Return filename.
        """

        return Path(file_path).name

    # =====================================================
    # File Stem
    # =====================================================

    @staticmethod
    def stem(
        file_path: str | Path,
    ) -> str:
        """
        Return filename without extension.
        """

        return Path(file_path).stem

    # =====================================================
    # List Files
    # =====================================================

    @staticmethod
    def list_files(
        directory: str | Path,
        extensions: Iterable[str] | None = None,
    ) -> list[Path]:
        """
        List files inside a directory.

        Optionally filter by file extensions.
        """

        path = Path(directory)

        if not path.exists():
            return []

        files = [
            file
            for file in path.iterdir()
            if file.is_file()
        ]

        if extensions is None:
            return sorted(files)

        allowed = {
            ext.lower()
            for ext in extensions
        }

        return sorted(
            [
                file
                for file in files
                if file.suffix.lower() in allowed
            ]
        )

    # =====================================================
    # Clear Directory
    # =====================================================

    @staticmethod
    def clear_directory(
        directory: str | Path,
    ) -> None:
        """
        Remove all files inside a directory.
        """

        path = Path(directory)

        if not path.exists():
            return

        for item in path.iterdir():

            if item.is_file():
                item.unlink()

            elif item.is_dir():
                shutil.rmtree(item)


# ==========================================================
# Singleton
# ==========================================================

file_utils = FileUtils()