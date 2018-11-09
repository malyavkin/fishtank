import asyncio


class UI:
    def __init__(self, canvas):
        self.view_stack = []
        self.canvas = canvas
        self.RUNNING = False
        self.console_mgr = None

    def command(self, command):
        self.get_current_view().command(command)

    async def run(self, console_mgr):
        self.console_mgr = console_mgr
        while self.RUNNING:
            self.draw()
            await asyncio.sleep(0)
        return

    def push_view(self, view, callback=None):
        self.view_stack.append({"view": view, "callback": callback})
        self.RUNNING = True

    def pop_view(self, result):
        if self.view_stack:
            last = self.view_stack.pop(-1)
            if last['callback'] is not None:
                last['callback'](result)

        if not self.view_stack:
            self.RUNNING = False
            self.console_mgr.stop()

    def get_current_view(self):
        return self.view_stack[-1]['view']

    def draw(self):
        self.get_current_view().draw(self.canvas)
