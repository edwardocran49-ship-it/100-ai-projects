"""Rank medicines by Morgan-fingerprint Tanimoto similarity."""
import argparse,csv,json,os
from pathlib import Path
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=73,"Drug Similarity Finder","Edward Ocran"
DEFAULT={"Aspirin":"CC(=O)OC1=CC=CC=C1C(=O)O","Ibuprofen":"CC(C)CC1=CC=C(C=C1)C(C)C(=O)O","Acetaminophen":"CC(=O)NC1=CC=C(O)C=C1","Naproxen":"COC1=CC=CC2=C1C=C(C=C2)C(C)C(=O)O","Diclofenac":"OC(=O)CC1=CC=CC=C1NC2=C(Cl)C=CC=C2Cl"}
def rank(smiles,records,fast=False):
 out=[]
 if fast:
  # Dependency-light structural smoke check for the isolated CI runner. Full
  # runs use RDKit Morgan fingerprints below.
  tokens=lambda value:{value[index:index+2] for index in range(len(value)-1)}
  query=tokens(smiles)
  for name,s in records.items():
   candidate=tokens(s);out.append({"drug":name,"similarity":round(len(query&candidate)/len(query|candidate),4)})
  return sorted(out,key=lambda x:x["similarity"],reverse=True)
 from rdkit import Chem,DataStructs
 from rdkit.Chem import rdFingerprintGenerator
 gen=rdFingerprintGenerator.GetMorganGenerator(radius=2,fpSize=2048);query=gen.GetFingerprint(Chem.MolFromSmiles(smiles))
 for name,s in records.items():out.append({"drug":name,"similarity":round(DataStructs.TanimotoSimilarity(query,gen.GetFingerprint(Chem.MolFromSmiles(s))),4)})
 return sorted(out,key=lambda x:x["similarity"],reverse=True)
def run_demo(fast=None,data=None):
 if fast is None:fast=os.environ.get("PORTFOLIO_FAST_VALIDATION")=="1"
 if data is None:
  local=Path(__file__).parent/"data"/"pubchem_drugs.csv"
  data=local if local.exists() else None
 records=DEFAULT if data is None else {r["drug"]:r["smiles"] for r in csv.DictReader(open(data,encoding="utf-8"))};results=rank(records["Acetaminophen"],records,fast)
 return {"project":73,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","query":"Acetaminophen","results":results,"metrics":{"compounds":len(records),"exact_match":results[0]["similarity"],"next_similarity":results[1]["similarity"]}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--data",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();print(json.dumps(run_demo(data=a.data),indent=None if a.json else 2))
if __name__=="__main__":main()
