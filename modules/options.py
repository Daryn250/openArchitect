from OpenGL.GL import *
from OpenGL.GLUT import *
import glfw



class OptionBase:
    def __init__(self, font, label="", height=24):
        self.label = label
        self.height = height
        self.bg_padding = 4
        self.font = font
        self.FONT_HEIGHT = 12
        self.FONT_BASELINE_OFFSET = 4

    def draw_label(self, x, y, label, color=(0.95,0.95,0.95,1.0)):
        # Small helper to draw a label left-aligned at (x,y)
        glColor4f(*color)
        if self.font is None: # type: ignore
            return
        glRasterPos2f(x, y)
        for ch in str(label):
            try:
                glutBitmapCharacter(self.font, ord(ch)) # type: ignore
            except Exception:
                continue
    
    def draw_label_centered(self, x, center_y, label, color=(0.95,0.95,0.95,1.0)):
        baseline_y = center_y + self.FONT_HEIGHT/2
        self.draw_label(x, baseline_y, label, color)

    
    def draw_background(self, x, y, width, panel_color):
        pad = self.bg_padding

        # slightly darker than panel, but derived from it
        r, g, b, a = panel_color
        bg_color = (r * 0.85, g * 0.85, b * 0.85, a)

        glColor4f(*bg_color)
        glBegin(GL_QUADS)
        glVertex2f(x - pad, y - pad)
        glVertex2f(x + width + pad, y - pad)
        glVertex2f(x + width + pad, y + self.height + pad)
        glVertex2f(x - pad, y + self.height + pad)
        glEnd()

    def title_height(self):
        # reserve a small area at the top of each option for the title/label
        return min(18, max(12, int(self.height * 0.4)))

    def title_y(self, y):
        # y is the top of the option block; return y position for raster text
        # approximate vertical placement so text appears visually centered
        return y + (self.title_height() - 4)

    def content_y(self, y):
        # top y coordinate where the control content should begin
        return y + self.title_height() + 6

class Slider(OptionBase):
    def __init__(self, font, label="", value=0.5, minimum=0.0, maximum=1.0, height=34, step = None):
        super().__init__(font, label, height)
        self.value = float(value)
        self.min = float(minimum)
        self.max = float(maximum)
        self.step = step

    def draw(self, x, y, width, panel_color):
        self.draw_background(x, y, width, panel_color)
        # draw label (top area)
        self.draw_label(x, self.title_y(y), self.label)
        # draw track (on next line)
        track_w = max(40, width - 40)
        track_x = x + (width - track_w)
        track_y = self.content_y(y) + 6
        glColor4f(0.28, 0.28, 0.28, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(track_x, track_y - 4)
        glVertex2f(track_x + track_w, track_y - 4)
        glVertex2f(track_x + track_w, track_y + 4)
        glVertex2f(track_x, track_y + 4)
        glEnd()
        # knob
        t = (self.value - self.min) / max(1e-6, (self.max - self.min))
        knob_x = track_x + t * track_w - 6
        glColor4f(0.85, 0.85, 0.85, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(knob_x, track_y - 8)
        glVertex2f(knob_x + 12, track_y - 8)
        glVertex2f(knob_x + 12, track_y + 8)
        glVertex2f(knob_x, track_y + 8)
        glEnd()

    def send_event(self, event, options = None):
        if options is None:
            options = []
        # handle mouse events for slider interaction
        event_type = event.get('type')
        if event_type == 'mouse_button':
            # handle knob dragging
            action = event.get('action')
            if action == 1:  # GLFW_PRESS
                self.dragging = True
            elif action == 0:  # GLFW_RELEASE
                self.dragging = False
        elif event_type == 'mouse_move' and hasattr(self, 'dragging') and self.dragging:
            # update value based on mouse position
            width = event.get('width', 100)
            track_w = max(40, width - 40)
            rel_x = event.get('x', 0)
            # clamp relative x to track bounds
            track_start = width - track_w
            t = (rel_x - track_start) / max(1e-6, track_w)
            t = max(0.0, min(1.0, t))
            raw_value = self.min + t * (self.max - self.min)

            if self.step is not None and self.step > 0:
                steps = round((raw_value - self.min) / self.step)
                stepped_value = self.min + steps * self.step
                self.value = max(self.min, min(self.max, stepped_value))
            else:
                self.value = raw_value

class Label(OptionBase):
    def __init__(self, font, label="", height=28):
        super().__init__(font, label, height)

    def draw(self, x, y, width, panel_color):
        self.draw_background(x, y, width, panel_color)
        # draw label inline
        title_h = self.title_height()
        center_y = y + title_h / 2
        self.draw_label_centered(x, center_y, self.label)
        
        # inline shrink height
        self.height = int(self.title_height() + 6)

    def send_event(self, event, options = None):
        if options is None:
            options = []
        # do nothing. nothing to do with a title.

class CheckBox(OptionBase):
    def __init__(self, font, label="", checked=False, height=28):
        super().__init__(font, label, height)
        self.checked = bool(checked)

    def draw(self, x, y, width, panel_color):
        self.draw_background(x, y, width, panel_color)
        # draw label inline and checkbox on same line
        title_h = self.title_height()
        center_y = y + title_h / 2
        self.draw_label_centered(x, center_y, self.label)

        box_size = 16
        # center checkbox vertically inside title area
        title_h = self.title_height()
        box_center_y = y + title_h / 2 + 2
        by = box_center_y - (box_size / 2)
        bx = x + width - box_size
        if self.checked:
            glColor4f(0.9, 0.9, 0.9, 1.0)
        else:
            glColor4f(0.3, 0.3, 0.3, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(bx, by)
        glVertex2f(bx + box_size, by)
        glVertex2f(bx + box_size, by + box_size)
        glVertex2f(bx, by + box_size)
        glEnd()
        if self.checked:
            # draw a simple check mark
            glColor4f(0.06, 0.06, 0.06, 1.0)
            glBegin(GL_LINES)
            glVertex2f(bx + 3, by + 9)
            glVertex2f(bx + 7, by + 13)
            glVertex2f(bx + 7, by + 13)
            glVertex2f(bx + 13, by + 5)
            glEnd()
        # inline checkbox: shrink height to title area + padding
        self.height = int(self.title_height() + 6)

    def send_event(self, event, options = None):
        if options is None:
            options = []
        # toggle checkbox on click
        event_type = event.get('type')
        if event_type == 'mouse_button':
            action = event.get('action')
            if action == 1:  # GLFW_PRESS
                self.checked = not self.checked

class ColorSwatch(OptionBase):
    def __init__(self, font, label="", color=(1,1,1,1), height=28):
        super().__init__(font, label, height)
        self.color = color

    def draw(self, x, y, width, panel_color):
        self.draw_background(x, y, width, panel_color)
        # draw label inline, swatch on same line
        title_h = self.title_height()
        center_y = y + title_h / 2
        self.draw_label_centered(x, center_y, self.label)

        sw = 20
        title_h = self.title_height()
        sw_center_y = y + title_h / 2 + 2
        sy = sw_center_y - (sw / 2)
        sx = x + width - sw
        glColor4f(*self.color)
        glBegin(GL_QUADS)
        glVertex2f(sx, sy)
        glVertex2f(sx + sw, sy)
        glVertex2f(sx + sw, sy + sw)
        glVertex2f(sx, sy + sw)
        glEnd()
        # inline swatch height
        self.height = int(self.title_height() + 6)

    def send_event(self, event, options = None):
        if options is None:
            options = []
        # color swatch could open a color picker dialog on click
        event_type = event.get('type')
        if event_type == 'mouse_button':
            action = event.get('action')
            if action == 1:  # GLFW_PRESS
                # TODO: Open a color picker dialog
                pass

class Clickable_Button(OptionBase): # for the clickable buttons. ex: open file, save, ect.
    def __init__(self, font, label="", height=30):
        super().__init__(font, label, height)
        self.selected = False

    def draw(self, x, y, width, panel_color):
        self.draw_background(x, y, width, panel_color)
        # button background - lighter color when selected
        if self.selected:
            glColor4f(0.42, 0.42, 0.42, 1.0)
        else:
            glColor4f(0.22, 0.22, 0.22, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + self.height)
        glVertex2f(x, y + self.height)
        glEnd()
        # label centered vertically
        label_y = y + (self.height // 2) + 4
        self.draw_label(x + 6, label_y, self.label)

    def send_event(self, event, options = None):
        if options is None:
            options = []
        # handle button click
        event_type = event.get('type')
        if event_type == 'mouse_button':
            action = event.get('action')
            if action == 1:  # GLFW_PRESS
                print(f"Button clicked: {self.label}")
    
class Clickable_Tab(OptionBase): # for the clickable tabs. only one per panel should be selected
    def __init__(self, font, panel, panel_manager, label="", height=30):
        super().__init__(font, label, height)
        self.selected = False
        self.panel = panel # allow it to open/close it's specific panel. 
        self.panel_manager = panel_manager

    def draw(self, x, y, width, panel_color):
        self.draw_background(x, y, width, panel_color)
        # button background - lighter color when selected
        if self.selected:
            glColor4f(0.42, 0.42, 0.42, 1.0)
        else:
            glColor4f(0.22, 0.22, 0.22, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + self.height)
        glVertex2f(x, y + self.height)
        glEnd()
        # label centered vertically
        label_y = y + (self.height // 2) + 4
        self.draw_label(x + 6, label_y, self.label)

    def send_event(self, event, options = None):
        if options is None:
            options = []
        # handle button click
        event_type = event.get('type')
        if event_type == 'mouse_button':
            action = event.get('action')
            if action == 1:  # GLFW_PRESS
                # deselect all Clickables recursively in the provided options list
                to_clear = self._deselect_all_clickables(options)
                for item in to_clear:
                    item.panel_manager.delete_panel(item.panel)

                # toggle selected state
                if self.selected:
                    self.selected = False
                    # remove the panel from the panel manager when deselected
                    self.panel_manager.delete_panel(self.panel)
                else:
                    self.selected = True
                    # add the panel to the panel manager when selected
                    self.panel_manager.add_existing_panel(self.panel)
    
    def _deselect_all_clickables(self, options, depth=0, max_depth=10):
        if depth > max_depth or not options:
            return []

        to_clear = []

        for option in options:
            if option is self:
                continue

            if isinstance(option, Clickable_Tab):
                option.selected = False
                to_clear.append(option)

            elif isinstance(option, DropDown_Settings):
                to_clear.extend(
                    self._deselect_all_clickables(option.children, depth + 1, max_depth)
                )

        return to_clear

class DropDown_Settings(OptionBase): # for expandable/closable folders in tabs
    def __init__(self, font, label="", children=None, expanded=False, height=28):
        super().__init__(font, label, height)
        self.children = children or []
        self.expanded = expanded

    def draw(self, x, y, width, panel_color):
        self.draw_background(x, y, width, panel_color)
        # header (title area)
        self.draw_label(x, self.title_y(y), ("[-] " if self.expanded else "[+] ") + self.label)
        # draw children if expanded (stacked below)
        total_h = self.title_height()
        if self.expanded:
            cy = self.content_y(y)  # Start at content_y for consistent placement
            for child in self.children:
                # place each child on its own block with padding
                child.draw(x + 8, cy, width - 16, panel_color)
                cy += child.height + 6
            # include children in this dropdown's height so following content
            # is placed after this expanded block
            total_h += sum((child.height + 6) for child in self.children)

        # update reported height so Panel.draw advances correctly
        self.height = total_h

    def send_event(self, event, options = None):
        if options is None:
            options = []
        # only toggle on clicks to the title area, not children
        event_type = event.get('type')
        event_y = event.get('y', -1)
        title_h = self.title_height()
        
        # check if event is in title area (top portion)
        if event_y < title_h:
            if event_type == 'mouse_button':
                action = event.get('action')
                if action == 1:  # GLFW_PRESS
                    self.expanded = not self.expanded
                    return  # consume the event for the title click
        # if expanded and event is in children area, route to children
        elif self.expanded and event_y >= title_h:
            # calculate y positions for children to route events
            padding = 6
            cy = title_h + padding
            for child in self.children:
                child_top = cy
                child_bottom = cy + child.height
                if child_top <= event_y <= child_bottom:
                    rel_y = event_y - child_top
                    child_event = event.copy()
                    child_event['y'] = rel_y
                    if hasattr(child, 'send_event'):
                        # pass the parent panel's options list so Clickable can deselect everything
                        child.send_event(child_event, options)
                    return  # consume the event since we found a matching child
                cy += child.height + padding
            # if expanded but no child matched, don't consume the event
        # if not expanded or event didn't match, don't consume the event

class DropDown_Picker(OptionBase): # for choosing options from a dropdown
    def __init__(self, font, label="", options=None, selected=0, height=30):
        super().__init__(font, label, height)
        self.options = options or []
        self.selected = selected

    def draw(self, x, y, width, panel_color):
        self.draw_background(x, y, width, panel_color)
        # draw label inline and show picker box on the same line
        title_h = self.title_height()
        center_y = y + title_h / 2
        self.draw_label_centered(x, center_y, self.label)

        # small inline picker box to the right
        box_w = min(140, width // 2)
        bx = x + width - box_w
        box_h = 20
        # center box vertically within title area
        
        by = y + (title_h - box_h) / 2 + 2
        glColor4f(0.22, 0.22, 0.22, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(bx, by)
        glVertex2f(bx + box_w, by)
        glVertex2f(bx + box_w, by + box_h)
        glVertex2f(bx, by + box_h)
        glEnd()
        if 0 <= self.selected < len(self.options):
            box_center_y = by + box_h / 2
            self.draw_label_centered(bx + 6, box_center_y, self.options[self.selected])

        # inline control -> keep height as title area plus small padding
        self.height = int(self.title_height() + 6)

    def send_event(self, event, options = None):
        # cycle through options on click
        event_type = event.get('type')
        if event_type == 'mouse_button':
            action = event.get('action')
            if action == 1:  # GLFW_PRESS
                if len(self.options) > 0:
                    self.selected = (self.selected + 1) % len(self.options)