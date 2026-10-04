from pathlib import Path
import kagglehub

HANDLE = "emmarex/plantdisease"


def ensure_dataset() -> Path:
    root = Path(kagglehub.dataset_download(HANDLE)) / "PlantVillage"
    if not root.exists():
        raise FileNotFoundError(root)
    return root


if __name__ == "__main__":
    print(ensure_dataset())
