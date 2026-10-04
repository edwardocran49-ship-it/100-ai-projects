"""Select an available business-hour slot and create a calendar event."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from portfolio_core.agents import schedule_event
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=54,"AI Calendar Scheduler Agent","Edward Ocran"


def run_demo():
    calendar={"2026-10-05 10:00":"Team Sync","2026-10-05 14:00":"Sales Demo","2026-10-05 15:00":"Budget Review"}
    result=schedule_event(calendar,"2026-10-05","Project meeting",after_hour=12)
    return {"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","request":"Schedule a project meeting tomorrow afternoon","result":result,
            "metrics":{"occupied_before":3,"available_considered":len(result["available_before_booking"]),"events_after":len(calendar)}}


def main():
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args(); result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
