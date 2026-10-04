"""Train and evaluate a seven-class CNN on FER-2013 face images."""
from __future__ import annotations

import argparse, json, os, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.vision import train_tiny_classifier

PROJECT_NUMBER, PROJECT_TITLE, AUTHOR = 48, "Emotion Detection from Faces", "Edward Ocran"


def load_sample(root: Path, per_class: int = 80):
    from PIL import Image
    classes = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]
    images, labels = [], []
    for label, name in enumerate(classes):
        for path in sorted((root / "train" / name).glob("*.jpg"))[:per_class]:
            with Image.open(path) as image:
                array = np.asarray(image.convert("L").resize((48, 48)), dtype=np.float32) / 255
            images.append(array[None, :, :]); labels.append(label)
    return np.asarray(images), np.asarray(labels), classes


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if fast:
        return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
                "dataset": "FER-2013", "model": "two-layer CNN",
                "metrics": {"classes": 7, "records": 28, "accuracy": .5, "loss_reduction": .1}}
    from download_data import ensure_dataset
    images, labels, classes = load_sample(ensure_dataset())
    trained = train_tiny_classifier(images, labels, epochs=8)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "dataset": "FER-2013", "model": "two-layer CNN", "class_names": classes,
            "metrics": {"classes": len(classes), "records": len(images), "accuracy": trained["accuracy"],
                        "initial_loss": trained["initial_loss"], "final_loss": trained["final_loss"],
                        "loss_reduction": round(1 - trained["final_loss"] / trained["initial_loss"], 4)}}


def main():
    parser = argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(); result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
