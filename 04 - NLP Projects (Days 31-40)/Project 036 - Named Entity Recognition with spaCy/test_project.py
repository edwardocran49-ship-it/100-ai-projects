from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from main import PROJECT_NUMBER, PROJECT_TITLE, run_demo


class ProjectBehaviorTest(unittest.TestCase):
    def test_pdf_aligned_behavior(self) -> None:
        result = run_demo(fast=True)
        self.assertEqual(result["project"], PROJECT_NUMBER)
        self.assertEqual(result["title"], PROJECT_TITLE)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["metrics"]["entities_found"], 4)
        self.assertEqual({item["label"] for item in result["entities"]}, {"PERSON", "ORG", "GPE", "DATE"})
        self.assertEqual(result["model"], "en_core_web_sm")


if __name__ == "__main__":
    unittest.main()
