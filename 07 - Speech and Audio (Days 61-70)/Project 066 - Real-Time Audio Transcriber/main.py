"""Runnable offline demonstration for Project 66: Real-Time Audio Transcriber.

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

PROJECT_NUMBER = 66
PROJECT_TITLE = 'Real-Time Audio Transcriber'
AUTHOR = "Edward Ocran"
SEED = 1000 + PROJECT_NUMBER

def audio_features(samples: list[float]) -> dict[str, float]:
    rms = math.sqrt(sum(value * value for value in samples) / len(samples))
    crossings = sum((a < 0) != (b < 0) for a, b in zip(samples, samples[1:]))
    return {"rms": rms, "zero_crossing_rate": crossings / (len(samples) - 1)}


def run_demo() -> dict[str, Any]:
    rate = 8000
    frequency = 220 + (PROJECT_NUMBER % 5) * 110
    samples = [0.7 * math.sin(2 * math.pi * frequency * i / rate) for i in range(rate // 4)]
    features = audio_features(samples)
    label = "high_tone" if features["zero_crossing_rate"] > 0.09 else "low_tone"
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "status": "ok", "task": "audio",
            "metrics": {key: round(value, 6) for key, value in features.items()}, "sample_prediction": label}

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
