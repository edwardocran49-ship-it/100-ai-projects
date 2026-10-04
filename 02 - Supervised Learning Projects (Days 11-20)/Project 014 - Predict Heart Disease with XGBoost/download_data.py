"""Resolve the project dataset through KaggleHub's versioned local cache."""
from pathlib import Path
import contextlib
import io
import kagglehub

HANDLE = "johnsmith88/heart-disease-dataset"
FILENAME = "heart.csv"

def ensure_dataset() -> Path:
    owner, slug = HANDLE.split("/", 1)
    versions = Path.home() / ".cache" / "kagglehub" / "datasets" / owner / slug / "versions"
    cached = sorted(versions.glob(f"*/{FILENAME}")) if versions.exists() else []
    if cached:
        return cached[-1]
    with contextlib.redirect_stdout(io.StringIO()):
        source_dir = Path(kagglehub.dataset_download(HANDLE))
    path = source_dir / FILENAME
    if not path.exists():
        raise FileNotFoundError(f"{FILENAME} was not found in {source_dir}")
    return path

if __name__ == "__main__":
    print(ensure_dataset())
