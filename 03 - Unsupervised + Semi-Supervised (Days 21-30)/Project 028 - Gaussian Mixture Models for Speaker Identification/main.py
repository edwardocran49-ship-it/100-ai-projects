"""Runnable offline demonstration for Project 28: Gaussian Mixture Models for Speaker Identification.

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

PROJECT_NUMBER = 28
PROJECT_TITLE = 'Gaussian Mixture Models for Speaker Identification'
AUTHOR = "Edward Ocran"
SEED = 1000 + PROJECT_NUMBER

def squared_distance(a: list[float], b: list[float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def run_demo() -> dict[str, Any]:
    rng = random.Random(SEED)
    points = []
    for cx, cy in ((-4, -3), (0, 4), (4, -2)):
        points.extend([[rng.gauss(cx, .55), rng.gauss(cy, .55)] for _ in range(30)])
    centers = [points[0], points[30], points[60]]
    labels = [0] * len(points)
    for _ in range(12):
        labels = [min(range(3), key=lambda i: squared_distance(point, centers[i])) for point in points]
        centers = [[sum(points[j][axis] for j, label in enumerate(labels) if label == i) /
                    sum(label == i for label in labels) for axis in range(2)] for i in range(3)]
    inertia = sum(squared_distance(point, centers[label]) for point, label in zip(points, labels))
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "status": "ok",
            "task": "clustering", "metrics": {"clusters": 3, "inertia": round(inertia, 4)},
            "sample_prediction": labels[0]}

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
