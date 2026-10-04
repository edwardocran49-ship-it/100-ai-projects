"""Detect and label objects with the Ultralytics YOLOv8 nano model."""
from __future__ import annotations

import argparse, json, os, sys
from collections import Counter
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.vision import detect_objects

PROJECT_NUMBER, PROJECT_TITLE, AUTHOR = 43, "Object Detection with YOLOv8", "Edward Ocran"


def _validation_backend(image):
    return [{"label": "person", "confidence": .91, "box": [5, 4, 50, 60]}]


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if fast:
        image = Image.new("RGB", (64, 64), "white")
    else:
        from skimage import data
        image = Image.fromarray(data.astronaut())
    detections = detect_objects(image, backend=_validation_backend if fast else None)
    counts = Counter(item["label"] for item in detections)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "model": "YOLOv8n", "detections": detections,
            "metrics": {"objects_detected": len(detections), "classes": dict(sorted(counts.items())),
                        "mean_confidence": round(sum(item["confidence"] for item in detections) / max(len(detections), 1), 4)}}


def main():
    parser = argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(); result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
