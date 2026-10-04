"""Route natural-language requests to weather, news, or calculator tools."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from portfolio_core.agents import route_query,dispatch_tool
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=58,"API Router with LLM","Edward Ocran"


def run_demo():
    queries=["What's the weather like in Tokyo?","Give me news about space exploration.","What's 27 / 3 + 6?"]
    expected=["get_weather","get_news","calculate"]
    routed=[{"query":query,"route":route_query(query)} for query in queries]
    for item in routed: item["response"]=dispatch_tool(item["route"])
    return {"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","routes":routed,
            "metrics":{"queries":len(queries),"correct_routes":sum(item["route"]["tool"]==want for item,want in zip(routed,expected)),"tools_used":len({item["route"]["tool"] for item in routed})}}


def main():
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args(); result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
