"""Download and unpack the compact English Vosk model used by audio projects."""
from pathlib import Path
import io,requests,zipfile

URLS=[
"https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
"https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip",
"https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip",
]
root=Path(__file__).resolve().parents[1]/".models";root.mkdir(exist_ok=True)
for url in URLS:
    name=Path(url).stem;target=root/name
    if not target.exists():
        response=requests.get(url,timeout=180);response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as archive:archive.extractall(root)
    print(target)
