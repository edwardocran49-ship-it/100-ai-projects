"""Educational symptom matching with explicit emergency triage rules."""
import argparse,json,os,re
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=71,"Medical Diagnosis Support Tool","Edward Ocran"
KB={"influenza-like illness":{"fever","cough","fatigue","aches"},"migraine pattern":{"headache","nausea","light sensitivity"},"gastroenteritis pattern":{"abdominal pain","diarrhea","nausea"},"arthritis pattern":{"joint pain","stiffness","swelling"}}
RED=("chest pain","shortness of breath","one-sided weakness","severe bleeding","confusion")
def assess(text):
 lower=text.lower();alerts=[x for x in RED if x in lower];scores=[]
 for name,terms in KB.items():
  matched=[x for x in terms if x in lower];scores.append((name,len(matched)/len(terms),matched))
 scores.sort(key=lambda x:x[1],reverse=True);return {"triage":"emergency evaluation" if alerts else "routine clinical review","alerts":alerts,"matches":[{"pattern":n,"score":round(s,3),"matched":m} for n,s,m in scores[:3]]}
def run_demo(fast=None):
 r=assess("Fever, cough, fatigue and body aches for two days")
 return {"project":71,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok",**r,"metrics":{"patterns":len(KB),"top_score":r["matches"][0]["score"],"red_flags":len(r["alerts"])},"disclaimer":"Educational support only; not a diagnosis."}
def main():
 p=argparse.ArgumentParser();p.add_argument("symptoms",nargs="?",default="Fever, cough, fatigue and body aches for two days");p.add_argument("--json",action="store_true");a=p.parse_args();r={"project":71,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok",**assess(a.symptoms)};print(json.dumps(r,indent=None if a.json else 2))
if __name__=="__main__":main()
