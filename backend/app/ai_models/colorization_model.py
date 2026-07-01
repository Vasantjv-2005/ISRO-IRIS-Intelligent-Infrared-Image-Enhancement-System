"""
Colorization Model

Image colorization wrapper supporting both OpenCV (Pseudo Color)
and Deep Learning backends.
"""

from __future__ import annotations

import logging
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.nn as nn

from app.core.config import COLORIZATION_BACKEND, COLORIZATION_MODEL_PATH
from app.ai_models.utils import validate_weights
from app.middleware.error_handler import WeightsInvalidError

logger = logging.getLogger("iris")


class ColorizationNet(nn.Module):
    """
    Placeholder PyTorch model architecture for future deep-learning colorization.
    Replace this with DeOldify, Palette, or custom model architecture.
    """

    def __init__(self) -> None:
        super().__init__()
        # Standard input 1-channel grayscale to 3-channel BGR
        self.conv = nn.Conv2d(1, 3, kernel_size=3, padding=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(x)


class ColorizationModel:
    """
    Image colorization model wrapper.
    """

    def __init__(
        self,
        model_path: str | Path | None = None,
        backend: str | None = None,
    ) -> None:
        """
        Initialize the colorization model.
        """
        self.model_path = Path(model_path or COLORIZATION_MODEL_PATH)
        self.backend = backend or COLORIZATION_BACKEND
        self.model: nn.Module | None = None
        self.model_loaded = False

    # ---------------------------------------------------------
    # Load Model
    # ---------------------------------------------------------

    def load(self) -> None:
        """
        Load deep learning model weights.
        """
        if self.model_loaded:
            return

        if self.backend == "opencv":
            # No weights needed for OpenCV backend
            self.model_loaded = True
            return

        # For "deep_learning" or "auto" backend, try to load PyTorch weights
        try:
            validate_weights(self.model_path)
            
            # Instantiate the network and load state dictionary
            self.model = ColorizationNet()
            
            # Attempt to load weights. If the file size is valid but content is corrupted,
            # torch.load will raise an exception.
            try:
                state_dict = torch.load(str(self.model_path), map_location="cpu")
                # If state_dict is valid, load it
                if isinstance(state_dict, nn.Module):
                    self.model = state_dict
                elif isinstance(state_dict, dict):
                    self.model.load_state_dict(state_dict, strict=False)
            except Exception as e:
                raise WeightsInvalidError(
                    f"Failed to parse or load PyTorch weights: {e}"
                ) from e
                
            self.model.eval()
            self.model_loaded = True
            logger.info("Successfully loaded deep-learning colorization weights.")
            
        except Exception as e:
            if self.backend == "deep_learning":
                logger.error(f"Failed to load required colorization weights: {e}")
                raise
            else:  # "auto" mode fallback
                logger.warning(
                    f"Colorization weights loading failed ({e}). Falling back to OpenCV Pseudo Color."
                )
                self.model_loaded = True  # We consider it "loaded" via the fallback backend

    # ---------------------------------------------------------
    # Colorize Image
    # ---------------------------------------------------------

    def colorize(
        self,
        input_path: str,
        output_path: str,
        color_map: int = cv2.COLORMAP_INFERNO,
    ) -> str:
        """
        Colorize an infrared image.
        """
        self.load()

        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Input image not found: {input_path}")

        # If model is loaded successfully (meaning valid weights are loaded) and backend is not opencv
        if self.backend in ("deep_learning", "auto") and self.model is not None:
            try:
                # Read grayscale image
                image = cv2.imread(str(input_file), cv2.IMREAD_GRAYSCALE)
                if image is None:
                    raise ValueError(f"Unable to read input image: {input_path}")

                if len(image.shape) == 3:
                    image = image.squeeze(-1)

                # Run simple PyTorch inference dummy pass
                # Convert to tensor [B, C, H, W] normalized
                h, w = image.shape[:2]
                tensor_in = torch.from_numpy(image).float().unsqueeze(0).unsqueeze(0) / 255.0
                
                with torch.no_grad():
                    tensor_out = self.model(tensor_in)
                    
                # Postprocess: convert output tensor back to numpy BGR image
                # Standardize output to 0-255 range
                numpy_out = tensor_out.squeeze(0).permute(1, 2, 0).cpu().numpy()
                numpy_out = np.clip(numpy_out * 255.0, 0, 255).astype(np.uint8)
                
                output = Path(output_path)
                output.parent.mkdir(parents=True, exist_ok=True)
                cv2.imwrite(str(output), numpy_out)
                return str(output)
            except Exception as e:
                if self.backend == "deep_learning":
                    raise RuntimeError(f"Deep learning colorization inference failed: {e}") from e
                logger.warning(
                    f"Deep learning colorization failed ({e}). Falling back to OpenCV."
                )

        # Fallback to OpenCV implementation
        image = cv2.imread(str(input_file), cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise FileNotFoundError(f"Image not found: {input_path}")

        # Standardize normalization as in service
        normalized = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        colorized = cv2.applyColorMap(normalized, color_map)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output), colorized)

        return str(output)

    # ---------------------------------------------------------
    # Colorize Array
    # ---------------------------------------------------------

    def colorize_array(
        self,
        image: np.ndarray,
        color_map: int = cv2.COLORMAP_INFERNO,
    ) -> np.ndarray:
        """
        Colorize an image already loaded into memory.
        """
        self.load()

        if image is None:
            raise ValueError("Invalid image supplied.")

        if len(image.shape) == 3:
            if image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            elif image.shape[2] == 1:
                image = image[:, :, 0]

        if self.backend in ("deep_learning", "auto") and self.model is not None:
            try:
                # DL processing
                tensor_in = torch.from_numpy(image).float().unsqueeze(0).unsqueeze(0) / 255.0
                with torch.no_grad():
                    tensor_out = self.model(tensor_in)
                numpy_out = tensor_out.squeeze(0).permute(1, 2, 0).cpu().numpy()
                numpy_out = np.clip(numpy_out * 255.0, 0, 255).astype(np.uint8)
                return numpy_out
            except Exception as e:
                if self.backend == "deep_learning":
                    raise RuntimeError(f"Deep learning colorization inference failed: {e}") from e
                logger.warning(
                    f"Deep learning colorization failed ({e}). Falling back to OpenCV."
                )

        # OpenCV processing
        normalized = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        colorized = cv2.applyColorMap(normalized, color_map)
        return colorized

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    def info(self) -> dict:
        """
        Return model information.
        """
        active_backend = self.backend
        if active_backend == "auto":
            active_backend = "deep_learning" if self.model is not None else "opencv"

        return {
            "name": f"Colorization Model ({active_backend.upper()})",
            "type": "Image Colorization",
            "loaded": self.model_loaded,
            "backend": active_backend,
            "weights_path": str(self.model_path),
            "dl_loaded": self.model is not None,
        }


# -------------------------------------------------------------
# Singleton
# -------------------------------------------------------------

colorization_model = ColorizationModel()