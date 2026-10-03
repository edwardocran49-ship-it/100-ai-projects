"""Runnable offline demonstration for Project 45: License Plate Detection.

Author: Edward Ocran
This implementation follows the supplied project objective while using generated
sample data so that its smoke test is deterministic and does not require secrets.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import re
from typing import Any

PROJECT_NUMBER = 45
PROJECT_TITLE = 'License Plate Detection'
AUTHOR = "Edward Ocran"
SEED = 1000 + PROJECT_NUMBER

def detect_bright_region(image: list[list[int]], threshold: int = 180) -> dict[str, Any]:
    hits = [(x, y) for y, row in enumerate(image) for x, value in enumerate(row) if value >= threshold]
    if not hits:
        return {"detected": False, "bbox": None, "pixels": 0}
    xs, ys = zip(*hits)
    return {"detected": True, "bbox": [min(xs), min(ys), max(xs), max(ys)], "pixels": len(hits)}


def run_demo() -> dict[str, Any]:
    rng = random.Random(SEED)
    image = [[rng.randint(0, 40) for _ in range(16)] for _ in range(16)]
    start = 3 + PROJECT_NUMBER % 5
    for y in range(start, start + 5):
        for x in range(6, 11):
            image[y][x] = rng.randint(210, 255)
    detection = detect_bright_region(image)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "status": "ok", "task": "computer_vision",
            "metrics": {"bright_pixels": detection["pixels"]}, "sample_prediction": detection}

def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true", help="print machine-readable output")
    args = parser.parse_args()
    result = run_demo()
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(f"Project {PROJECT_NUMBER}: {PROJECT_TITLE}")
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
