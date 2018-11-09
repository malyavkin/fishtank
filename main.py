from font import MyFont
from render import canvas, DummyCanvas
from ui.ui import UI
from ui.view import TitleView
from ui.input_agent import Console
import asyncio

try:
    from device import ssd1306

    display = ssd1306(port=1, address=0x3C)
    draw_target = canvas(display)
except Exception as x:
    print(x)
    draw_target = DummyCanvas((128, 64))


def handler(loop, context):
    print(context)


fnt = MyFont('./assets/1bit.png', './assets/1bit.descriptor.json')
ui_mgr = UI(draw_target)
ui_mgr.push_view(TitleView(fnt=fnt, UI=ui_mgr, title='Привет, мир!'))
console_mgr = Console()
loop = asyncio.get_event_loop()
loop.set_exception_handler(handler)
loop.set_debug(True)
loop.run_until_complete(asyncio.wait([
    ui_mgr.run(console_mgr),
    console_mgr.run(ui_mgr)
]))
