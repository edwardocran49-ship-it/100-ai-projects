"""Download the public Kaggle source into this project's data directory."""
from pathlib import Path
import shutil
import kagglehub

DESTINATION = Path(__file__).with_name("data") / "spam.csv"

def ensure_dataset() -> Path:
    if not DESTINATION.exists():
        source_dir = Path(kagglehub.dataset_download("uciml/sms-spam-collection-dataset"))
        DESTINATION.parent.mkdir(exist_ok=True)
        shutil.copy2(source_dir / "spam.csv", DESTINATION)
    return DESTINATION

if __name__ == "__main__":
    print(ensure_dataset())
