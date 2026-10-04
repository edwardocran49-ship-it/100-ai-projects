from pathlib import Path
import kagglehub

HANDLE = "balraj98/deepglobe-land-cover-classification-dataset"


def ensure_dataset() -> Path:
    root = Path(kagglehub.dataset_download(HANDLE))
    if not root.exists():
        raise FileNotFoundError(root)
    return root


if __name__ == "__main__":
    print(ensure_dataset())
