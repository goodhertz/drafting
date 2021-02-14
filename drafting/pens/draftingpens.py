from drafting.sh import SHContext
from drafting.pens.draftingpen import DraftingPen


class DraftingPens(DraftingPen, SHContext):
    def __init__(self, pens):
        self.pens = []
        for p in pens:
            self.append(p)
    
    def append(self, pen):
        