"""
Enhancement Model

Image enhancement wrapper.

Current backend:
    OpenCV (CLAHE)

Future backend:
    MIRNet / Zero-DCE / Custom PyTorch model
"""

from __future__ import annotations

from pathlib import Path

import cv2


class EnhancementModel:
    """
    Image enhancement model.
    """

    def __init__(self) -> None:
        self.model_loaded = True

    # ---------------------------------------------------------
    # Load Model
    # ---------------------------------------------------------

    def load(self) -> None:
        """
        Placeholder.

        Later this method will load the MIRNet weights.
        """
        self.model_loaded = True

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

        image = cv2.imread(input_path)

        if image is None:
            raise FileNotFoundError(
                f"Image not found: {input_path}"
            )

        # -----------------------------------------
        # Convert to LAB
        # -----------------------------------------

        lab = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2LAB,
        )

        l_channel, a_channel, b_channel = cv2.split(
            lab
        )

        # -----------------------------------------
        # CLAHE
        # -----------------------------------------

        clahe = cv2.createCLAHE(
            clipLimit=3.0,
            tileGridSize=(8, 8),
        )

        enhanced_l = clahe.apply(
            l_channel
        )

        enhanced = cv2.merge(
            (
                enhanced_l,
                a_channel,
                b_channel,
            )
        )

        enhanced = cv2.cvtColor(
            enhanced,
            cv2.COLOR_LAB2BGR,
        )

        # -----------------------------------------
        # Save
        # -----------------------------------------

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cv2.imwrite(
            str(output),
            enhanced,
        )

        return str(output)

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    def info(self) -> dict:
        """
        Model information.
        """

        return {
            "name": "OpenCV CLAHE",
            "type": "Image Enhancement",
            "loaded": self.model_loaded,
            "future_model": "MIRNet",
        }


# -------------------------------------------------------------
# Singleton
# -------------------------------------------------------------

enhancement_model = EnhancementModel()