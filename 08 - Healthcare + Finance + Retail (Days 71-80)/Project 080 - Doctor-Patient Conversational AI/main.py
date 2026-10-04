"""Stateful symptom-intake dialogue with red-flag escalation and hand-off summary."""
import argparse,json,os
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=80,"Doctor-Patient Conversational Assistant","Edward Ocran"
class Intake:
 def __init__(self):self.turns=[];self.duration=None;self.symptoms=[];self.red_flags=[]
 def respond(self,text):
  self.turns.append(("patient",text));low=text.lower();self.red_flags += [x for x in ("chest pain","shortness of breath","fainting") if x in low and x not in self.red_flags]
  for x in ("fever","sore throat","cough","headache"):
   if x in low and x not in self.symptoms:self.symptoms.append(x)
  if self.red_flags:reply="These symptoms need urgent in-person assessment now."
  elif self.duration is None:reply="How long have these symptoms been present?"
  else:reply="Have they worsened, and are you able to drink fluids normally?"
  self.turns.append(("assistant",reply));return reply
 def summary(self):return {"symptoms":self.symptoms,"red_flags":self.red_flags,"turns":len(self.turns),"handoff":f"Patient reports {', '.join(self.symptoms) or 'unspecified symptoms'}."}
def run_demo(fast=None):
 s=Intake();s.respond("I have had a sore throat, fever and dry cough");s.duration="3 days";s.respond("It has been three days and is not getting worse");summary=s.summary();return {"project":80,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","summary":summary,"metrics":{"patient_turns":2,"symptoms":len(summary["symptoms"]),"red_flags":len(summary["red_flags"])},"disclaimer":"Intake support only; not medical advice."}
def main():
 p=argparse.ArgumentParser();p.add_argument("--json",action="store_true");a=p.parse_args();print(json.dumps(run_demo(),indent=None if a.json else 2))
if __name__=="__main__":main()
