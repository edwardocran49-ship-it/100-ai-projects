import unittest
import main
class TestProject(unittest.TestCase):
    def test_pipeline(self):
        result=main.run_demo(); self.assertEqual(result['project'],24); self.assertEqual(result['status'],'ok'); self.assertGreater(result['records'],50); self.assertTrue(result['metrics'])
if __name__=='__main__': unittest.main()
