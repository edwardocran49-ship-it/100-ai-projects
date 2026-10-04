"""Locate license-plate-shaped regions and read candidate text with EasyOCR."""
from __future__ import annotations

import argparse, json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.vision import plate_candidates, read_text

PROJECT_NUMBER, PROJECT_TITLE, AUTHOR = 45, "License Plate Detection", "Edward Ocran"


class _Reader:
    def readtext(self, image):
        h, w = image.shape[:2]
        return [([[0, 0], [w, 0], [w, h], [0, h]], "ABC 1234", .94)]


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if fast:
        import numpy as np
        image = np.full((120, 320, 3), 220, dtype=np.uint8)
        candidates = [(80, 55, 160, 40)]
    else:
        import cv2
        from download_data import load_reference_image
        source = load_reference_image()
        image = cv2.cvtColor(cv2.imread(str(source)), cv2.COLOR_BGR2RGB)
        if image is None:
            raise RuntimeError(f"Unable to read dataset image: {source}")
    if not fast:
        candidates = plate_candidates(image)
    x, y, width, height = candidates[0] if candidates else (0, 0, image.shape[1], image.shape[0])
    readings = read_text(image[y:y + height, x:x + width], reader=_Reader() if fast else None)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "dataset": "Kaggle Car Plate Detection (Cars379.png)",
            "model": "OpenCV contours + EasyOCR", "candidates": len(candidates), "readings": readings,
            "metrics": {"best_confidence": max((item["confidence"] for item in readings), default=0.0)}}


def main():
    parser = argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(); result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
