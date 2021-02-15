import unittest
from drafting.geometry import Rect
from drafting.pens.draftingpen import DraftingPen


class TestDraftingPens(unittest.TestCase):
    def test_test(self):
        r = Rect(0, 0, 100, 100)
        dp = DraftingPen().sh(f"{r}")
        print(dp.value)

if __name__ == "__main__":
    unittest.main()