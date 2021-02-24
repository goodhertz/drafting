from coldtype import *
from drafting.pens.draftingpens import DraftingPen, DraftingPens

def flr(ln, amt=50, crv=65, mid="50"):
    mid = float(mid)/100
    if "~" in ln:
        amt = -int(amt)
    a, b, c = norm(0.5, 0, mid), mid, norm(0.5, mid, 1)
    return f"""({ln})∏{a},-{amt}|{crv}|({ln})∏{b},-{amt} ({ln})∏{c},-{amt}|{crv}|({ln})⍵"""

@renderable()
def test_bowing(r):
    return ((ß:=DPS())
        .define(
            r=r.inset(400, 100),
            d="$r↗⨝$r↙")
        .macro(
            flr=flr,
            flrmn=lambda ln: flr(ln, amt=-30, crv=65))
        #.gs("$d⍺ $dP0.25,-$pr|65|$dP0.5,-$pr $dP0.75,-$pr|65|$d⍵ ɜ")
        .gs("$d⍺ @flr:$d ɜ")
        .gs("$d⍵ @flr:$d~ ɜ")
        .f(None).s(0).sw(4)
        .append(ß.all_guides())
        #.pen().skeleton()
        )
    
@renderable()
def test_trapezoid(r):
    return ((ß:=DPS())
        .define(
            r=r.inset(400, 100))
        #.gss("$r")
        #.ap(DP(ß.defs.r).en.offset(0, -20).inset(20))
        .ap(DP(ß.defs.r).pinch("⊤", 50).ee)
        .f(None).s(0).sw(4))

@renderable(solo=1)
def test_last_pt(r):
    return ((ß:=DPS())
        .define(r=r.inset(400, 100))
        .macro(flr=flr)
        .gs("$r↗ @flr:¬⨝$r↙ ɜ")
        .f(None).s(0).sw(4)
        .pen().skeleton())