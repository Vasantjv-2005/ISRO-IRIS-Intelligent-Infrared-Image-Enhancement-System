"""
Unit tests for AI model wrappers and weight validation.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

from app.ai_models.colorization_model import ColorizationModel
from app.ai_models.enhancement_model import EnhancementModel
from app.ai_models.utils import validate_weights
from app.ai_models.yolov8_model import YOLOv8Model
from app.middleware.error_handler import (
    WeightsInvalidError,
    WeightsNotFoundError,
)


class TestWeightValidation(unittest.TestCase):
    """
    Tests for weights validation logic.
    """

    def test_missing_weights_file(self) -> None:
        """
        Validate that missing files raise WeightsNotFoundError.
        """
        non_existent = Path("non_existent_weights_file.pth")
        with self.assertRaises(WeightsNotFoundError):
            validate_weights(non_existent)

    def test_empty_weights_file(self) -> None:
        """
        Validate that empty (0-byte) files raise WeightsInvalidError.
        """
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            # File is empty (0 bytes)
            with self.assertRaises(WeightsInvalidError) as ctx:
                validate_weights(tmp_path)
            self.assertIn("empty (0-byte placeholder)", str(ctx.exception))
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    def test_directory_as_weights(self) -> None:
        """
        Validate that directories raise WeightsInvalidError.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            dir_path = Path(tmp_dir)
            with self.assertRaises(WeightsInvalidError) as ctx:
                validate_weights(dir_path)
            self.assertIn("not a file", str(ctx.exception))


class TestColorizationWrapper(unittest.TestCase):
    """
    Tests for ColorizationModel wrapper.
    """

    def test_opencv_backend(self) -> None:
        """
        OpenCV backend should run without checking weights.
        """
        # Initialize model with invalid path but explicitly set to opencv backend
        model = ColorizationModel(
            model_path="invalid_path.pth",
            backend="opencv",
        )
        model.load()
        self.assertTrue(model.model_loaded)
        self.assertIsNone(model.model)

        # Test inference with dummy image
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_in:
            in_path = tmp_in.name
            dummy_img = np.zeros((100, 100), dtype=np.uint8)
            cv2.imwrite(in_path, dummy_img)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_out:
            out_path = tmp_out.name

        try:
            res_path = model.colorize(in_path, out_path)
            self.assertEqual(res_path, out_path)
            # Verify colorized image exists and has 3 channels
            colorized = cv2.imread(res_path)
            self.assertIsNotNone(colorized)
            self.assertEqual(colorized.shape[2], 3)
        finally:
            Path(in_path).unlink(missing_ok=True)
            Path(out_path).unlink(missing_ok=True)

    def test_deep_learning_backend_invalid_weights(self) -> None:
        """
        In deep_learning mode, invalid/empty weights must raise WeightsInvalidError.
        """
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            model = ColorizationModel(
                model_path=tmp_path,
                backend="deep_learning",
            )
            with self.assertRaises(WeightsInvalidError):
                model.load()
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_auto_backend_fallback(self) -> None:
        """
        In auto mode, invalid weights should fall back to OpenCV gracefully.
        """
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            model = ColorizationModel(
                model_path=tmp_path,
                backend="auto",
            )
            # load should NOT raise, it should fall back to OpenCV
            model.load()
            self.assertTrue(model.model_loaded)
            self.assertIsNone(model.model)
            self.assertEqual(model.info()["backend"], "opencv")
        finally:
            Path(tmp_path).unlink(missing_ok=True)


class TestEnhancementWrapper(unittest.TestCase):
    """
    Tests for EnhancementModel wrapper.
    """

    def test_opencv_backend(self) -> None:
        """
        OpenCV backend should run without checking weights.
        """
        model = EnhancementModel(
            model_path="invalid_path.pth",
            backend="opencv",
        )
        model.load()
        self.assertTrue(model.model_loaded)
        self.assertIsNone(model.model)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_in:
            in_path = tmp_in.name
            dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
            cv2.imwrite(in_path, dummy_img)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_out:
            out_path = tmp_out.name

        try:
            res_path = model.enhance(in_path, out_path)
            self.assertEqual(res_path, out_path)
            enhanced = cv2.imread(res_path)
            self.assertIsNotNone(enhanced)
        finally:
            Path(in_path).unlink(missing_ok=True)
            Path(out_path).unlink(missing_ok=True)

    def test_deep_learning_backend_invalid_weights(self) -> None:
        """
        In deep_learning mode, invalid/empty weights must raise WeightsInvalidError.
        """
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            model = EnhancementModel(
                model_path=tmp_path,
                backend="deep_learning",
            )
            with self.assertRaises(WeightsInvalidError):
                model.load()
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_auto_backend_fallback(self) -> None:
        """
        In auto mode, invalid weights should fall back to OpenCV gracefully.
        """
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            model = EnhancementModel(
                model_path=tmp_path,
                backend="auto",
            )
            model.load()
            self.assertTrue(model.model_loaded)
            self.assertIsNone(model.model)
            self.assertEqual(model.info()["backend"], "opencv")
        finally:
            Path(tmp_path).unlink(missing_ok=True)


class TestYOLOv8Wrapper(unittest.TestCase):
    """
    Tests for YOLOv8Model wrapper.
    """

    def test_empty_weights_raises_invalid(self) -> None:
        """
        YOLOv8 loading on empty weights must raise WeightsInvalidError.
        """
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            model = YOLOv8Model(model_path=tmp_path)
            with self.assertRaises(WeightsInvalidError):
                model.load()
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_missing_weights_raises_not_found(self) -> None:
        """
        YOLOv8 loading on missing weights must raise WeightsNotFoundError.
        """
        model = YOLOv8Model(model_path="completely_missing_weights.pt")
        with self.assertRaises(WeightsNotFoundError):
            model.load()
