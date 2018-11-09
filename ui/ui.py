from PIL import ImageDraw
from ui.widgets.time import time_widget
import asyncio
from aioconsole import ainput

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


    def manage(self, view):
        def pop_view(result):
            print(result)
            self.pop_view()

    def push_view(self, view, callback=None):
        self.view_stack.append({"view":view, "callback":callback})
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



class View:
    ACTION_DOWN = 'down'
    ACTION_UP = 'up'
    ACTION_LEFT = 'left'
    ACTION_RIGHT = 'right'
    ACTION_ENTER = 'enter'
    ACTION_BACK = 'back'

    def __init__(self, UI, fnt):
        self.fnt = fnt
        self.UI = UI

    def command(self, action):
        pass

    def draw(self, canvas):
        pass

    def finish(self, result):
        self.UI.pop_view(result)

    def push_view(self, view, callback=None):
        self.UI.push_view(view, callback)


class TitleView(View):
    def __init__(self, UI, fnt, title):
        self.last_command = None
        super().__init__(fnt=fnt, UI=UI)
        self.initial_title = title
        self.title = title

    def onreturn(self, result):
        print('view returned ', result)

    def command(self, action):
        if action == View.ACTION_DOWN:
            self.title = self.initial_title + 'вниз'
        elif action == View.ACTION_UP:
            self.title = self.initial_title + 'вверх'
        elif action == View.ACTION_ENTER:
            v = TitleView(fnt=self.fnt, UI=self.UI, title=self.initial_title+'!')
            self.push_view(v, self.onreturn)
        elif action == View.ACTION_BACK:
            try:
                self.finish(self.title)
            except Exception as e:
                print(e)
            

    def draw(self, canvas):
        with canvas as image:
            # draw.paste(f)
            draw = ImageDraw.Draw(image)
            time_widget((0, 0), draw, self.fnt)
            draw.text((40, 0), '192.168.1.172', fill=255, font=self.fnt)
            draw.text((0, 8), self.title, fill=255, font=self.fnt)
            draw.line((0, 15, 127, 15), fill=255, width=1)
