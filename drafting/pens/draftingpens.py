from drafting.sh import sh
from drafting.geometry import Geometrical
from drafting.pens.draftingpen import DraftingPen


class DraftingPens(DraftingPen):
    def __init__(self, pens):
        super().__init__()
        self._in_progress_pen = None
        self.pens = []
        for p in pens:
            self.append(p)
    
    def print_tree(self, depth=0):
        """Print a hierarchical representation of the pen set"""
        print(" |"*depth, self)
        for pen in self.pens:
            if hasattr(pen, "pens"):
                #print("  "*depth, pen)
                pen.print_tree(depth=depth+1)
                #print("  "*depth, "/"+str(pen))
            else:
                print(" |"*(depth+1), pen)
        #print("  "*depth + "/"+str(self))
        return self
    
    def __repr__(self):
        v = "" if self.visible else "ø-"
        return f"<{v}DraftingPens:{len(self.pens)})>"
    
    def __len__(self):
        return len(self.pens)
    
    def __getitem__(self, index):
        return self.pens[index]
        
    def __setitem__(self, index, pen):
        self.pens[index] = pen
    
    def __iadd__(self, item):
        return self.append(item)
    
    def __add__(self, item):
        return self.append(item)
    
    def append(self, pen):
        if isinstance(pen, Geometrical):
            return self.pens.append(DATPen(pen))
        elif isinstance(pen, DraftingPen):
            self.pens.append(pen)
        else:
            try:
                for p in pen:
                    if p:
                        self.pens.append(p)
            except TypeError:
                self.pens.append(pen)
        return self
    
    # RecordingPen contract

    def moveTo(self, p0):
        self._in_progress_pen = DraftingPen()
        self._in_progress_pen.moveTo(p0)
        return self
    
    def lineTo(self, p1):
        self._in_progress_pen.lineTo(p1)
        return self
    
    def qCurveTo(self, *points):
        self._in_progress_pen.qCurveTo(*points)
        return self
    
    def curveTo(self, *points):
        self._in_progress_pen.curveTo(*points)
        return self
    
    def closePath(self):
        self._in_progress_pen.closePath()
        self.append(self._in_progress_pen)
        self._in_progress_pen = None
        return self
    
    def endPath(self):
        self._in_progress_pen.endPath()
        self.append(self._in_progress_pen)
        self._in_progress_pen = None
        return self
    
    def replay(self, pen):
        self.pen().replay(pen)
    
    def sh(self, s):
        res = sh(s, self)
        if res[0] == "∫":
            res = [DraftingPen().sh(res[1:])]
        return res
    
    def pen(self):
        """A flat representation of this set as a single pen"""
        dp = DraftingPen()
        fps = self.collapse()
        for p in fps.pens:
            dp.record(p)
        if len(fps.pens) > 0:
            for k, attrs in fps.pens[0].attrs.items():
                dp.attr(tag=k, **attrs)
        dp.frame(self.frame())
        return dp
    
    def collapse(self, levels=100, onself=False):
        """AKA `flatten` in some programming contexts, though
        `flatten` is a totally different function here that flattens
        outlines; this function flattens nested collections into
        one-dimensional collections"""
        pens = []
        for idx, p in enumerate(self.pens):
            if hasattr(p, "pens") and levels > 0:
                pens.extend(p.collapse(levels=levels-1).pens)
            else:
                pens.append(p)
        dps = DraftingPens(pens)
        if onself:
            self.pens = dps.pens
            return self
        else:
            return dps