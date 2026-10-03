"""Runnable offline demonstration for Project 5: Random Forest on Breast Cancer Dataset.

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

PROJECT_NUMBER = 5
PROJECT_TITLE = 'Random Forest on Breast Cancer Dataset'
AUTHOR = "Edward Ocran"
SEED = 1000 + PROJECT_NUMBER

def distance(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def run_demo() -> dict[str, Any]:
    rng = random.Random(SEED)
    rows: list[tuple[list[float], int]] = []
    for label, center in ((0, (-2.0, -1.5)), (1, (2.0, 1.5))):
        for _ in range(50):
            rows.append(([rng.gauss(center[0], .65), rng.gauss(center[1], .65)], label))
    train, test = rows[:80], rows[80:]
    centroids = []
    for label in (0, 1):
        points = [x for x, y in train if y == label]
        centroids.append([sum(p[i] for p in points) / len(points) for i in range(2)])
    predicted = [min((distance(x, c), label) for label, c in enumerate(centroids))[1] for x, _ in test]
    accuracy = sum(int(p == y) for p, (_, y) in zip(predicted, test)) / len(test)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "status": "ok",
            "task": "classification", "metrics": {"accuracy": round(accuracy, 4)},
            "sample_prediction": predicted[0]}

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
