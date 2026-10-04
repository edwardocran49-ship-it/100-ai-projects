from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    mains = sorted(root.glob("*/*/main.py"))
    failures = []
    timeout_seconds = int(os.environ.get("PROJECT_TIMEOUT_SECONDS", "300"))
    for main_file in mains:
        try:
            completed = subprocess.run(
                [sys.executable, str(main_file), "--json"],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env={**os.environ, "PORTFOLIO_FAST_VALIDATION": "1"},
            )
        except subprocess.TimeoutExpired as exc:
            failures.append(
                {
                    "project": str(main_file.parent),
                    "stderr": f"Timed out after {timeout_seconds} seconds: {exc}",
                }
            )
            continue
        try:
            # Download libraries may emit progress notices before the program's
            # machine-readable result. Each project prints its JSON result last.
            payload = json.loads(completed.stdout.strip().splitlines()[-1])
        except Exception:
            payload = {}
        if completed.returncode or payload.get("status") != "ok":
            failures.append({"project": str(main_file.parent), "stderr": completed.stderr[-500:]})
    report = {"projects_found": len(mains), "passed": len(mains) - len(failures), "failed": failures}
    (root / "validation-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if failures or len(mains) != 100 else 0


if __name__ == "__main__":
    raise SystemExit(main())
