"""Load one genuine IAM handwritten line through the public Hugging Face mirror."""
from __future__ import annotations

import numpy as np

DATASET = "anris05/IAM-line"


def load_reference_line() -> tuple[np.ndarray, str]:
    from datasets import load_dataset

    row = next(iter(load_dataset(DATASET, split="train", streaming=True)))
    return np.asarray(row["image"].convert("RGB")), str(row["text"])


if __name__ == "__main__":
    image, text = load_reference_line()
    print({"shape": image.shape, "text": text})
