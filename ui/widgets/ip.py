from time import time

from ui.widgets.text import TextWidget


class IPWidget(TextWidget):
    def __init__(self, ctx, mod):
        super().__init__(ctx, mod)
        self.ip = None

    def gettext(self):
        if not self.ip:
            try:
                import socket
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                self.ip = s.getsockname()[0]
                s.close()
            except Exception as x:
                self.ip = 'Нет сети'
        return self.ip
