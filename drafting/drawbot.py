import contextlib
import drawBot as db
from drafting.geometry import Point, Line, Rect
from drafting.pens.drawbotpen import DrawBotPen
from drafting.pens.draftingpen import DraftingPen
from drafting.pens.draftingpens import DraftingPens
from drafting.text.reader import StyledString, Style, Font
from drafting.text.composer import StSt
from drafting.color import hsl, bw
from pathlib import Path

def dbdraw(p:DraftingPen):
    p.cast(DrawBotPen).draw()
    return p

def tobp(p:DraftingPen):
    bp = db.BezierPath()
    p.replay(bp)
    return bp

def dbdraw_with_filters(rect:Rect, filters):
    def _draw_call(p:DraftingPen):
        p.cast(DrawBotPen).draw_with_filters(rect, filters)
        return p
    return _draw_call

def page_rect() -> Rect:
    return Rect(db.width(), db.height())

@contextlib.contextmanager
def new_page(r:Rect=Rect(1000, 1000)):
    _r = Rect(r)
    db.newPage(*_r.wh())
    yield _r

@contextlib.contextmanager
def new_drawing(rect:Rect=Rect(1000, 1000), count=1, save_to=None):
    db.newDrawing()
    for idx in range(0, count):
        with new_page(rect) as r:
            yield idx, r
    if save_to:
        db.saveImage(str(save_to))
    db.endDrawing()

def releaser(fn, path, frame_class=None):
    db.newDrawing()
    r = fn.rect
    w, h = r.wh()
    for idx in range(0, fn.duration):
        print(f"Saving page {idx}...")
        db.newPage(w, h)
        if frame_class:
            fn.func(frame_class(idx, fn))
        else:
            fn.func(r)
    pdf_path = Path(path)
    pdf_path.parent.mkdir(exist_ok=True)
    db.saveImage(str(pdf_path))
    print("Saved pdf", str(pdf_path))
    db.endDrawing()