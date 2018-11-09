from typing import List

from PIL import Image

from ui.layout.layout import Layout
from ui.widgets.widget import Widget


class VerticalLayout(Layout):
    def __init__(self, ctx, mod, w: List[Widget]):
        super().__init__(ctx, mod, w)

    def draw_widget(self, widget):
        return widget(self.ctx).draw()

    def make_bitmap(self):

        bitmaps = list(map(self.draw_widget, self.widgets))
        heights = map(lambda bm: bm.height, bitmaps)
        total_height = sum(heights)

        img = Image.new('1', (self.width, total_height))
        cursor = 0
        for bitmap in bitmaps:
            box = [
                0, cursor, bitmap.width, bitmap.height + cursor
            ]
            img.paste(bitmap, box)
            cursor += bitmap.height

        return img


