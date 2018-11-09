from typing import List

from PIL import Image

from ui.layout.layout import Layout, Align
from ui.widgets.widget import Widget


class HorizontalLayout(Layout):
    def __init__(self, ctx, mod, w: List[Widget], align: Align=Align.LEFT):
        super().__init__(ctx, mod, w)
        self.align = align

    def draw_widget(self, widget):
        return widget(self.ctx).draw()

    def make_bitmap(self):

        bitmaps = list(map(self.draw_widget, self.widgets))
        widths = map(lambda bm: bm.width, bitmaps)
        heights = map(lambda bm: bm.height, bitmaps)
        total_width = sum(widths)
        height = max(heights)

        gap = 0
        cursor = 0
        if self.align == Align.SPACE_BETWEEN:
            if total_width < self.width and len(self.widgets) > 1:
                gap = (self.width - total_width) // (len(self.widgets) - 1)
        elif self.align == Align.RIGHT:
            cursor = self.width-total_width

        img = Image.new('1', (self.width, height))

        for bitmap in bitmaps:
            box = [
                cursor, 0, cursor + bitmap.width, bitmap.height
            ]
            img.paste(bitmap, box)
            cursor += (bitmap.width + gap)

        return img


