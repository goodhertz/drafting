from coldtype import *
from drafting.pens.draftingpens import DraftingPen, DraftingPens

@renderable()
def stub(r):
    return ((ß:=DPS())
        .define(
            r=r.inset(200),
            d="$r↗⨝$r↙",
            pr=130)
        #.define(dr=ß.defs.d.rotate(90))
        .gs("$d⍺ $dP0.25,-$pr|65|$dP0.5,-$pr $dP0.75,-$pr|65|$d⍵ ɜ")
        #.ap(DP(ß.defs.d.project_pt(0.5, -90)))
        #.ap(DP(ß.defs.d.project_pt(0, -90)))
        #.ap(DP(ß.defs.d.rotate(90, point=ß.defs.d.t(0.25))))
        .f(None).s(0).sw(4)
        #.append(ß.all_guides())
        #.pen()
        #.skeleton()
        )
