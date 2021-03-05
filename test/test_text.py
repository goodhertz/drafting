import unittest
from drafting.grid import Grid
from drafting.geometry import *
from drafting.text.reader import StyledString, Style

class TestText(unittest.TestCase):
    
    def test_sh_context(self):
        style = Style("~/Type/fonts/fonts/_script/MistralD.otf")
        ss = StyledString("Hello World", style)
        ssps = ss.pens()
        self.assertEqual(len(ssps), 11)
        print(ssps[0].glyphName)
        #print(ssps.tree())
        #print()

if __name__ == "__main__":
    unittest.main()