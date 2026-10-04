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
        self.assertGreater(result["candidates"], 0)
        self.assertEqual(result["readings"][0]["text"], "ABC 1234")


if __name__ == "__main__":
    unittest.main()
