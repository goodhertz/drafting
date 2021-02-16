import unittest
from drafting.geometry import Rect, Point
from drafting.pens.draftingpen import DraftingPen
from drafting.pens.draftingpens import DraftingPens

class TestDraftingPens(unittest.TestCase):
    def test_test(self):
        r = Rect(0, 0, 100, 100)
        dps = DraftingPens()
        dp = (DraftingPen()
            .define(r=r)
            .sh("$r↖ $r↗ ↘|65|$r↙ ɜ"))
        self.assertEqual(len(dp.value), 4)
        self.assertEqual(dp.value[-2][-1][0], Point(100, 35))
        self.assertEqual(dp.value[-1][0], "endPath")
        self.assertEqual(dp.unended(), False)
        dps.append(DraftingPens([dp]))
        self.assertEqual(len(dps.tree().splitlines()), 3)
        self.assertEqual(dps.tree().splitlines()[-1],
            " | | DraftingPen<4mvs:end/>")
        
    def test_reverse(self):
        dp = (DraftingPen()
            .define(r=Rect(100, 100))
            .sh("$r↖ $r↗ $r↘ ɜ"))
        p1 = dp.value[0][-1]
        p2 = dp.reverse().value[-2][-1]
        self.assertEqual(p1, p2)
    
    def test_transforms(self):
        dp = (DraftingPen(Rect(100, 100))
            .frame(Rect(100, 100))
            .align(Rect(200, 200)))
        
        self.assertEqual(dp.frame().mxx, 150)
        self.assertEqual(dp.value[-2][-1][-1][0], 50)

        self.assertEqual(
            dp.copy().rotate(45).round().value,
            dp.copy().rotate(360+45).round().value)
        
        self.assertEqual(dp.copy().scale(2).ambit().w, 200)

    def test_pens_ambit(self):
        dps = (DraftingPens([
                DraftingPen(Rect(50, 50)),
                DraftingPen(Rect(100, 100, 100, 100))])
                .print(lambda x: x.tree()))
        ram = dps.ambit()
        self.assertEqual(ram, Rect(0, 0, 200, 200))

        moves = []
        dps.walk(lambda p, pos, _: moves.append([p, pos]))
        self.assertEqual(moves[0][0], dps)
        self.assertEqual(moves[0][1], -1)
        self.assertEqual(moves[1][1], 0)

if __name__ == "__main__":
    unittest.main()