from typing import List

from ui.drawable import Drawable
from ui.widgets.widget import Widget


class Layout(Drawable):
    def __init__(self, ctx, mod, w: List[Widget]):
        super().__init__(ctx, mod)
        size = ctx['size']
        fnt = ctx['fnt']
        self.width, self.height = size
        self.widgets = w

    def make_bitmap(self):
        pass


class Align:
    LEFT = 'left'
    RIGHT = 'right'
    SPACE_BETWEEN = 'space-between'
