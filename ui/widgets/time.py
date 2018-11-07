from time import time


def time_widget(xy, image, fnt):
    ts = int(time() + 3 * 3600)
    minutes = (ts // 60) % 60
    hours = (ts // 3600) % 24
    string = "{:0>2}{}{:0>2}".format(hours, ":" if int(time()) % 2 else " ", minutes)
    image.text(xy, string, fill=255, font=fnt)
