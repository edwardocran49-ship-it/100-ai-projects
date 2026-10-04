import unittest

import main


class ProjectTest(unittest.TestCase):
    def test_real_dataset_pipeline(self) -> None:
        result = main.run_demo()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["dataset"], "Boston Housing")
        self.assertGreaterEqual(result["records"], 500)
        self.assertGreater(result["metrics"]["mae"], 0)
        self.assertLess(result["metrics"]["mae"], 10)


if __name__ == "__main__":
    unittest.main()
