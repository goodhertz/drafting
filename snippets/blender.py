# to be run from within blender — could be encapsulated as a coldtype-like pattern?

import importlib

import drafting.blender
importlib.reload(drafting.blender)

from drafting.blender import *

BPH.Clear()

r = Rect(0, 0, 1000, 1000)
tc = BPH.Collection("Text")
fnt = Font.Cacheable("~/Type/fonts/fonts/CheeeVariable.ttf")

(DraftingPen(r)
    .f(hsl(0.9))
    .tag("Frame")
    .cast(BlenderPen)
    .draw(tc, plane=1))

def draw_txt(txt, e):
    (StSt("A", fnt, 800, yest=e)
        .pen()
        .align(r)
        .tag("Yoy")
        .cast(BlenderPen)
        .draw(tc))

current_frame = -1

def my_handler(scene):
    global current_frame
    if scene.frame_current != current_frame:
        current_frame = scene.frame_current
        print("Frame Change POST", current_frame)
        draw_txt(str(current_frame), current_frame/10)

# https://docs.blender.org/api/current/bpy.app.handlers.html

bpy.app.handlers.frame_change_post.clear()
bpy.app.handlers.frame_change_post.append(my_handler)

draw_txt("A", 0)