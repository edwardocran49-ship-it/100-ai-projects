"""Train and evaluate a housing-price baseline on the Boston Housing data."""
from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path
from typing import Any

PROJECT_NUMBER = 1
PROJECT_TITLE = "Predict House Prices (Boston Housing Dataset)"
AUTHOR = "Edward Ocran"
DATA_FILE = Path(__file__).with_name("data") / "HousingData.csv"


def load_dataset(path: Path = DATA_FILE) -> list[tuple[float, float]]:
    """Return complete RM/MEDV observations from the downloaded Kaggle CSV."""
    rows: list[tuple[float, float]] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            if row.get("RM") and row.get("MEDV"):
                rows.append((float(row["RM"]), float(row["MEDV"])))
    if len(rows) < 400:
        raise ValueError(f"Expected the Boston Housing data; found only {len(rows)} usable rows")
    return rows


def fit_line(rows: list[tuple[float, float]]) -> tuple[float, float]:
    x_mean = sum(x for x, _ in rows) / len(rows)
    y_mean = sum(y for _, y in rows) / len(rows)
    denominator = sum((x - x_mean) ** 2 for x, _ in rows)
    slope = sum((x - x_mean) * (y - y_mean) for x, y in rows) / denominator
    return slope, y_mean - slope * x_mean


def run_demo() -> dict[str, Any]:
    rows = load_dataset()
    random.Random(1001).shuffle(rows)
    split = int(len(rows) * 0.8)
    train, test = rows[:split], rows[split:]
    slope, intercept = fit_line(train)
    predictions = [slope * rooms + intercept for rooms, _ in test]
    mae = sum(abs(actual - predicted) for (_, actual), predicted in zip(test, predictions)) / len(test)
    return {
        "project": PROJECT_NUMBER,
        "title": PROJECT_TITLE,
        "author": AUTHOR,
        "status": "ok",
        "task": "regression",
        "dataset": "Boston Housing",
        "source": "Kaggle: altavish/boston-housing-dataset",
        "records": len(rows),
        "features_used": ["RM"],
        "target": "MEDV",
        "metrics": {"mae": round(mae, 4), "slope": round(slope, 4)},
        "sample_prediction": round(predictions[0], 3),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true", help="print machine-readable output")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
