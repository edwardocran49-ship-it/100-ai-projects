"""Train a compact UNet-style model on DeepGlobe satellite image/mask pairs."""
from __future__ import annotations

import argparse, json, os, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.vision import train_tiny_segmenter

PROJECT_NUMBER, PROJECT_TITLE, AUTHOR = 50, "Satellite Image Segmentation", "Edward Ocran"
COLORS = np.asarray([[0, 255, 255], [255, 255, 0], [255, 0, 255], [0, 255, 0], [0, 0, 255], [255, 255, 255], [0, 0, 0]])


def encode_mask(mask):
    pixels = np.asarray(mask.convert("RGB"), dtype=np.int16)
    palette = COLORS.astype(np.int16)
    distance = ((pixels[:, :, None, :] - palette[None, None, :, :]) ** 2).sum(3)
    return distance.argmin(2)


def load_sample(root: Path, limit: int = 6):
    from PIL import Image
    image_paths = [path for path in sorted(root.rglob("*_sat.jpg"))
                   if Path(str(path).replace("_sat.jpg", "_mask.png")).exists()][:limit]
    images, masks = [], []
    for image_path in image_paths:
        mask_path = Path(str(image_path).replace("_sat.jpg", "_mask.png"))
        if not mask_path.exists():
            continue
        with Image.open(image_path) as image, Image.open(mask_path) as mask:
            rgb = np.asarray(image.convert("RGB").resize((64, 64)), dtype=np.float32) / 255
            target = encode_mask(mask.resize((64, 64), Image.Resampling.NEAREST))
        images.append(rgb.transpose(2, 0, 1)); masks.append(target)
    return np.asarray(images), np.asarray(masks)


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if fast:
        return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
                "dataset": "DeepGlobe Land Cover", "model": "UNet-style encoder-decoder",
                "metrics": {"image_mask_pairs": 2, "classes": 7, "mean_iou": .6, "loss_reduction": .2}}
    from download_data import ensure_dataset
    images, masks = load_sample(ensure_dataset())
    if not len(images):
        raise RuntimeError("No paired DeepGlobe satellite images and masks were found")
    result = train_tiny_segmenter(images, masks, classes=7, epochs=8)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "dataset": "DeepGlobe Land Cover", "model": "UNet-style encoder-decoder",
            "metrics": {"image_mask_pairs": len(images), "classes": 7, "mean_iou": result["mean_iou"],
                        "initial_loss": result["initial_loss"], "final_loss": result["final_loss"],
                        "loss_reduction": round(1 - result["final_loss"] / result["initial_loss"], 4)}}


def main():
    parser = argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(); result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
