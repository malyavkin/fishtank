import json

from PIL import Image


class MyFont:
    def __init__(self, filename, descriptor):
        with open(descriptor, 'r', encoding='utf-8') as desc:
            self.descriptor = json.load(desc)
        self.image = Image.open(filename)
        if self.image.mode != "1":
            self.image = self.image.convert("1")
        self.image.load()
        self.glyphs = {}

        self.tile_width = self.descriptor["TILE_WIDTH"]
        self.glyph_width = self.descriptor["GLYPH_WIDTH"]
        self.tile_height = self.descriptor["TILE_HEIGHT"]
        self.glyph_height = self.descriptor["GLYPH_HEIGHT"]
        self.width = self.image.width // self.tile_width
        self.height = self.image.height // self.tile_height
        glyph_groups = self.descriptor["glyphs"]
        glyphs = ''.join(glyph_groups)
        for i, glyph in enumerate(glyphs):
            line = i // self.width
            column = i % self.width
            left = column * self.tile_width
            up = line * self.tile_height
            right = left + self.glyph_width
            low = up+self.glyph_height

            img = self.image.crop(box=(left, up, right, low))
            img.load()
            self.glyphs[glyph] = img.im


    def get_crop_by_character(self, character):
        return self.glyphs[character]

    def getmask(self, text, mode):
        glyphs = list(map(self.get_crop_by_character, text))
        a = Image.new('1', (len(glyphs)*self.glyph_width, self.glyph_height))
        for i, glyph in enumerate(glyphs):
            a.paste(glyph, (i*self.glyph_width, 0, (i+1)*self.glyph_width, 0+self.glyph_height))
        return a.im
