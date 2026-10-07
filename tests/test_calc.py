import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).parents[1]))
from cost.calc import estimate
class T(unittest.TestCase):
 def test_math(self): self.assertAlmostEqual(estimate({'input':1e-6,'output':3e-6},2,1),5e-6)
if __name__=="__main__":unittest.main()
