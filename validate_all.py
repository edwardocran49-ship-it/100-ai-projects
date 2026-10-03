from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    mains = sorted(root.glob("*/*/main.py"))
    failures = []
    for main_file in mains:
        completed = subprocess.run(
            [sys.executable, str(main_file), "--json"], capture_output=True, text=True, timeout=30
        )
        try:
            payload = json.loads(completed.stdout.strip())
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
