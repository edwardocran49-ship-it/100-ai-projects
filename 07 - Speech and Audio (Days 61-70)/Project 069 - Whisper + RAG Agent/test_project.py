import importlib.util,os,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("project_main",Path(__file__).with_name("main.py"));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class ProjectTest(unittest.TestCase):
    def test_workflow(self):
        result=module.run_demo(fast=True)
        self.assertEqual(result["status"],"ok")
        self.assertEqual(result["author"],"Edward Ocran")
        self.assertTrue(result.get("metrics") or result.get("reference"))
if __name__=="__main__":unittest.main()
