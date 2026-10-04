from pathlib import Path
import csv,requests
NAMES=["aspirin","ibuprofen","acetaminophen","naproxen","diclofenac","ketoprofen","celecoxib","meloxicam"]
rows=[]
for name in NAMES:
 url=f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/CanonicalSMILES/JSON"
 prop=requests.get(url,timeout=30).json()["PropertyTable"]["Properties"][0]
 rows.append({"drug":name.title(),"smiles":prop.get("ConnectivitySMILES") or prop.get("CanonicalSMILES")})
out=Path(__file__).parent/"data";out.mkdir(exist_ok=True)
with (out/"pubchem_drugs.csv").open("w",newline="",encoding="utf-8") as f:
 w=csv.DictWriter(f,fieldnames=["drug","smiles"]);w.writeheader();w.writerows(rows)
print("saved",len(rows),"PubChem compounds")
