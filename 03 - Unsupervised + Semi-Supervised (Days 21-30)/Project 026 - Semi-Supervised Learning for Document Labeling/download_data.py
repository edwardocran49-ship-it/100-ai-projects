from pathlib import Path
import contextlib, io
import kagglehub

HANDLE = "lakshmi25npathi/imdb-dataset-of-50k-movie-reviews"
FILENAME = "IMDB Dataset.csv"

def ensure_dataset() -> Path:
    owner, slug = HANDLE.split("/", 1)
    versions = Path.home() / ".cache" / "kagglehub" / "datasets" / owner / slug / "versions"
    cached = sorted(versions.glob(f"*/{FILENAME}")) if versions.exists() else []
    if cached: return cached[-1]
    with contextlib.redirect_stdout(io.StringIO()): source = Path(kagglehub.dataset_download(HANDLE))
    path = source / FILENAME
    if not path.exists(): raise FileNotFoundError(path)
    return path
