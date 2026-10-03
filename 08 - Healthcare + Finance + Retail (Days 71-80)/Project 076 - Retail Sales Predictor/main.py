"""Runnable offline demonstration for Project 76: Retail Sales Predictor.

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

PROJECT_NUMBER = 76
PROJECT_TITLE = 'Retail Sales Predictor'
AUTHOR = "Edward Ocran"
SEED = 1000 + PROJECT_NUMBER

def fit_line(xs: list[float], ys: list[float]) -> tuple[float, float]:
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / denominator
    return slope, y_mean - slope * x_mean


def run_demo() -> dict[str, Any]:
    rng = random.Random(SEED)
    xs = [float(i) for i in range(1, 61)]
    expected_slope = 1.25 + (PROJECT_NUMBER % 9) / 10
    ys = [expected_slope * x + 7 + rng.uniform(-2.0, 2.0) for x in xs]
    slope, intercept = fit_line(xs[:48], ys[:48])
    predictions = [slope * x + intercept for x in xs[48:]]
    actual = ys[48:]
    mae = sum(abs(a - p) for a, p in zip(actual, predictions)) / len(actual)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "status": "ok",
            "task": "regression", "metrics": {"mae": round(mae, 4), "slope": round(slope, 4)},
            "sample_prediction": round(predictions[0], 3)}

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
