#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2015 Richard Hull
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# Example usage:
#
#   from oled.Device import ssd1306, sh1106
#   from oled.render import canvas
#   from PIL import ImageFont, ImageDraw
#
#   font = ImageFont.load_default()
#   Device = ssd1306(port=1, address=0x3C)
#
#   with canvas(Device) as draw:
#      draw.rectangle((0, 0, Device.width, Device.height), outline=0, fill=0)
#      draw.text(30, 40, "Hello World", font=font, fill=255)
#
# As soon as the with-block scope level is complete, the graphics primitives
# will be flushed to the Device.
#
# Creating a new canvas is effectively 'carte blanche': If you want to retain
# an existing canvas, then make a reference like:
#
#    c = canvas(Device)
#    for X in ...:
#        with c as draw:
#            draw.rectangle(...)
#
# As before, as soon as the with block completes, the canvas buffer is flushed
# to the Device

from time import time, sleep

from PIL import Image


def timeit(fn):
    def inner(*args, **kwargs):
        s = time()
        fn(*args, **kwargs)
        duration = time() - s
        print('render time', duration)

    return inner


class DummyCanvas:
    def __init__(self, size):
        self.size = size
        self.image = Image.new('1', self.size)
        self.black = Image.new('RGB', self.size)
        self.display = Image.open('./assets/display.bmp').convert('RGB')

    def __enter__(self):
        return self.image

    def __exit__(self, type, value, traceback):
        if type is None:
            try:
                Image.composite(self.display, self.black, self.image).save('1.png')
                sleep(0.05)
            except Exception as e:
                raise print(e)

        self.image = Image.new('1', self.size)  # Tidy up the resources
        return False  # Never suppress exceptions


class canvas(object):
    """
    A canvas returns a properly-sized `ImageDraw` object onto which the caller
    can draw upon. As soon as the with-block completes, the resultant image is
    flushed onto the Device.
    """

    def __init__(self, device):
        # self.draw = None
        self.image = Image.new('1', (device.width, device.height))
        self.device = device

    def __enter__(self):
        # self.draw = ImageDraw.Draw(self.image)
        return self.image

    @timeit
    def __exit__(self, type, value, traceback):
        if type is None:
            # do the drawing onto the Device
            self.device.display(self.image)

        del self.image  # Tidy up the resources
        return False  # Never suppress exceptions
