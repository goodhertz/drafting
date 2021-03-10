from random import random
from drafting.drawbot import *
from drafting.text.reader import StyledString, Style, Font

mistral = Font.Cacheable("~/Type/fonts/fonts/_script/MistralD.otf")

save = "test/drawbot/hello.pdf"

with new_drawing("letter", save_to=save) as (idx, r):
    s = (StyledString("Hello", Style(mistral, 300))
        .pens()
        .f(hsl(random(), s=1))
        .align(r))
    
    print(s.attrs)

    db.fill(*hsl(random(), l=0.3))
    db.rect(*s.ambit())
    s.chain(dbdraw)