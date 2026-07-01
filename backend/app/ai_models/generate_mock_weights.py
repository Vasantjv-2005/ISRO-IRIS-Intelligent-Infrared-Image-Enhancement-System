"""
Generate Mock Weight Files for IRIS AI Models.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import torch
from ultralytics import YOLO

from app.ai_models.colorization_model import ColorizationNet
from app.ai_models.enhancement_model import EnhancementNet


def main() -> None:
    weights_dir = Path("weights")
    colorization_path = weights_dir / "colorization" / "colorization_model.pth"
    enhancement_path = weights_dir / "enhancement" / "enhancement_model.pth"
    yolo_path = weights_dir / "detection" / "yolov8.pt"

    # Create directories if they do not exist
    colorization_path.parent.mkdir(parents=True, exist_ok=True)
    enhancement_path.parent.mkdir(parents=True, exist_ok=True)
    yolo_path.parent.mkdir(parents=True, exist_ok=True)

    print("Generating mock colorization weights...")
    color_model = ColorizationNet()
    torch.save(color_model.state_dict(), str(colorization_path))
    print(f"Saved: {colorization_path.absolute()}")

    print("Generating mock enhancement weights...")
    enhance_model = EnhancementNet()
    torch.save(enhance_model.state_dict(), str(enhancement_path))
    print(f"Saved: {enhancement_path.absolute()}")

    print("Downloading/Saving YOLOv8 model weights...")
    try:
        # Load small yolov8n model (will auto-download if not present)
        # We save it to the target path.
        yolo_model = YOLO("yolov8n.pt")
        src_path = Path("yolov8n.pt")
        if src_path.exists():
            shutil.copy(str(src_path), str(yolo_path))
            print(f"Copied local yolov8n.pt to {yolo_path.absolute()}")
            # clean up temp download in backend root
            try:
                src_path.unlink()
            except Exception:
                pass
        else:
            yolo_model.save(str(yolo_path))
            print(f"Saved YOLOv8 weights to {yolo_path.absolute()}")
    except Exception as e:
        print(f"Warning: Failed to download YOLOv8 model weights: {e}")


if __name__ == "__main__":
    main()
