"""Detect faces with OpenCV and blur each detected region for privacy."""
from __future__ import annotations

import argparse, json, os, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.vision import blur_faces

PROJECT_NUMBER, PROJECT_TITLE, AUTHOR = 41, "Face Detection and Blur", "Edward Ocran"


class _Detector:
    def detectMultiScale(self, image, **kwargs):
        return np.asarray([[15, 15, 30, 30]])


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if fast:
        image = np.tile(np.arange(80, dtype=np.uint8), (80, 1))
        image = np.dstack([image] * 3)
        result = blur_faces(image, detector=_Detector(), kernel=15)
    else:
        from skimage import data
        from PIL import Image
        image = data.astronaut()
        result = blur_faces(image)
        output = HERE / "outputs" / "blurred_faces.png"
        output.parent.mkdir(exist_ok=True)
        Image.fromarray(result["image"]).save(output)
    reduction = [1 - item["sharpness_after"] / max(item["sharpness_before"], 1e-9) for item in result["faces"]]
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "model": "OpenCV Haar cascade", "faces_detected": len(result["faces"]),
            "metrics": {"mean_sharpness_reduction": round(float(np.mean(reduction)), 4) if reduction else 0.0},
            "regions": result["faces"]}


def main():
    parser = argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(); result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
