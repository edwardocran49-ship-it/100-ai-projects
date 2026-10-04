"""Download the public Kaggle source used by the license-plate workflow."""
from pathlib import Path

DATASET = "andrewmvd/car-plate-detection"
REFERENCE_IMAGE = "Cars379.png"


def ensure_dataset() -> Path:
    import kagglehub

    return Path(kagglehub.dataset_download(DATASET))


def load_reference_image() -> Path:
    path = ensure_dataset() / "images" / REFERENCE_IMAGE
    if not path.exists():
        raise FileNotFoundError(f"Expected {REFERENCE_IMAGE} in the downloaded Kaggle dataset")
    return path


if __name__ == "__main__":
    print(load_reference_image())
