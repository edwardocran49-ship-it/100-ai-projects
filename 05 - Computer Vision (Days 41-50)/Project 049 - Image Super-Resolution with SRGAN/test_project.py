from __future__ import annotations

import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from main import PROJECT_NUMBER, PROJECT_TITLE, run_demo


class ProjectBehaviorTest(unittest.TestCase):
    def test_pdf_aligned_behavior(self):
        result = run_demo(fast=True)
        self.assertEqual(result["project"], PROJECT_NUMBER)
        self.assertEqual(result["title"], PROJECT_TITLE)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["metrics"]["scale_factor"], 4)
        self.assertEqual(result["metrics"]["output_width"], 64)


if __name__ == "__main__":
    unittest.main()
