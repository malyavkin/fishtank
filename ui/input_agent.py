from ui.view import View
from aioconsole import ainput


class Console:

    def __init__(self):
        self.actions = {
            "w": View.ACTION_UP,
            "a": View.ACTION_LEFT,
            "s": View.ACTION_DOWN,
            "d": View.ACTION_RIGHT,
            "q": View.ACTION_BACK,
            "e": View.ACTION_ENTER
        }
        self.RUNNING = True

    def stop(self):
        self.RUNNING = False
        print('Received stop signal. Send anything to exit')

    async def run(self, mgr):
        while self.RUNNING:
            command = await ainput('(wasd/qe)>')
            if command in self.actions.keys():
                mgr.command(self.actions[command])
