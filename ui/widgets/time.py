from time import time

from ui.widgets.text import TextWidget


class TimeWidget(TextWidget):
    def __init__(self, ctx, mod, **kwargs):
        super().__init__(ctx, mod, **kwargs)

    def gettext(self):
        ts = int(time() + 3 * 3600)
        minutes = (ts // 60) % 60
        hours = (ts // 3600) % 24
        return "{:0>2}{}{:0>2}".format(hours, ":" if int(time()) % 2 else " ", minutes)
