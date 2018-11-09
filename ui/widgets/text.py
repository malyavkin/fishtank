from PIL import Image, ImageDraw

from ui.widgets.widget import Widget


class TextWidget(Widget):
    def __init__(self, ctx, mod, text='Пусто'):
        super().__init__(ctx, mod)
        self.text = text

    def gettext(self):
        return self.text

    def make_bitmap(self):
        font = self.ctx['fnt']
        image = Image.new('1', (1, 1))
        draw = ImageDraw.Draw(image)
        size = draw.textsize(text=self.gettext(), font=font)
        image = image.resize(size)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), self.gettext(), fill=255, font=font)
        return image
