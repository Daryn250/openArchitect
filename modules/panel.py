from OpenGL.GL import *
from OpenGL.GLUT import *
import glfw
from modules.options import *




# first, make a class for a panel manager
class PanelManager:
    def __init__(self, drawManager):
        self.panels = []
        # default manager tint/color as RGBA tuple usable by OpenGL
        self.color = (0.1, 0.1, 0.1, 0.9)
        self.drawManager = drawManager
        self.font = drawManager.default_font

    def draw(self):
        current_offset = 0
        height = 0 # dunno what to do about this
        for panel in self.panels:
            panel.draw(current_offset, height, self.color)
            current_offset += panel.width # get the width of the current panel and add it to offset to draw next panel correctly
    
    def send_events(self, event):
        # route events to panels and provide each panel its x-offset so it
        # can perform hit-testing
        current_offset = 0
        for panel in self.panels:
            panel.send_event(event, current_offset)
            current_offset += panel.width

    def add_new_panel(self):
        self.panels.append(Panel())
    
    def add_existing_panel(self, panel):
        self.panels.append(panel)

    def delete_panel(self, panel):
        self.panels[:] = [p for p in self.panels if p is not panel]


# next, make a modular panel class

class Panel:
    def __init__(self, to_add = []):
        self.width = 150 # default of 150
        self.height = 800 # default of screen size. currently 800, will make modular later.
        self.options = [] # list of all options.
        self.padding = 12
        for item in to_add:
            self.add_option(item)

    def draw(self, current_offset, height, color):
        # draw the panel background at the given horizontal offset
        panel_x = current_offset
        panel_y = 0

        # make sure color is an RGBA tuple; fall back to semi-transparent black
        bg = color if (isinstance(color, (list, tuple)) and len(color) >= 4) else (0.0, 0.0, 0.0, 0.6)

        # enable blending so alpha is respected
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glColor4f(bg[0], bg[1], bg[2], bg[3])
        glBegin(GL_QUADS)
        glVertex2f(panel_x, panel_y)
        glVertex2f(panel_x + self.width, panel_y)
        glVertex2f(panel_x + self.width, panel_y + self.height)
        glVertex2f(panel_x, panel_y + self.height)
        glEnd()

        # optional thin border
        glColor4f(0.0, 0.0, 0.0, min(1.0, bg[3] + 0.2))
        glLineWidth(1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(panel_x, panel_y)
        glVertex2f(panel_x + self.width, panel_y)
        glVertex2f(panel_x + self.width, panel_y + self.height)
        glVertex2f(panel_x, panel_y + self.height)
        glEnd()

        # draw the options with padding
        padding = self.padding
        option_current_height = padding # set to be where options starts drawing.
        for option in self.options:
            option.draw(panel_x + padding, option_current_height, self.width-(padding*2), color)
            option_current_height += padding + option.height
    

    def send_event(self, event, offset_x=0):
        # event: dict with keys 'type','x','y','button','action'
        ex = event.get('x')
        ey = event.get('y')
        # check if event is within this panel
        if ex is None or ey is None:
            return
        # if click outside panel, ignore
        if not (offset_x <= ex <= offset_x + self.width and 0 <= ey <= self.height):
            return

        # translate to panel-local coordinates
        local_x = ex - offset_x

        padding = self.padding
        opt_x = padding
        opt_w = max(32, self.width - (padding * 2))
        option_current_height = padding
        for option in self.options:
            opt_top = option_current_height
            opt_bottom = opt_top + option.height
            # check if event y falls within this option's vertical range
            if ey >= opt_top and ey <= opt_bottom:
                # compute coordinates relative to option (x from left padding)
                rel_x = local_x - opt_x
                rel_y = ey - opt_top
                # call option's send_event if available
                if hasattr(option, 'send_event'):
                    option.send_event({'type': event.get('type'), 'x': rel_x, 'y': rel_y, 'button': event.get('button'), 'action': event.get('action'), 'width': opt_w}, self.options)
                # only the topmost option should receive the event
                return
            option_current_height += padding + option.height
    
    def add_option(self, option):
        self.options.append(option)
    




def create_default_panels(drawManager):
    """Create a PanelManager that contains the default structure
    of the GUI. Includes Elements, Libraries, Measurements, and Options.
    """
    pm = PanelManager(drawManager)

    p1 = Panel()
    p1.width = 150
    p1.height = 800
    
    # clickable button, dropdown settings, slider, checkbox, color swatch, dropdown, tab
    p1.add_option(Clickable_Tab(pm.font,Panel([
        DropDown_Settings(pm.font, "Walls", [
            Clickable_Button(pm.font,"Wall"),
            Clickable_Button(pm.font,"Curved Wall"),
            Clickable_Button(pm.font,"Glass Wall"),
            Slider(pm.font,"Wall Width",12,1,30,34,0.5),
            Clickable_Button(pm.font,"Break Wall"),
        ], False),
        DropDown_Settings(pm.font,"Doors", [
            DropDown_Picker(pm.font,"Door Type", ["Regular", "Double", "Revolving", "Pocket"]),
            CheckBox(pm.font,"Arched Doorway"),

        ], False),
        DropDown_Settings(pm.font,"Decorations", [
            Label(pm.font,"Furniture"), # needs a new type to select from an expandable list of images
            Label(pm.font,"Plants"),
            Label(pm.font,"Industrial"),
            Label(pm.font,"More"),
        ], False)

    ]), pm, "ELEMENTS"))
    p1.add_option(Clickable_Tab(pm.font,Panel([
        Clickable_Button(pm.font,"Add a Library"),
        Clickable_Button(pm.font,"Modify a Library"),
        Label(pm.font,"Installed Libraries:")
    ]), pm, "LIBRARIES"))

    p1.add_option(Clickable_Tab(pm.font,Panel([
        Clickable_Button(pm.font,"Measure"),
        Clickable_Button(pm.font,"Constrain"),
        Clickable_Button(pm.font,"Delete Measurement"),
        DropDown_Picker(pm.font,"Units", ["Metric", "Imperial", "Pixel"])
    ]), pm, "MEASUREMENTS"))

    p1.add_option(Clickable_Tab(pm.font,Panel([
        Label(pm.font,"Nothing Here!")
    ]), pm, "OPTIONS"))

    pm.add_existing_panel(p1)

    return pm



# currently, I just want to make the structure right now. I'll focus on more later. I want it to look similar to gimp's toolbox or any other
# editing software.