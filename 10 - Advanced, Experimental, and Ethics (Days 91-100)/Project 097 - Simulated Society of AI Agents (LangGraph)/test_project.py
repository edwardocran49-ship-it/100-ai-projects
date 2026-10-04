import importlib.util,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location("m",Path(__file__).with_name("main.py"));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class T(unittest.TestCase):
 def test_workflow(self):
  r=m.run_demo(True);self.assertEqual(r["metrics"]["roles"],4);self.assertEqual(r["metrics"]["messages"],12)
if __name__=="__main__":unittest.main()
