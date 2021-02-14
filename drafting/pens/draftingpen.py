from fontTools.pens.recordingPen import RecordingPen
from drafting.geometry import Geometrical, Atom, Point, Line, Rect


class DraftingPen(RecordingPen):
    """Fluent subclass of RecordingPen"""

    def __init__(self, *args):
		self.value = []
        self._tag = None

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
    
    def tag(self, value=None):
        if value:
            self._tag = value
            return self
        else:
            return self._tag

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
