from pathlib import Path
import io,requests,zipfile,shutil
URL="https://archive.ics.uci.edu/static/public/331/sentiment+labelled+sentences.zip"
out=Path(__file__).parent/"data";out.mkdir(exist_ok=True)
z=zipfile.ZipFile(io.BytesIO(requests.get(URL,timeout=120).content));name=next(x for x in z.namelist() if x.endswith('amazon_cells_labelled.txt'))
with z.open(name) as src,(out/'amazon_cells_labelled.txt').open('wb') as dst:shutil.copyfileobj(src,dst)
print('saved',out/'amazon_cells_labelled.txt')
