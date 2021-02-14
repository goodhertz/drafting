from coldtype import *
from drafting.geometry import Rect
from drafting.color import hsl
import colorio

L_A = 64 / math.pi / 5
print(L_A)

cshsl = colorio.cs.HSL()
csok = colorio.cs.OKLAB()
csok.to_rgb1([0.69, 20, L_A])
#c = cshsl.from_rgb1([1, 0, 0])
#print(colorio.cs.OKLAB(c))
#print(colorspace.to_rgb1([0.62, 0.22, 0.125]))
#print(c)

@renderable((500, 500))
def t1(r):
    return (DP(r).f(hsl(0.3)))
