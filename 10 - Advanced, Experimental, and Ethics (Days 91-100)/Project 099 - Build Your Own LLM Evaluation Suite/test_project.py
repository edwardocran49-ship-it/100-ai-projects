import importlib.util,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location("m",Path(__file__).with_name("main.py"));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class T(unittest.TestCase):
 def test_workflow(self):
  r=m.run_demo(True);self.assertGreaterEqual(r["metrics"]["mean_score"],.9);self.assertEqual(r["metrics"]["safety"],1.0);self.assertTrue((Path(__file__).with_name("evaluation_results.csv")).exists())
if __name__=="__main__":unittest.main()
