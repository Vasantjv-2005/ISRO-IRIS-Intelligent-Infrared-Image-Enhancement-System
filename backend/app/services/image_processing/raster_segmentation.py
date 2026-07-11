"""
Satellite Raster Segmentation Integration Module

Accepts a multi-band satellite raster file stream, reads its shape and pixel arrays,
isolates the infrared spectrum data, and runs high-speed thresholding algorithms
to segment water bodies (low infrared reflectance) from forest canopy (high infrared reflectance).
Designed to be modular, runtime-optimized, and free of heavy external dependencies.
"""

from __future__ import annotations

import io
import time
from pathlib import Path
from typing import Any, BinaryIO, Union

import cv2
import numpy as np
from PIL import Image

from app.middleware.error_handler import ImageProcessingException
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class RasterSegmentationService:
    """
    Modular integration service for multi-band satellite raster segmentation.
    """

    def parse_raster_stream(
        self,
        file_stream: Union[bytes, io.BytesIO, BinaryIO, str, Path, np.ndarray],
    ) -> np.ndarray:
        """
        Reads a multi-band satellite raster stream or array and returns a standardized
        NumPy array of shape (height, width, bands).

        Args:
            file_stream: Stream of bytes, file-like object, file path, or numpy array.

        Returns:
            np.ndarray: Multi-band raster array of shape (H, W, C) or single band (H, W, 1).
        """
        try:
            if isinstance(file_stream, np.ndarray):
                array = file_stream
            elif isinstance(file_stream, (str, Path)):
                path = Path(file_stream)
                if not path.exists():
                    raise FileNotFoundError(f"Raster file not found: {path}")
                if path.suffix.lower() in (".npy", ".npz"):
                    loaded = np.load(str(path))
                    if isinstance(loaded, np.lib.npyio.NpzFile):
                        first_key = loaded.files[0]
                        array = loaded[first_key]
                    else:
                        array = loaded
                else:
                    # Parse image raster (TIFF, PNG, JPG, etc.)
                    img = Image.open(str(path))
                    array = np.array(img)
            elif isinstance(file_stream, bytes):
                # Check if it is a numpy binary archive stream (.npy / .npz)
                buffer = io.BytesIO(file_stream)
                try:
                    loaded = np.load(buffer)
                    if isinstance(loaded, np.lib.npyio.NpzFile):
                        first_key = loaded.files[0]
                        array = loaded[first_key]
                    else:
                        array = loaded
                except Exception:
                    buffer.seek(0)
                    img = Image.open(buffer)
                    array = np.array(img)
            elif hasattr(file_stream, "read"):
                content = file_stream.read()
                return self.parse_raster_stream(content)
            else:
                raise ValueError(f"Unsupported file_stream type: {type(file_stream)}")

            # Standardize shape to (H, W, C)
            if array.ndim == 2:
                array = array[:, :, np.newaxis]
            elif array.ndim == 3 and array.shape[0] in (1, 3, 4, 8, 12) and array.shape[2] > 32:
                # Channel-first format (C, H, W) -> convert to (H, W, C)
                array = np.transpose(array, (1, 2, 0))

            return array
        except Exception as exc:
            logger.error("Failed to parse satellite raster stream: %s", exc, exc_info=True)
            raise ImageProcessingException(f"Failed to parse satellite raster stream: {exc}") from exc

    def isolate_infrared_band(
        self,
        raster_array: np.ndarray,
        ir_band_idx: int = -1,
    ) -> np.ndarray:
        """
        Isolates the infrared spectrum data from a multi-band satellite raster.

        Args:
            raster_array: Standardized raster array of shape (H, W, C).
            ir_band_idx: Index of the infrared band. Default -1 selects the highest
                         wavelength/infrared channel (e.g., NIR channel or designated IR band).

        Returns:
            np.ndarray: 2D array of isolated infrared spectrum data (H, W) as float32.
        """
        try:
            if raster_array.ndim != 3:
                raise ValueError(f"Expected 3D raster array (H, W, C), got shape {raster_array.shape}")

            num_bands = raster_array.shape[2]
            if ir_band_idx < -num_bands or ir_band_idx >= num_bands:
                raise ValueError(
                    f"Band index {ir_band_idx} out of range for raster with {num_bands} bands."
                )

            # Extract the target band
            ir_band = raster_array[:, :, ir_band_idx].astype(np.float32)

            return ir_band
        except Exception as exc:
            logger.error("Failed to isolate infrared spectrum data: %s", exc, exc_info=True)
            raise ImageProcessingException(f"Failed to isolate infrared spectrum: {exc}") from exc

    def enhance_infrared_band(
        self,
        ir_band: np.ndarray,
    ) -> np.ndarray:
        """
        Applies edge-preserving bilateral filtering and high-frequency detail boosting
        to the isolated infrared band while preserving global class separation.

        Args:
            ir_band: 2D infrared band array.

        Returns:
            np.ndarray: Enhanced 2D infrared band in original radiometric scale.
        """
        try:
            min_val = float(np.min(ir_band))
            max_val = float(np.max(ir_band))
            if max_val - min_val < 1e-5:
                return ir_band

            # Denoise while preserving sharp boundaries between water and forest canopy
            filtered = cv2.bilateralFilter(ir_band.astype(np.float32), d=5, sigmaColor=(max_val - min_val) * 0.15, sigmaSpace=10)

            # High-frequency unsharp detail boost
            blurred = cv2.GaussianBlur(filtered, (0, 0), 1.0)
            enhanced = cv2.addWeighted(filtered, 1.25, blurred, -0.25, 0)

            return np.clip(enhanced, min_val, max_val).astype(np.float32)
        except Exception as exc:
            logger.warning("Infrared band enhancement failed (%s), returning original band.", exc)
            return ir_band

    def compute_segmentation_threshold(
        self,
        ir_band: np.ndarray,
        method: str = "otsu",
        custom_threshold: float | None = None,
    ) -> float:
        """
        Computes the threshold to separate low reflectance (water bodies)
        from high reflectance (forest canopy / dense vegetation).

        Args:
            ir_band: 2D infrared band array.
            method: Method to compute threshold ('otsu', 'adaptive', 'percentile', 'isodata').
            custom_threshold: Explicit threshold if method=='custom'.

        Returns:
            float: Threshold value in the scale of ir_band.
        """
        try:
            if custom_threshold is not None:
                return float(custom_threshold)

            min_v = float(np.min(ir_band))
            max_v = float(np.max(ir_band))
            if max_v - min_v < 1e-5:
                return min_v

            norm_band = np.clip(
                ((ir_band - min_v) / (max_v - min_v)) * 255.0, 0, 255
            ).astype(np.uint8)

            if method.lower() == "otsu":
                thresh_norm, _ = cv2.threshold(
                    norm_band, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )
                if thresh_norm <= 0.0 or thresh_norm >= 255.0:
                    thresh_norm = 127.5
                return float(min_v + (thresh_norm / 255.0) * (max_v - min_v))
            elif method.lower() == "percentile":
                return float(np.percentile(ir_band, 35.0))
            elif method.lower() == "isodata":
                t = float(np.mean(ir_band))
                for _ in range(25):
                    low = ir_band[ir_band < t]
                    high = ir_band[ir_band >= t]
                    mean_low = float(np.mean(low)) if low.size > 0 else min_v
                    mean_high = float(np.mean(high)) if high.size > 0 else max_v
                    new_t = (mean_low + mean_high) / 2.0
                    if abs(new_t - t) < 0.01:
                        break
                    t = new_t
                return float(t)
            else:
                thresh_norm, _ = cv2.threshold(
                    norm_band, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )
                if thresh_norm <= 0.0 or thresh_norm >= 255.0:
                    thresh_norm = 127.5
                return float(min_v + (thresh_norm / 255.0) * (max_v - min_v))
        except Exception as exc:
            logger.error("Failed to compute segmentation threshold: %s", exc, exc_info=True)
            raise ImageProcessingException(f"Failed to compute threshold: {exc}") from exc

    def segment_water_and_canopy(
        self,
        ir_band: np.ndarray,
        threshold: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Segments water bodies (low infrared reflectance) and forest canopy (high infrared reflectance).

        Args:
            ir_band: 2D infrared band array.
            threshold: Computed threshold value.

        Returns:
            tuple[np.ndarray, np.ndarray]:
                water_mask: Binary mask (uint8 0/255) where 255 indicates water bodies.
                forest_mask: Binary mask (uint8 0/255) where 255 indicates forest canopy.
        """
        try:
            # Fast vectorized comparison
            water_mask = np.where(ir_band < threshold, 255, 0).astype(np.uint8)
            forest_mask = np.where(ir_band >= threshold, 255, 0).astype(np.uint8)

            # Vectorized morphological clean-up to remove isolated speckle noise
            kernel = np.ones((3, 3), dtype=np.uint8)
            water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_OPEN, kernel)
            forest_mask = cv2.morphologyEx(forest_mask, cv2.MORPH_OPEN, kernel)

            return water_mask, forest_mask
        except Exception as exc:
            logger.error("Segmentation execution failed: %s", exc, exc_info=True)
            raise ImageProcessingException(f"Segmentation failed: {exc}") from exc

    def create_colorized_segmentation_map(
        self,
        ir_band: np.ndarray,
        water_mask: np.ndarray,
        forest_mask: np.ndarray,
    ) -> np.ndarray:
        """
        Generates a premium high-definition RGB visualization overlay
        differentiating water bodies (azure blue) from forest canopy (lush emerald green).

        Args:
            ir_band: 2D infrared band array.
            water_mask: Binary mask of water bodies.
            forest_mask: Binary mask of forest canopy.

        Returns:
            np.ndarray: BGR colorized segmentation map of shape (H, W, 3).
        """
        h, w = ir_band.shape[:2]
        # Base grayscale representation
        min_v = float(np.min(ir_band))
        max_v = float(np.max(ir_band))
        if max_v - min_v > 1e-5:
            gray = np.clip(((ir_band - min_v) / (max_v - min_v)) * 255.0, 0, 255).astype(np.uint8)
        else:
            gray = np.zeros((h, w), dtype=np.uint8)

        color_map = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        # Rich aesthetic colors (BGR format)
        # Water: Azure Blue (255, 140, 20)
        # Forest Canopy: Emerald Green (50, 205, 50)
        water_overlay = np.zeros_like(color_map)
        water_overlay[:, :] = (255, 140, 20)

        forest_overlay = np.zeros_like(color_map)
        forest_overlay[:, :] = (50, 205, 50)

        # Apply overlay with smooth blending
        water_bool = water_mask > 0
        forest_bool = forest_mask > 0

        color_map[water_bool] = cv2.addWeighted(
            color_map, 0.45, water_overlay, 0.55, 0
        )[water_bool]
        color_map[forest_bool] = cv2.addWeighted(
            color_map, 0.50, forest_overlay, 0.50, 0
        )[forest_bool]

        return color_map

    def process_raster(
        self,
        file_stream: Union[bytes, io.BytesIO, BinaryIO, str, Path, np.ndarray],
        ir_band_idx: int = -1,
        method: str = "otsu",
        custom_threshold: float | None = None,
        enhance_ir: bool = True,
        output_path: str | Path | None = None,
    ) -> dict[str, Any]:
        """
        Orchestrates the complete multi-band satellite raster segmentation workflow:
        1. Parse stream to shape (H, W, C)
        2. Isolate infrared spectrum data
        3. Pre-process & enhance infrared band for high quality feature separation
        4. Compute optimal segmentation threshold
        5. Segment water bodies (low reflectance) vs forest canopy (high reflectance)
        6. Compute runtime speed & coverage statistics

        Args:
            file_stream: Input multi-band satellite raster stream or array.
            ir_band_idx: Index of infrared band.
            method: Thresholding method ('otsu', 'percentile', 'isodata').
            custom_threshold: Optional explicit threshold value.
            enhance_ir: Whether to apply CLAHE detail enhancement before segmentation.
            output_path: Optional file path to save the colorized segmentation visualization.

        Returns:
            dict[str, Any]: Complete segmentation results and statistics.
        """
        start_time = time.perf_counter()

        raster_array = self.parse_raster_stream(file_stream)
        shape = raster_array.shape

        ir_band = self.isolate_infrared_band(raster_array, ir_band_idx=ir_band_idx)

        processed_ir = self.enhance_infrared_band(ir_band) if enhance_ir else ir_band

        threshold = self.compute_segmentation_threshold(
            processed_ir, method=method, custom_threshold=custom_threshold
        )

        water_mask, forest_mask = self.segment_water_and_canopy(processed_ir, threshold)

        total_pixels = float(water_mask.size)
        water_pixels = float(np.count_nonzero(water_mask))
        forest_pixels = float(np.count_nonzero(forest_mask))

        water_pct = round((water_pixels / total_pixels) * 100.0, 2) if total_pixels > 0 else 0.0
        forest_pct = round((forest_pixels / total_pixels) * 100.0, 2) if total_pixels > 0 else 0.0

        colorized_map = self.create_colorized_segmentation_map(processed_ir, water_mask, forest_mask)

        saved_path = None
        if output_path:
            out_file = Path(output_path)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(out_file), colorized_map, [cv2.IMWRITE_JPEG_QUALITY, 96])
            saved_path = str(out_file)

        runtime_ms = round((time.perf_counter() - start_time) * 1000.0, 3)

        logger.info(
            "Satellite raster segmentation completed in %.3f ms. Shape=%s, Threshold=%.2f, Water=%.2f%%, Forest=%.2f%%",
            runtime_ms,
            shape,
            threshold,
            water_pct,
            forest_pct,
        )

        return {
            "success": True,
            "shape": shape,
            "infrared_band": ir_band,
            "processed_infrared_band": processed_ir,
            "water_mask": water_mask,
            "forest_mask": forest_mask,
            "colorized_segmentation": colorized_map,
            "threshold": threshold,
            "threshold_method": method,
            "water_coverage_pct": water_pct,
            "forest_coverage_pct": forest_pct,
            "water_pixels": int(water_pixels),
            "forest_pixels": int(forest_pixels),
            "runtime_ms": runtime_ms,
            "output_path": saved_path,
        }


raster_segmentation_service = RasterSegmentationService()
