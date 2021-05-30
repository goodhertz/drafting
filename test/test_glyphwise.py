import unittest
from pathlib import Path
from drafting.grid import Grid
from drafting.geometry import *
from drafting.text.composer import StSt, Glyphwise, Style
from drafting.pens.svgpen import SVGPen

tf = Path(__file__).parent

class TestGlyphwise(unittest.TestCase):
    def _test_glyph_names(self, font_path, kern):
        ss = StSt("AVAMANAV", font_path, 100, wdth=0, kern=kern)
        gw = Glyphwise("AVAMANAV", lambda i, c: Style(font_path, 100, wdth=0, kern=kern))
        gwo = Glyphwise("AVAMANAV", lambda i, c: Style(font_path, 100, wdth=0, kern=(not kern)))

        self.assertEqual(len(ss), 8)
        self.assertEqual(ss[0].glyphName, "A")
        self.assertEqual(ss[-1].glyphName, "V")
        self.assertEqual(len(gw), 8)
        self.assertEqual(ss[0].glyphName, "A")
        self.assertEqual(ss[-1].glyphName, "V")

        self.assertEqual(ss.ambit(), gw.ambit())
        self.assertNotEqual(ss.ambit(), gwo.ambit())

        fp = Path(font_path)
        op = (tf / f"ignorables/__{fp.name}.svg")
        op.parent.mkdir(exist_ok=True)
        op.write_text(SVGPen.Composite(ss, ss.ambit(), viewBox=True))
        return ss, gw

    def test_format_equality(self):
        self._test_glyph_names("~/Type/fonts/fonts/OhnoFatfaceVariable.ttf", True)
        self._test_glyph_names("~/Type/fonts/fonts/OhnoFatfaceVariable.ttf", False)

        # TODO why isn't the ttf version equal to these?
        #self.assertEqual(ufo[0].value, ds[0].value)
        #self.assertEqual(ufo[-1].value, ds[-1].value)

if __name__ == "__main__":
    unittest.main()