from ui.drawable import Mod
from ui.layout.horizontal import HorizontalLayout
from ui.layout.VerticalLayout import VerticalLayout
from ui.layout.layout import Align

from ui.widgets.text import TextWidget
from ui.widgets.time import TimeWidget
from ui.widgets.ip import IPWidget
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

    def render(self):
        pass

    # def draw(self, canvas):
    #     pass

    def finish(self, result):
        self.ui.pop_view(result)

    def push_view(self, view, callback=None):
        self.ui.push_view(view, callback)

    def set_state(self, **state):
        self.state = py_.assign({}, self.state, state)

    def onreturn(self, result):
        print('view returned ', result)


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
            counter = self.state['counter'] + 1
            if counter >= len(self.props['items']):
                counter = 0
            self.set_state(counter=counter)
        elif action == View.ACTION_UP:
            counter = self.state['counter'] - 1
            if counter < 0:
                counter += len(self.props['items'])
            self.set_state(counter=counter)
        elif action == View.ACTION_ENTER:
            try:
                v = TitleView(fnt=self.fnt, ui=self.ui, **(py_.assign({}, self.props, {'title':self.props['title']+'.!'})))
                self.push_view(v, self.onreturn)
            except Exception as x:
                print(x)
        elif action == View.ACTION_BACK:
            self.finish(self.state['counter'])

    def render(self):

        menu_items = [TextWidget.prep(text=text,
                                      mod=Mod.NEGATE if i == self.state['counter'] else None)
                      for i, text in enumerate(self.props['items'])]

        return VerticalLayout.prep(
            ctx={"fnt": self.fnt},
            w=[
                VerticalLayout.prep(
                    mod=Mod.UNDERLINE,
                    w=[
                        HorizontalLayout.prep(
                            align=Align.SPACE_BETWEEN,
                            mod=Mod.NEGATE,
                            w=[
                                TimeWidget.prep(),
                                IPWidget.prep()
                            ]
                        ),
                        HorizontalLayout.prep(
                            align=Align.LEFT,
                            w=[
                                TextWidget.prep(text=self.props['title'])
                            ]
                        )
                    ]
                ),
                VerticalLayout.prep(
                    w=menu_items
                )
            ]
        )
