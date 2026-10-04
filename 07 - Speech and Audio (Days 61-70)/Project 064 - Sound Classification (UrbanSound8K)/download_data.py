"""Download a balanced, genuine UrbanSound8K subset from the HF dataset server."""
from pathlib import Path
from collections import Counter
import csv,re,requests

OUT=Path(__file__).parent/"data";OUT.mkdir(exist_ok=True)
API="https://datasets-server.huggingface.co/rows"
counts=Counter();rows=[]
for offset in range(0,5100,100):
    payload=requests.get(API,params={"dataset":"CLAPv2/Urbansound8K","config":"default","split":"train","offset":offset,"length":100},timeout=60).json()
    for item in payload.get("rows",[]):
        row=item["row"];label=re.sub(r"^The sound of |\.$","",row["text"]).replace(" ","_")
        if counts[label]>=30:continue
        source=row["audio"][0]["src"];name=f"{label}_{counts[label]:02d}.wav"
        content=requests.get(source,timeout=90).content;(OUT/name).write_bytes(content)
        rows.append({"file":name,"label":label,"source_file":row["raw_text"][0].removeprefix("File: ")});counts[label]+=1
    if len(counts)>=10 and min(counts.values())>=30:break
with (OUT/"manifest.csv").open("w",newline="",encoding="utf-8") as handle:
    writer=csv.DictWriter(handle,fieldnames=["file","label","source_file"]);writer.writeheader();writer.writerows(rows)
print(dict(counts),"total",len(rows))
