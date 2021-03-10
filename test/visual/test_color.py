from coldtype import *
from drafting.geometry import Rect
from drafting.color import hsl

@renderable((500, 500))
def t1(r):
    return (DP(r).f(hsl(0.3)))
