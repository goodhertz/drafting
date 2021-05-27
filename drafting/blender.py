# to be loaded from within Blender

from drafting.geometry import Point, Line, Rect
from drafting.pens.drawbotpen import DrawBotPen
from drafting.pens.draftingpen import DraftingPen
from drafting.pens.draftingpens import DraftingPens
from drafting.pens.blenderpen import BlenderPen, BPH
from drafting.text.reader import StyledString, Style, Font
from drafting.text.composer import StSt
from drafting.color import hsl, bw
from pathlib import Path
try:
    import bpy
except ImportError:
    print("no bpy")
    pass

# def bldraw(p:DraftingPen):
#     p.cast(DrawBotPen).draw()
#     return p

class bl_frame_animation():
    """
    """
    def __init__(self):
        self.func = None
        self.name = None
        self.current_frame = -1
    
    def __call__(self, func):
        def _frame_update_handler(scene):
            if scene.frame_current != self.current_frame:
                self.current_frame = scene.frame_current
                # make a real frame object here
                # to get real easing, etc.

        self.func = func
        if not self.name:
            self.name = self.func.__name__
        return self