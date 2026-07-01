"""
Colorization Model

Image colorization wrapper.

Current backend:
    OpenCV (Pseudo Color)

Future backend:
    Palette / DeOldify / Custom PyTorch Model
"""

from __future__ import annotations

from pathlib import Path

import cv2


class ColorizationModel:
    """
    Image colorization model.
    """

    def __init__(self) -> None:
        self.model_loaded = True

    # ---------------------------------------------------------
    # Load Model
    # ---------------------------------------------------------

    def load(self) -> None:
        """
        Placeholder.

        Later this method will load a deep learning
        colorization model.
        """
        self.model_loaded = True

    # ---------------------------------------------------------
    # Colorize Image
    # ---------------------------------------------------------

    def colorize(
        self,
        input_path: str,
        output_path: str,
        color_map: int = cv2.COLORMAP_JET,
    ) -> str:
        """
        Apply pseudo color to an infrared image.
        """

        image = cv2.imread(
            input_path,
            cv2.IMREAD_GRAYSCALE,
        )

        if image is None:
            raise FileNotFoundError(
                f"Image not found: {input_path}"
            )

        colorized = cv2.applyColorMap(
            image,
            color_map,
        )

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cv2.imwrite(
            str(output),
            colorized,
        )

        return str(output)

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    def info(self) -> dict:
        """
        Return model information.
        """

        return {
            "name": "OpenCV Pseudo Color",
            "type": "Image Colorization",
            "loaded": self.model_loaded,
            "future_model": "Palette / DeOldify",
        }


# -------------------------------------------------------------
# Singleton
# -------------------------------------------------------------

colorization_model = ColorizationModel()