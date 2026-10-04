"""Extract and score text regions from a photographed note with EasyOCR."""
from __future__ import annotations

import argparse, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.vision import read_text

PROJECT_NUMBER, PROJECT_TITLE, AUTHOR = 46, "OCR for Handwritten Notes", "Edward Ocran"


class _Reader:
    def readtext(self, image):
        return [([[5, 5], [55, 5], [55, 20], [5, 20]], "Review the figures", .92),
                ([[5, 25], [60, 25], [60, 40], [5, 40]], "before Friday", .88)]


def _edit_distance(left, right):
    previous = list(range(len(right) + 1))
    for row, left_item in enumerate(left, 1):
        current = [row]
        for column, right_item in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[column] + 1,
                               previous[column - 1] + (left_item != right_item)))
        previous = current
    return previous[-1]


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if fast:
        import numpy as np
        image = np.full((64, 320, 3), 255, dtype=np.uint8)
        expected = "Review the figures before Friday"
    else:
        from download_data import load_reference_line
        image, expected = load_reference_line()
    readings = read_text(image, reader=_Reader() if fast else None)
    transcript = " ".join(item["text"] for item in readings)
    reference_normalized, transcript_normalized = expected.lower(), transcript.lower()
    character_error_rate = _edit_distance(reference_normalized, transcript_normalized) / max(len(reference_normalized), 1)
    word_error_rate = _edit_distance(reference_normalized.split(), transcript_normalized.split()) / max(len(reference_normalized.split()), 1)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "dataset": "IAM Handwriting Database (IAM-line)", "model": "EasyOCR English",
            "reference_text": expected, "transcript": transcript, "readings": readings,
            "metrics": {"regions": len(readings), "mean_confidence": round(sum(item["confidence"] for item in readings) / max(len(readings), 1), 4),
                        "character_error_rate": round(character_error_rate, 4), "word_error_rate": round(word_error_rate, 4)}}


def main():
    parser = argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(); result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
