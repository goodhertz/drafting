from fontTools.pens.recordingPen import RecordingPen
from drafting.geometry import Geometrical, Atom, Point, Line, Rect
from drafting.sh import sh, SHContext


class DraftingPen(RecordingPen, SHContext):
    """Fluent subclass of RecordingPen"""

    def __init__(self, *args):
		self.value = []
        self._tag = None
        self._frame = None

        for idx, arg in enumerate(args):
            if isinstance(arg, str):
                self.tag(arg)
            elif isinstance(arg, DATPen):
                self.replace_with(arg)
            elif isinstance(arg, Rect):
                self.rect(arg)
            elif isinstance(arg, Line):
                self.line(arg)
            elif isinstance(arg, Point):
                self.oval(Rect.FromCenter(arg, 50, 50))
    
    def __repr__(self):
        s = f"DraftingPen<"
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
    
    def define(self, *args, **kwargs):
        return self.context_record("$", "defs", *args, **kwargs)
    
    def sh(self, s, fn=None, tag=None):
        if isinstance(s, str):
            e = sh(s, self)
        else:
            e = s

        self.moveTo(e[0])
        for _e in e[1:]:
            if _e is None:
                continue
            elif isinstance(_e, Point):
                self.lineTo(_e)
            elif isinstance(_e, str):
                getattr(self, _e)()
            elif len(_e) == 3:
                self.boxCurveTo(_e[-1], _e[0], _e[1])
        
        if self.is_unended():
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
		super().closesPath()
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
    
    def rect(self, rect, *args):
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