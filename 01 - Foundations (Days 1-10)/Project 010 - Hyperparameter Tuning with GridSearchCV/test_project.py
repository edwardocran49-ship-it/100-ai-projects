import unittest

import main


class ProjectTest(unittest.TestCase):
    def test_dataset_pipeline(self):
        result = main.run_demo()
        self.assertEqual(result["project"], 10)
        self.assertEqual(result["status"], "ok")
        self.assertGreater(result["records"], 50)
        self.assertTrue(result["dataset"])
        self.assertTrue(result["metrics"])


if __name__ == "__main__":
    unittest.main()
