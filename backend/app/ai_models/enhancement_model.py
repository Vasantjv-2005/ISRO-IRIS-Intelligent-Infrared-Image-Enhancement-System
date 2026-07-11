"""
Enhancement Model

Image enhancement wrapper supporting both OpenCV (CLAHE/Bilateral Filter)
and Deep Learning backends.
"""

from __future__ import annotations

import logging
from pathlib import Path

import cv2
import numpy as np

from app.core.config import ENHANCEMENT_BACKEND, ENHANCEMENT_MODEL_PATH
from app.ai_models.utils import validate_weights, torch, nn, TORCH_AVAILABLE
from app.middleware.error_handler import WeightsInvalidError

logger = logging.getLogger("iris")

_BaseModule = nn.Module if TORCH_AVAILABLE else object


class EnhancementNet(_BaseModule):
    """
    Production-ready PyTorch Zero-DCE (Zero-Reference Deep Curve Estimation) architecture
    for infrared and low-light image enhancement.
    """

    def __init__(self) -> None:
        super().__init__()
        if TORCH_AVAILABLE:
            self.relu = nn.ReLU(inplace=True)
            self.conv1 = nn.Conv2d(3, 32, 3, 1, 1)
            self.conv2 = nn.Conv2d(32, 32, 3, 1, 1)
            self.conv3 = nn.Conv2d(32, 32, 3, 1, 1)
            self.conv4 = nn.Conv2d(32, 32, 3, 1, 1)
            self.conv5 = nn.Conv2d(64, 32, 3, 1, 1)
            self.conv6 = nn.Conv2d(64, 32, 3, 1, 1)
            self.conv7 = nn.Conv2d(64, 24, 3, 1, 1)

    def forward(self, x: any) -> any:
        if not TORCH_AVAILABLE:
            return x
        x1 = self.relu(self.conv1(x))
        x2 = self.relu(self.conv2(x1))
        x3 = self.relu(self.conv3(x2))
        x4 = self.relu(self.conv4(x3))
        x5 = self.relu(self.conv5(torch.cat([x3, x4], 1)))
        x6 = self.relu(self.conv6(torch.cat([x2, x5], 1)))
        x_r = torch.tanh(self.conv7(torch.cat([x1, x6], 1)))
        
        # Apply 8 enhancement iterations using estimated curves
        r1, r2, r3, r4, r5, r6, r7, r8 = torch.split(x_r, 3, dim=1)
        x = x + r1 * (torch.pow(x, 2) - x)
        x = x + r2 * (torch.pow(x, 2) - x)
        x = x + r3 * (torch.pow(x, 2) - x)
        enhanced = x + r4 * (torch.pow(x, 2) - x)
        enhanced = enhanced + r5 * (torch.pow(enhanced, 2) - enhanced)
        enhanced = enhanced + r6 * (torch.pow(enhanced, 2) - enhanced)
        enhanced = enhanced + r7 * (torch.pow(enhanced, 2) - enhanced)
        enhanced = enhanced + r8 * (torch.pow(enhanced, 2) - enhanced)
        return torch.clamp(enhanced, 0.0, 1.0)


class EnhancementModel:
    """
    Image enhancement model wrapper.
    """

    def __init__(
        self,
        model_path: str | Path | None = None,
        backend: str | None = None,
    ) -> None:
        """
        Initialize the enhancement model.
        """
        self.model_path = Path(model_path or ENHANCEMENT_MODEL_PATH)
        self.backend = backend or ENHANCEMENT_BACKEND
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
        if not TORCH_AVAILABLE:
            if self.backend == "deep_learning":
                raise WeightsInvalidError("PyTorch is not available: DLL load failed or not installed.")
            else:  # "auto" mode fallback
                logger.warning("PyTorch not available. Falling back to OpenCV CLAHE.")
                self.model_loaded = True
                return

        try:
            validate_weights(self.model_path)
            
            # Instantiate the network and load state dictionary
            self.model = EnhancementNet()
            
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
            logger.info("Successfully loaded deep-learning enhancement weights.")
            
        except Exception as e:
            if self.backend == "deep_learning":
                logger.error(f"Failed to load required enhancement weights: {e}")
                raise
            else:  # "auto" mode fallback
                logger.warning(
                    f"Enhancement weights loading failed ({e}). Falling back to OpenCV CLAHE."
                )
                self.model_loaded = True  # We consider it "loaded" via the fallback backend

    # ---------------------------------------------------------
    # Enhance Image
    # ---------------------------------------------------------

    def enhance(
        self,
        input_path: str,
        output_path: str,
    ) -> str:
        """
        Enhance an infrared image.
        """
        self.load()

        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Input image not found: {input_path}")

        # If model is loaded successfully and backend is not opencv
        if self.backend in ("deep_learning", "auto") and self.model is not None and TORCH_AVAILABLE:
            try:
                # Read BGR image
                image = cv2.imread(str(input_file))
                if image is None:
                    raise ValueError(f"Unable to read input image: {input_path}")

                # Run simple PyTorch inference dummy pass
                # Convert to tensor [B, C, H, W] normalized
                tensor_in = torch.from_numpy(image).float().permute(2, 0, 1).unsqueeze(0) / 255.0
                
                with torch.no_grad():
                    tensor_out = self.model(tensor_in)
                    
                # Postprocess: convert output tensor back to numpy BGR image
                numpy_out = tensor_out.squeeze(0).permute(1, 2, 0).cpu().numpy()
                numpy_out = np.clip(numpy_out * 255.0, 0, 255).astype(np.uint8)
                
                output = Path(output_path)
                output.parent.mkdir(parents=True, exist_ok=True)
                cv2.imwrite(str(output), numpy_out)
                return str(output)
            except Exception as e:
                # If anything fails inside deep learning execution, raise or fallback
                if self.backend == "deep_learning":
                    raise RuntimeError(f"Deep learning enhancement inference failed: {e}") from e
                logger.warning(
                    f"Deep learning enhancement failed ({e}). Falling back to OpenCV."
                )

        # Fallback to OpenCV implementation
        image = cv2.imread(str(input_file))
        if image is None:
            raise FileNotFoundError(f"Image not found: {input_path}")

        enhanced = self.enhance_array(image)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output), enhanced)

        return str(output)

    # ---------------------------------------------------------
    # Enhance Array
    # ---------------------------------------------------------

    def enhance_array(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        """
        Enhance an image already loaded into memory.
        """
        self.load()

        if image is None:
            raise ValueError("Invalid image supplied.")

        if self.backend in ("deep_learning", "auto") and self.model is not None:
            try:
                # DL processing
                tensor_in = torch.from_numpy(image).float().permute(2, 0, 1).unsqueeze(0) / 255.0
                with torch.no_grad():
                    tensor_out = self.model(tensor_in)
                numpy_out = tensor_out.squeeze(0).permute(1, 2, 0).cpu().numpy()
                numpy_out = np.clip(numpy_out * 255.0, 0, 255).astype(np.uint8)
                return numpy_out
            except Exception as e:
                if self.backend == "deep_learning":
                    raise RuntimeError(f"Deep learning enhancement inference failed: {e}") from e
                logger.warning(
                    f"Deep learning enhancement failed ({e}). Falling back to OpenCV."
                )

        # High-definition OpenCV multi-scale enhancement (CLAHE + Bilateral Detail Boosting + Micro-Contrast)
        try:
            is_color = len(image.shape) == 3 and image.shape[2] == 3

            if is_color:
                # Convert to LAB color space to process luminance independently
                lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                l_channel, a_channel, b_channel = cv2.split(lab)

                # Edge-preserving bilateral filter to reduce sensor grain while retaining sharp foliage/water boundaries
                denoised_l = cv2.bilateralFilter(l_channel, d=7, sigmaColor=18, sigmaSpace=18)

                # Apply high-definition CLAHE for local contrast equalization
                clahe = cv2.createCLAHE(clipLimit=2.6, tileGridSize=(8, 8))
                enhanced_l = clahe.apply(denoised_l)

                # Extract and boost minute high-frequency structures (canopy edges, shorelines, fine roads)
                blur_detail = cv2.GaussianBlur(enhanced_l, (0, 0), 2.0)
                detail_layer = cv2.subtract(enhanced_l, blur_detail)
                boosted_l = cv2.addWeighted(enhanced_l, 1.0, detail_layer, 0.85, 0)

                # Merge back to BGR space
                merged = cv2.merge((boosted_l, a_channel, b_channel))
                enhanced = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
            else:
                # Grayscale image enhancement
                denoised = cv2.bilateralFilter(image, d=7, sigmaColor=18, sigmaSpace=18)
                clahe = cv2.createCLAHE(clipLimit=2.6, tileGridSize=(8, 8))
                enhanced = clahe.apply(denoised)

                blur_detail = cv2.GaussianBlur(enhanced, (0, 0), 2.0)
                detail_layer = cv2.subtract(enhanced, blur_detail)
                enhanced = cv2.addWeighted(enhanced, 1.0, detail_layer, 0.85, 0)

            # High-precision crisp unsharp masking
            blur_fine = cv2.GaussianBlur(enhanced, (0, 0), 1.0)
            sharpened = cv2.addWeighted(enhanced, 1.55, blur_fine, -0.55, 0)
            return np.clip(sharpened, 0, 255).astype(np.uint8)
        except Exception as e:
            raise RuntimeError(f"Failed to enhance image array: {e}") from e

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
            "name": f"Enhancement Model ({active_backend.upper()})",
            "type": "Image Enhancement",
            "loaded": self.model_loaded,
            "backend": active_backend,
            "weights_path": str(self.model_path),
            "dl_loaded": self.model is not None,
        }


# -------------------------------------------------------------
# Singleton
# -------------------------------------------------------------

enhancement_model = EnhancementModel()