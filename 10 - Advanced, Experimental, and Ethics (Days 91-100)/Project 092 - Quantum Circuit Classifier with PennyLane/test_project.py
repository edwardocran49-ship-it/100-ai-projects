import importlib.util,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location("m",Path(__file__).with_name("main.py"));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class T(unittest.TestCase):
 def test_workflow(self):
  r=m.run_demo(True);self.assertEqual(r["metrics"]["accuracy"],1.0);self.assertLess(r["metrics"]["final_loss"],.1)
if __name__=="__main__":unittest.main()
