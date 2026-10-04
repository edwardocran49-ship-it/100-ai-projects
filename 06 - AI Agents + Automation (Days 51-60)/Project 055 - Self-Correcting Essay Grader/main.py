"""Grade an essay, rewrite it from the critique, and grade it again."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from portfolio_core.agents import grade_essay,improve_essay
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=55,"Self-Correcting Essay Grader","Edward Ocran"


def run_demo():
    original="I think school is important because you learn stuff and get a job"
    first=grade_essay(original); improved=improve_essay(original); second=grade_essay(improved)
    return {"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","original":original,"improved":improved,"first_evaluation":first,"second_evaluation":second,
            "metrics":{"original_score":first["overall"],"revised_score":second["overall"],"score_change":round(second["overall"]-first["overall"],2),"word_count_change":second["word_count"]-first["word_count"]}}


def main():
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args(); result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
