"""Evaluate a pretrained BERT-family sentiment model on labelled reviews."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.nlp import classify_sentiment, evaluate_sentiment

PROJECT_NUMBER = 31
PROJECT_TITLE = "Sentiment Analysis with BERT"
AUTHOR = "Edward Ocran"


def _validation_backend(texts):
    return [{"label": "POSITIVE" if "excellent" in text.lower() else "NEGATIVE", "score": 0.99} for text in texts]


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if fast:
        rows = [{"text": "An excellent film.", "label": 1}, {"text": "A dull film.", "label": 0}]
        metrics = evaluate_sentiment(rows, backend=_validation_backend)
        sample = classify_sentiment([rows[0]["text"]], backend=_validation_backend)[0]
    else:
        import pandas as pd
        from download_data import ensure_dataset

        frame = pd.read_csv(ensure_dataset())
        positive = frame[frame["sentiment"].str.lower() == "positive"].sample(100, random_state=31)
        negative = frame[frame["sentiment"].str.lower() == "negative"].sample(100, random_state=31)
        sample_frame = pd.concat([positive, negative]).sample(frac=1, random_state=31)
        rows = [{"text": row.review, "label": int(row.sentiment.lower() == "positive")}
                for row in sample_frame.itertuples()]
        metrics = evaluate_sentiment(rows)
        sample = classify_sentiment(["The performances hold the story together."])[0]
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR,
            "status": "ok", "model": "distilbert-base-uncased-finetuned-sst-2-english",
            "dataset": "IMDb Dataset of 50K Movie Reviews", "metrics": metrics, "sample_prediction": sample}


def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
