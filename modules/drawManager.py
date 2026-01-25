from modules.guiManager import *
from modules.floorManager import *
class drawManager:
    def __init__(self):
        ''' Creates a class that manages the tools and handles drawing and saving. Contains a GUI manager and the Floor Manager.
        '''
        self.default_font = self.init_font('/Fonts/Lato-Regular.ttf')
        self.gui_manager = guiManager(self)
        self.floor_manager = FloorManager(self, (1200, 800))
        
        self.current_brush = None # for communication between gui and floor manager


    def draw(self):
        self.floor_manager.draw()
        self.gui_manager.draw()
        

    def send_events(self, event):
        self.gui_manager.send_events(event)
        self.floor_manager.handle_event(event)

    def init_font(self, file):
        # try to load the font. don't load anything but helvetica 12 for now. evil, i know.
        try:
            #FONT = globals().get(file, None)
            FONT = GLUT_BITMAP_HELVETICA_12 #type: ignore

        except Exception as e:
            try:
                FONT = GLUT_BITMAP_HELVETICA_12 #type: ignore
                print(f"Could not load font: {e}")
            except Exception:
                FONT = None
        
        return FONT