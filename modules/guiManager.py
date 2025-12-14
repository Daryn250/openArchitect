# manages gui windows and handles passing updates to gui elements

from modules.panel import *

class guiManager:
    def __init__(self, drawManager):
        self.windows = [] # list of arbitrary windows
        self.panelManager = create_default_panels(drawManager)
        self.drawManager = drawManager

    def draw(self):
        # draw panel and then windows
        self.panelManager.draw()

        for window in self.windows:
            window.draw()

    def send_events(self, event):
        # route events to internal GUI elements (panels, windows)
        self.panelManager.send_events(event)

        for window in self.windows:
            window.update()
    