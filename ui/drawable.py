from PIL import ImageDraw
from pydash import py_
from PIL.ImageChops import invert


class Drawable:
    def __init__(self, ctx, mod=None, **kwargs):
        self.ctx = ctx
        self.mod = mod

    def post_process(self, bitmap):
        if self.mod == Mod.NEGATE:
            return invert(bitmap)
        elif self.mod == Mod.UNDERLINE:
            draw = ImageDraw.Draw(bitmap)
            draw.line([0, bitmap.height-1, bitmap.width-1, bitmap.height-1], fill=255, width=1)
            return bitmap

        return bitmap

    def draw(self):
        return self.post_process(self.make_bitmap())

    def make_bitmap(self):
        pass

    @classmethod
    def prep(cls, **kwargs):
        passed_context = {}
        mod = None
        if 'ctx' in kwargs:
            passed_context = kwargs['ctx']
        if 'mod' in kwargs:
            mod = kwargs['mod']
        kwargs = py_.omit(kwargs, ['ctx', 'mod'])

        def factory(ctx):
            merged_context = py_.assign({}, passed_context, ctx)
            try:
                return cls(ctx=merged_context, mod=mod, **kwargs)
            except Exception as x:
                print(x)
        return factory

class Mod:
    UNDERLINE = 'underline'
    NEGATE = 'negate'
