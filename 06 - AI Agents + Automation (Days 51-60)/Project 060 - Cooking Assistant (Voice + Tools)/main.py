"""Track a recipe through voice-style commands and unit conversions."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from portfolio_core.agents import CookingAssistant
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=60,"Cooking Assistant (Voice + Tools)","Edward Ocran"
RECIPE={"title":"Pancakes","ingredients":["1 cup flour","2 eggs","1 cup milk","1 tsp baking powder"],"steps":["Mix all the dry ingredients in a bowl.","Add eggs and milk. Stir until smooth.","Heat a skillet and pour one quarter cup of batter.","Flip when bubbles form. Cook until golden."]}


def run_demo():
    assistant=CookingAssistant(RECIPE); commands=["start","ingredients","convert","next","next","repeat","back","next"]
    transcript=[{"command":command,"response":assistant.handle(command),"step_after":assistant.current_step} for command in commands]
    return {"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","recipe":RECIPE["title"],"transcript":transcript,
            "metrics":{"commands":len(commands),"steps_completed":assistant.current_step,"conversions":2}}


def main():
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args(); result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
