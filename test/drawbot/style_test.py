import sys, os
from pathlib import Path

sys.path.insert(0, str(Path("~/Goodhertz/drafting").expanduser()))

from drafting.drawbot import *
from drafting.text.reader import StyledString, Style, Font

r = page_rect()

mistral = Font.Cacheable("~/Type/fonts/fonts/_script/MistralD.otf")

s = (StyledString("Hello",
    Style(mistral, 300))
    .pen()
    .f(hsl(0.9, s=1))
    .align(r))

db.rect(*s.ambit())
s.chain(dbdraw)

db.fontSize(24)
db.text("Mistral", s.ambit().inset(0, -50).ps, align="center")