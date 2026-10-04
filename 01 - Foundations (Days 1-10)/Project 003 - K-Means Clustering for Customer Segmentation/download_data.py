"""Download the public Kaggle source into this project's data directory."""
from pathlib import Path
import shutil
import contextlib
import io
import kagglehub

DESTINATION = Path(__file__).with_name("data") / "Mall_Customers.csv"

def ensure_dataset() -> Path:
    if not DESTINATION.exists():
        with contextlib.redirect_stdout(io.StringIO()):
            source_dir = Path(kagglehub.dataset_download("shwetabh123/mall-customers"))
        DESTINATION.parent.mkdir(exist_ok=True)
        shutil.copy2(source_dir / "Mall_Customers.csv", DESTINATION)
    return DESTINATION

if __name__ == "__main__":
    print(ensure_dataset())
