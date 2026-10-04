"""Run selected project entry points without the CI fast-validation flag."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def project_number(path: Path) -> int:
    match = re.match(r"Project (\d{3}) - ", path.parent.name)
    if not match:
        raise ValueError(f"Cannot read project number from {path.parent.name}")
    return int(match.group(1))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run full project entry points for a selected range")
    parser.add_argument("--from-project", type=int, default=1)
    parser.add_argument("--to-project", type=int, default=100)
    parser.add_argument("--timeout", type=int, default=900, help="seconds allowed per project")
    args = parser.parse_args()
    if not 1 <= args.from_project <= args.to_project <= 100:
        parser.error("project range must stay between 1 and 100")

    root = Path(__file__).resolve().parent
    mains = [path for path in root.glob("*/*/main.py") if args.from_project <= project_number(path) <= args.to_project]
    failures, passed = [], []
    for path in sorted(mains, key=project_number):
        number = project_number(path)
        try:
            completed = subprocess.run(
                [sys.executable, str(path), "--json"],
                capture_output=True,
                text=True,
                timeout=args.timeout,
            )
        except subprocess.TimeoutExpired:
            failures.append({"project": number, "reason": f"timed out after {args.timeout} seconds"})
            continue
        try:
            payload = json.loads(completed.stdout.strip().splitlines()[-1])
        except Exception:
            payload = {}
        if completed.returncode or payload.get("status") != "ok":
            failures.append({"project": number, "reason": completed.stderr[-800:] or "invalid JSON result"})
        else:
            passed.append(number)

    report = {
        "validation_level": "full project entry-point validation",
        "range": [args.from_project, args.to_project],
        "projects_found": len(mains),
        "passed": passed,
        "failed": failures,
    }
    print(json.dumps(report, indent=2))
    return 1 if failures or len(mains) != args.to_project - args.from_project + 1 else 0


if __name__ == "__main__":
    raise SystemExit(main())
