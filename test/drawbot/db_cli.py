from drafting.drawbot import *
from drafting.text.reader import StyledString, Style, Font

mistral = Font.Cacheable("~/Type/fonts/fonts/_script/MistralD.otf")

with new_drawing("letter", save_to="test/drawbot/hello.pdf") as (idx, rect):
    s = (StyledString("Hello",
        Style(mistral, 300))
        .pen()
        .f(hsl(0.9, s=1))
        .align(rect)
        .chain(dbdraw))