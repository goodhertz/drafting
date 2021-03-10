from coldtype import *
from drafting.pens.draftingpens import DraftingPen, DraftingPens

class test(renderable):
    def __init__(self, rect=(800, 300), **kwargs):
        super().__init__(rect=rect, **kwargs)
    
@test(solo=0)
def test_trapezoid(r):
    return ((ß:=DPS())
        .define(r=r.inset(50), p="$r¶π0,50")
        .gs("$p⊣⍺ $p⊣⍵")
        .f(None).s(0).sw(4))

@test(solo=0)
def test_last_pt(r):
    return ((ß:=DPS())
        .define(r=r.inset(50))
        .gs("$r↗ ¬OX-200 ɜ")
        .f(None).s(0).sw(4))