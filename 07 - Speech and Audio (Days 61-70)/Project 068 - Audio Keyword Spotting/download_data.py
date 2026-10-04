"""Download the official Speech Commands v0.01 test archive and extract 10 keywords."""
from pathlib import Path
from collections import Counter
import io,requests,tarfile

URL="https://s3.amazonaws.com/datasets.huggingface.co/SpeechCommands/v0.01/v0.01_test.tar.gz"
WORDS={"yes","no","up","down","left","right","on","off","stop","go"};LIMIT=100
out=Path(__file__).parent/"data";out.mkdir(exist_ok=True)
response=requests.get(URL,timeout=180);response.raise_for_status();counts=Counter()
with tarfile.open(fileobj=io.BytesIO(response.content),mode="r:gz") as archive:
    for member in archive:
        parts=Path(member.name).parts
        if not member.isfile() or len(parts)<2 or parts[-2] not in WORDS or counts[parts[-2]]>=LIMIT:continue
        target=out/parts[-2]/parts[-1];target.parent.mkdir(exist_ok=True)
        with archive.extractfile(member) as source:target.write_bytes(source.read())
        counts[parts[-2]]+=1
        if len(counts)==10 and min(counts.values())>=LIMIT:break
print("Speech Commands subset",dict(counts),"saved to",out)
