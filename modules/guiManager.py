# manages gui windows and handles passing updates to gui elements

from modules.panel import Panel

class guiManager:
    def __init__(self):
        self.windows = [] # list of arbitrary windows
        self.panel = Panel() # panel class

    def draw(self):
        # draw panel and then windows
        self.panel.draw()

        for window in self.windows:
            window.draw()

    def send_updates(self, update):
        # send updates? not sure how they work yet. ngl. funny.
        self.panel.update(update)

        for window in self.windows:
            window.update()