"""Locate price-like OCR results and return boxes with normalized values."""
import argparse,json,os,re
from pathlib import Path
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=78,"Visual Price Tag Detection for Retail","Edward Ocran"
PRICE=re.compile(r"(?:[$€£]\s*)?\d{1,4}[.,]\d{2}")
def filter_prices(results):
 out=[]
 for box,text,confidence in results:
  match=PRICE.search(text.replace(" ",""))
  if match:out.append({"text":match.group().replace(",","."),"confidence":round(float(confidence),3),"box":[[int(v) for v in point] for point in box]})
 return out
def detect(path):
 import easyocr
 return filter_prices([(b,t,c) for b,t,c in easyocr.Reader(["en"]).readtext(str(path))])
def run_demo(fast=None,image=None):
 mock=[([[10,10],[90,10],[90,40],[10,40]],"$3.49",.94),([[100,10],[180,10],[180,40],[100,40]],"7.99",.89),([[0,0],[1,0],[1,1],[0,1]],"SALE",.98)] if os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" or fast else None;found=filter_prices(mock) if mock else detect(image)
 return {"project":78,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","detections":found,"metrics":{"ocr_regions":3 if mock else len(found),"prices_found":len(found),"mean_confidence":round(sum(x["confidence"] for x in found)/max(len(found),1),3)}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--image",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();print(json.dumps(run_demo(image=a.image),indent=None if a.json else 2))
if __name__=="__main__":main()
