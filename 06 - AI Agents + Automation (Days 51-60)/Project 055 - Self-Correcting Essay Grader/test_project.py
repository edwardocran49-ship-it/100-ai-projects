from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from main import PROJECT_NUMBER, PROJECT_TITLE, run_demo


class ProjectSmokeTest(unittest.TestCase):
    def test_demo_completes(self) -> None:
        result = run_demo()
        self.assertEqual(result["project"], PROJECT_NUMBER)
        self.assertEqual(result["title"], PROJECT_TITLE)
        self.assertEqual(result["status"], "ok")
        self.assertIn("metrics", result)
        self.assertGreater(result["metrics"]["score_change"], 0)
        self.assertGreater(result["metrics"]["word_count_change"], 0)


if __name__ == "__main__":
    unittest.main()
