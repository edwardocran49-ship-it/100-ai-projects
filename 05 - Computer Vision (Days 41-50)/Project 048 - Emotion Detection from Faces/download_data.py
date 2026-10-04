from pathlib import Path
import kagglehub

HANDLE = "msambare/fer2013"


def ensure_dataset() -> Path:
    root = Path(kagglehub.dataset_download(HANDLE))
    if not (root / "train").exists():
        raise FileNotFoundError(root / "train")
    return root


if __name__ == "__main__":
    print(ensure_dataset())
