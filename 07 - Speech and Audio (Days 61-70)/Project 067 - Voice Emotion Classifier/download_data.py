"""Retrieve RAVDESS from Kaggle and copy a balanced speech subset locally."""
from pathlib import Path
from collections import Counter
import shutil,kagglehub

source=Path(kagglehub.dataset_download("uwrfkaggler/ravdess-emotional-speech-audio"))
out=Path(__file__).parent/"data";out.mkdir(exist_ok=True)
counts=Counter()
for path in sorted(source.rglob("*.wav")):
    parts=path.stem.split("-")
    if len(parts)<3 or counts[parts[2]]>=24:continue
    shutil.copy2(path,out/path.name);counts[parts[2]]+=1
print("RAVDESS subset",dict(counts),"saved to",out)
