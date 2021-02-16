import math
from typing import Callable

from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.reverseContourPen import ReverseContourPen

from drafting.geometry import Atom, Point, Line, Rect, align
from drafting.sh import sh, SHContext


class DraftingPen(RecordingPen, SHContext):
    """Fluent subclass of RecordingPen"""

    def __init__(self, *args):
        SHContext.__init__(self)
        RecordingPen.__init__(self)

        self._tag = None
        self._frame = None
        self._visible = True
        self._parent = None

        self.defs = None

        for _, arg in enumerate(args):
            if isinstance(arg, str):
                self.tag(arg)
            elif isinstance(arg, DraftingPen):
                self.replace_with(arg)
            elif isinstance(arg, Rect):
                self.rect(arg)
            elif isinstance(arg, Line):
                self.line(arg)
            elif isinstance(arg, Point):
                self.oval(Rect.FromCenter(arg, 50, 50))
    
    def __repr__(self):
        s = f"{type(self).__name__}<"
        if self._tag:
            s += self._tag + ":"
        s += f"{len(self.value)}mvs:"
        if self.value[-1][0] == "closePath":
            s += "closed"
        elif self.value[-1][0] == "endPath":
            s += "end"
        else:
            s += "open"
        s += "/>"
        return s
    
    def tag(self, value=None):
        if value:
            if isinstance(value, str):
                self._tag = value
            return self
        else:
            return self._tag
        
    def frame(self, value=None):
        if value:
            if isinstance(value, Rect):
                self._frame = value
            return self
        else:
            return self._frame
    
    def visible(self, value=None):
        if value:
            self._visible = value
            return self
        else:
            return self._visible
        
    def bounds(self):
        """Calculate the bounds of this shape; mostly for internal use."""
        try:
            cbp = BoundsPen(None)
            self.replay(cbp)
            mnx, mny, mxx, mxy = cbp.bounds
            return Rect((mnx, mny, mxx - mnx, mxy - mny))
        except:
            return Rect(0, 0, 0, 0)
    
    def ambit(self, th=False, tv=False):
        """Get the calculated rect boundary of the DraftingPen;
        `th` means `(t)rue (h)orizontal`;
        `ty` means `(t)rue (v)ertical`;
        passing either ignores a non-bounds-derived frame
        in either dimension"""
        if self._frame:
            if (th or tv) and len(self.value) > 0:
                f = self._frame
                b = self.bounds()
                if th and tv:
                    return b
                elif th:
                    return Rect(b.x, f.y, b.w, f.h)
                else:
                    return Rect(f.x, b.y, f.w, b.h)
            else:
                return self._frame
        else:
            return self.bounds()
    
    def define(self, *args, **kwargs):
        return self.context_record("$", "defs", None, *args, **kwargs)
    
    def print(self, *args):
        for a in args:
            if callable(a):
                print(a(self))
            else:
                print(a)
        return self
    
    def unended(self):
        if len(self.value) == 0:
            return True
        elif self.value[-1][0] not in ["endPath", "closePath"]:
            return True
        return False
    
    def reverse(self):
        """Reverse the winding direction of the pen."""
        if self.unended():
            self.closePath()
        dp = type(self)()
        rp = ReverseContourPen(dp)
        self.replay(rp)
        self.value = dp.value
        return self
    
    def __invert__(self):
        return self.reverse()
    
    def sh(self, s, fn=None, tag=None):
        if isinstance(s, str):
            e = sh(s, self)
        else:
            e = s
        
        def one_move(_e, move="lineTo"):
            if _e is None:
                return
            elif isinstance(_e, Point):
                getattr(self, move)(_e)
            elif isinstance(_e, Rect):
                self.rect(_e)
            elif isinstance(_e, str):
                getattr(self, _e)()
            elif len(_e) == 3:
                self.boxCurveTo(_e[-1], _e[0], _e[1])

        one_move(e[0], move="moveTo")

        for _e in e[1:]:
            one_move(_e, move="lineTo")
        
        if self.unended():
            self.closePath()

        if tag:
            self.tag(tag)
        if fn:
            fn(self)
        return self

    def moveTo(self, p0):
        super().moveTo(p0)
        return self

    def lineTo(self, p1):
        super().lineTo(p1)
        return self

    def qCurveTo(self, *points):
        super().qCurveTo(*points)
        return self

    def curveTo(self, *points):
        super().curveTo(*points)
        return self

    def closePath(self):
        super().closePath()
        return self

    def endPath(self):
        super().endPath()
        return self

    def addComponent(self, glyphName, transformation):
        super().addComponent(glyphName, transformation)
        return self

    def replay(self, pen):
        super().replay(pen)
        return self
    
    def rect(self, rect):
        """Rectangle primitive — `moveTo/lineTo/lineTo/lineTo/closePath`"""
        self.moveTo(rect.point("SW").xy())
        self.lineTo(rect.point("SE").xy())
        self.lineTo(rect.point("NE").xy())
        self.lineTo(rect.point("NW").xy())
        self.closePath()
        return self
    
    def roundedRect(self, rect, hr, vr=None):
        """Rounded rectangle primitive"""
        if vr is None:
            vr = hr
        l, b, w, h = Rect(rect)
        r, t = l + w, b + h
        K = 4 * (math.sqrt(2)-1) / 3
        circle = hr == 0.5 and vr == 0.5
        if hr <= 0.5:
            hr = w * hr
        if vr <= 0.5:
            vr = h * vr
        self.moveTo((l + hr, b))
        if not circle:
            self.lineTo((r - hr, b))
        self.curveTo((r+hr*(K-1), b), (r, b+vr*(1-K)), (r, b+vr))
        if not circle:
            self.lineTo((r, t-vr))
        self.curveTo((r, t-vr*(1-K)), (r-hr*(1-K), t), (r-hr, t))
        if not circle:
            self.lineTo((l+hr, t))
        self.curveTo((l+hr*(1-K), t), (l, t-vr*(1-K)), (l, t-vr))
        if not circle:
            self.lineTo((l, b+vr))
        self.curveTo((l, b+vr*(1-K)), (l+hr*(1-K), b), (l+hr, b))
        self.closePath()
        return self
    
    def oval(self, rect):
        """Oval primitive"""
        self.roundedRect(rect, 0.5, 0.5)
        return self

    def line(self, points, moveTo=True, endPath=True):
        """Syntactic sugar for `moveTo`+`lineTo`(...)+`endPath`; can have any number of points"""
        if isinstance(points, Line):
            points = list(points)
        if len(points) == 0:
            return self
        if len(self.value) == 0 or moveTo:
            self.moveTo(points[0])
        else:
            self.lineTo(points[0])
        for p in points[1:]:
            self.lineTo(p)
        if endPath:
            self.endPath()
        return self
    
    def boxCurveTo(self, pt, point, factor, mods={}):
        a = Point(self.value[-1][-1][-1])
        d = Point(pt)
        box = Rect.FromMnMnMxMx([min(a.x, d.x), min(a.y, d.y), max(a.x, d.x), max(a.y, d.y)])
        try:
            f1, f2 = factor
        except TypeError:
            if isinstance(factor, Atom):
                f1, f2 = (factor[0], factor[0])
            else:
                f1, f2 = (factor, factor)

        if isinstance(point, str):
            p = box.point(point)
            p1, p2 = (p, p)
        elif isinstance(point, Point):
            p1, p2 = point, point
        else:
            p1, p2 = point
            p1 = box.point(p1)
            p2 = box.point(p2)
        
        b = a.interp(f1, p1)
        c = d.interp(f2, p2)

        mb = mods.get("b")
        mc = mods.get("c")
        if mb:
            b = mb(b)
        elif mc:
            c = mc(c)
        
        self.curveTo(b, c, d)
        return self
    
    def vl(self, value):
        self.value = value
        return self
    
    def replace_with(self, other):
        return self.vl(other.value)
    
    def pvl(self):
        for idx, (_, pts) in enumerate(self.value):
            if len(pts) > 0:
                self.value[idx] = list(self.value[idx])
                self.value[idx][-1] = [Point(p) for p in self.value[idx][-1]]
        return self
    
    def copy(self, with_data=False):
        dp = type(self)(self)
        if with_data:
            dp._frame = self._frame
            dp.defs = self.defs # necessary to copy this and not pass by ref?
        else:
            dp.defs = self.defs
        return dp
    
    def round(self):
        """Round the values of this pen to integer values."""
        return self.round_to(1)

    def round_to(self, rounding):
        """Round the values of this pen to nearest multiple of rounding."""
        def rt(v, mult):
            rndd = float(round(v / mult) * mult)
            if rndd.is_integer():
                return int(rndd)
            else:
                return rndd
        
        rounded = []
        for t, pts in self.value:
            _rounded = []
            for p in pts:
                if p:
                    x, y = p
                    _rounded.append((rt(x, rounding), rt(y, rounding)))
                else:
                    _rounded.append(p)
            rounded.append((t, _rounded))
        
        self.value = rounded
        return self

    def transform(self, transform, transformFrame=True):
        """Perform an arbitrary transformation on the pen, using the fontTools `Transform` class."""
        op = RecordingPen()
        tp = TransformPen(op, transform)
        self.replay(tp)
        self.value = op.value
        if transformFrame and self._frame:
            self._frame = self._frame.transform(transform)
        return self
    
    def align(self, rect, x="mdx", y="mdy", th=True, tv=False, transformFrame=True):
        r = self.ambit(th, tv)
        self.translate(*align(r, rect, x, y))
        return self
    
    def translate(self, x, y=None, transformFrame=True):
        """Translate this shape by `x` and `y` (pixel values)."""
        if y is None:
            y = x
        return self.transform(Transform(1, 0, 0, 1, x, y), transformFrame=transformFrame)
    
    def skew(self, x=0, y=0, point=None):
        t = Transform()
        if not point:
            point = self.bounds().point("C") # maybe should be getFrame()?
        t = t.translate(point.x, point.y)
        t = t.skew(x, y)
        t = t.translate(-point.x, -point.y)
        return self.transform(t)
    
    def rotate(self, degrees, point=None):
        """Rotate this shape by a degree (in 360-scale, counterclockwise)."""
        t = Transform()
        if not point:
            point = self.bounds().point("C") # maybe should be getFrame()?
        elif isinstance(point, str):
            point = self.bounds().point(point)
        t = t.translate(point.x, point.y)
        t = t.rotate(math.radians(degrees))
        t = t.translate(-point.x, -point.y)
        return self.transform(t, transformFrame=False)
    
    def scale(self, scaleX, scaleY=None, point=None):
        """Scale this shape by a percentage amount (1-scale)."""
        t = Transform()
        if point != False:
            point = self.bounds().point("C") if point == None else point # maybe should be getFrame()?
            t = t.translate(point.x, point.y)
        t = t.scale(scaleX, scaleY or scaleX)
        if point != False:
            t = t.translate(-point.x, -point.y)
        return self.transform(t)
    
    def scaleToRect(self, rect, preserveAspect=True, shrink_only=False):
        """Scale this shape into a `Rect`."""
        bounds = self.bounds()
        h = rect.w / bounds.w
        v = rect.h / bounds.h
        if preserveAspect:
            scale = h if h < v else v
            if shrink_only and scale >= 1:
                return self
            return self.scale(scale)
        else:
            if shrink_only and (h >= 1 or v >= 1):
                return self
            return self.scale(h, v)
    
    def scaleToWidth(self, w, shrink_only=False):
        """Scale this shape horizontally"""
        b = self.bounds()
        if shrink_only and b.w < w:
            return self
        else:
            return self.scale(w / self.bounds().w, 1)
    
    def scaleToHeight(self, h, shrink_only=False):
        """Scale this shape horizontally"""
        b = self.bounds()
        if shrink_only and b.h < h:
            return self
        return self.scale(1, h / self.bounds().h)
    
    def walk(self, callback:Callable[["DraftingPen", int, dict], None], depth=0, visible_only=False, parent=None):
        if visible_only and not self._visible:
            return
        
        if parent:
            self._parent = parent
        
        is_dps = hasattr(self, "pens")
        if is_dps:
            callback(self, -1, dict(depth=depth))
            for pen in self.pens:
                pen.walk(callback, depth=depth+1, visible_only=visible_only, parent=self)
            callback(self, 1, dict(depth=depth))
        else:
            callback(self, 0, dict(depth=depth))
    
    def remove_blanks(self):
        """If this is blank, `return True` (for recursive calls from DATPens)."""
        return len(self.value) == 0
    
    # GEOMETRICAL

    def nsew(self):
        pts = [el[1][-1] for el in self.value if len(el[1]) > 0]
        
        lines = []
        for i, p in enumerate(pts):
            if i + 1 == len(pts):
                lines.append(Line(p, pts[0]))
            else:
                lines.append(Line(p, pts[i+1]))
        
        mnx, mny, mxx, mxy = self.bounds().mnmnmxmx()
        min_ang = min([l.ang for l in lines])
        max_ang = max([l.ang for l in lines])
        #for idx, l in enumerate(lines):
        #    print(idx, ">", l.ang, min_ang, max_ang)
        xs = [l for l in lines if math.isclose(l.ang,min_ang)]
        ys = [l for l in lines if math.isclose(l.ang, max_ang)]

        #print(len(xs), len(ys))
        #print("--------------------")

        n = [l for l in xs if l.start.y == mxy or l.end.y == mxy][0]
        s = [l for l in xs if l.start.y == mny or l.end.y == mny][0]
        e = [l for l in ys if l.start.x == mxx or l.end.x == mxx][0]
        w = [l for l in ys if l.start.x == mnx or l.end.x == mnx][0]
        return n, s, e, w

    def point(self, pt):
        n, s, e, w = self.nsew()
        if pt == "NE":
            return n.pe
        elif pt == "NW":
            return n.pw
        elif pt == "SE":
            return s.pe
        elif pt == "SW":
            return s.pw
        elif pt == "N":
            return n.mid
        elif pt == "S":
            return s.mid
        elif pt == "E":
            return e.mid
        elif pt == "W":
            return w.mid

    @property
    def pne(self): return self.point("NE")
    @property
    def pnw(self): return self.point("NW")
    @property
    def psw(self): return self.point("SW")
    @property
    def pse(self): return self.point("SE")
    @property
    def pn(self): return self.point("N")
    @property
    def ps(self): return self.point("S")
    @property
    def pe(self): return self.point("E")
    @property
    def pw(self): return self.point("W")
    @property
    def en(self): return self.nsew()[0]
    @property
    def es(self): return self.nsew()[1]
    @property
    def ee(self): return self.nsew()[2]
    @property
    def ew(self): return self.nsew()[3]
    
    @property
    def ecx(self):
        n, s, e, w = self.nsew()
        return e.interp(0.5, w.reverse())
    
    @property
    def ecy(self):
        n, s, e, w = self.nsew()
        return n.interp(0.5, s.reverse())