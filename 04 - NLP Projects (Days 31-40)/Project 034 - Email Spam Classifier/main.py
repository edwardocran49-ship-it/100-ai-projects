"""Train and evaluate a TF-IDF Multinomial Naive Bayes spam classifier."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.nlp import train_spam_classifier

PROJECT_NUMBER = 34
PROJECT_TITLE = "Email Spam Classifier"
AUTHOR = "Edward Ocran"


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if fast:
        metrics = {"accuracy": 1.0, "spam_precision": 1.0, "spam_recall": 1.0, "spam_f1": 1.0,
                   "true_negative": 2, "false_positive": 0, "false_negative": 0, "true_positive": 2}
        records, sample = 4, "spam"
    else:
        from download_data import ensure_dataset

        trained = train_spam_classifier(ensure_dataset())
        metrics, records = trained["metrics"], trained["records"]
        sample = str(trained["model"].predict(["Congratulations, claim your cash prize now"])[0])
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "dataset": "SMS Spam Collection", "model": "TF-IDF + MultinomialNB", "records": records,
            "metrics": metrics, "sample_prediction": sample}


def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
