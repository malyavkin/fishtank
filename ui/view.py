from PIL import ImageDraw

from ui.widgets.time import time_widget
from pydash import py_

class View:
    ACTION_DOWN = 'down'
    ACTION_UP = 'up'
    ACTION_LEFT = 'left'
    ACTION_RIGHT = 'right'
    ACTION_ENTER = 'enter'
    ACTION_BACK = 'back'

    def __init__(self, ui, fnt, **props):
        self.props = props
        self.fnt = fnt
        self.ui = ui
        self.state = {}

    def command(self, action):
        pass

    def draw(self, canvas):
        pass

    def finish(self, result):
        self.ui.pop_view(result)

    def push_view(self, view, callback=None):
        self.ui.push_view(view, callback)

    def set_state(self, **state):
        self.state = py_.assign({}, self.state, state)


class TitleView(View):
    def __init__(self, ui, fnt, **props):
        super().__init__(fnt=fnt, ui=ui, **props)
        self.state = {
            'counter': 0,
        }

    def onreturn(self, result):
        print('view returned ', result)

    def command(self, action):
        if action == View.ACTION_DOWN:
            self.set_state(counter=self.state['counter'] - 1)
        elif action == View.ACTION_UP:
            self.set_state(counter=self.state['counter'] + 1)
        elif action == View.ACTION_ENTER:
            v = TitleView(fnt=self.fnt, ui=self.ui, title=self.props['title'] + '!')
            self.push_view(v, self.onreturn)
        elif action == View.ACTION_BACK:
            try:
                self.finish(self.state['counter'])
            except Exception as e:
                print(e)

    def draw(self, canvas):
        with canvas as image:
            # draw.paste(f)
            draw = ImageDraw.Draw(image)
            time_widget((0, 0), draw, self.fnt)
            draw.text((40, 0), '192.168.1.172', fill=255, font=self.fnt)
            draw.text((0, 8), self.props['title'] + str(self.state['counter']), fill=255, font=self.fnt)
            draw.line((0, 15, 127, 15), fill=255, width=1)
