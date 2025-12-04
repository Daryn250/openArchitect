# create a panel class for the gui. organize like a file struct.
# eg.
# ELEMENTS
# - wall
# - - straight wall
# - - - wall width
# - - curved wall
# - - - wall width
# - - - wall angles (?)
# - - window wall
# - - - window height
# - - break wall
# - doors
# - - door types
# - - - door arch type
# - decoration
# - - furniture
# - - plants
# - - industrial
# - - ect
# - more
# LIBRARIES
# - add a library
# - modify a library
# - - library selector
# MEASUREMENTS
# - measure
# - constrain
# - delete measurement
# ECT

# currently, I just want to make the structure right now. I'll focus on more later. I want it to look similar to gimp's toolbox or any other
# editing software.

from OpenGL.GL import *
from OpenGL.GLUT import *


# try to ensure a bitmap font symbol exists; if not, fall back to None
try:
    FONT_HELV_12 = GLUT_BITMAP_HELVETICA_12
except NameError:
    try:
        FONT_HELV_12 = globals().get('GLUT_BITMAP_HELVETICA_12', None)
    except Exception:
        FONT_HELV_12 = None


class Panel:
    def __init__(self, pos=(0, 0), size=(220, 600), tools=None):
        """Create a visually complete toolbox panel.
        This implementation only draws the menu and controls — it does not
        implement interactive behavior (mouse/keyboard) beyond keeping a
        selected index for visual state.
        - pos: top-left position in framebuffer coordinates
        - size: (width, height) in framebuffer coordinates
        - tools: optional list of tool names; each tool will show a properties
          section on the right when selected.
        """
        self.x, self.y = pos
        self.width, self.height = size
        self.tools = tools or [
            "Select",
            "Wall",
            "Door",
            "Decoration",
            "Measure",
            "Library",
            "Settings",
        ]

        self.selected = 1  # default to 'Wall' visually

        # Example property templates for each tool (for rendering only)
        self.tool_properties = {
            "Select": [
                ("Mode", "Radio", ["Pointer", "Lasso", "Marquee"], 0),
            ],
            "Wall": [
                ("Width", "Slider", 4.0, 1.0, 64.0),
                ("Color", "Swatch", (0.9, 0.9, 0.9, 1.0)),
                ("Snap to Grid", "Checkbox", True),
            ],
            "Door": [
                ("Width", "Slider", 30.0, 10.0, 120.0),
                ("Swing", "Radio", ["In", "Out", "Sliding"], 0),
            ],
            "Decoration": [
                ("Opacity", "Slider", 1.0, 0.0, 1.0),
            ],
            "Measure": [
                ("Units", "Radio", ["px", "cm", "in"], 0),
                ("Show Labels", "Checkbox", True),
            ],
            "Library": [
                ("Category", "Dropdown", ["Furniture", "Plants", "Fixtures"], 0),
            ],
            "Settings": [
                ("Snap", "Checkbox", True),
                ("Grid Size", "Slider", 50, 5, 200),
            ],
        }

    # ---------- drawing helpers ----------
    def _draw_text(self, x, y, text, font=None, color=(0, 0, 0, 1)):
        # Use provided font or the detected default; if no font available, skip drawing
        use_font = font if font is not None else FONT_HELV_12
        glColor4f(*color)
        if use_font is None:
            return
        glRasterPos2f(x, y)
        for ch in str(text):
            try:
                glutBitmapCharacter(use_font, ord(ch))
            except Exception:
                # if character draw fails, continue gracefully
                continue

    def _rounded_rect(self, x, y, w, h, color):
        # simple filled rectangle; rounded corners not required for now
        glColor4f(*color)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + w, y)
        glVertex2f(x + w, y + h)
        glVertex2f(x, y + h)
        glEnd()

    # ---------- public API ----------
    def select_tool(self, index):
        if 0 <= index < len(self.tools):
            self.selected = index

    def draw(self):
        """Render the full toolbox panel. Assumes an orthographic projection
        with framebuffer coordinates (same coordinate system used elsewhere).
        """
        left_w = 110  # width of tool list
        pad = 8

        glPushMatrix()
        try:
            # Translate to panel top-left
            glTranslatef(self.x, self.y, 0)

            # Panel background
            self._rounded_rect(0, 0, self.width, self.height, (0.12, 0.12, 0.12, 0.95))

            # Tools header
            header_h = 30
            self._rounded_rect(0, 0, self.width, header_h, (0.16, 0.16, 0.16, 1.0))
            self._draw_text(pad, 10, "Tools", color=(1, 1, 1, 1))

            # Left: tool list
            y_off = header_h + pad
            btn_h = 34
            for idx, name in enumerate(self.tools):
                btn_y = y_off + idx * (btn_h + 6)
                is_selected = (idx == self.selected)

                # button background
                if is_selected:
                    self._rounded_rect(pad, btn_y, left_w - pad * 2, btn_h, (0.25, 0.45, 0.85, 1.0))
                    text_col = (1, 1, 1, 1)
                else:
                    self._rounded_rect(pad, btn_y, left_w - pad * 2, btn_h, (0.18, 0.18, 0.18, 1.0))
                    text_col = (0.9, 0.9, 0.9, 1.0)

                # simple icon square
                icon_size = 18
                icon_x = pad + 6
                icon_y = btn_y + (btn_h - icon_size) * 0.5
                glColor4f(0.9, 0.9, 0.9, 1.0) if is_selected else glColor4f(0.7, 0.7, 0.7, 1.0)
                glBegin(GL_QUADS)
                glVertex2f(icon_x, icon_y)
                glVertex2f(icon_x + icon_size, icon_y)
                glVertex2f(icon_x + icon_size, icon_y + icon_size)
                glVertex2f(icon_x, icon_y + icon_size)
                glEnd()

                # tool name
                self._draw_text(icon_x + icon_size + 8, btn_y + btn_h * 0.6, name, color=text_col)

            # Right: properties pane header
            prop_x = left_w + pad
            prop_w = self.width - prop_x - pad
            prop_header_h = header_h
            self._rounded_rect(prop_x, 0, prop_w, prop_header_h, (0.14, 0.14, 0.14, 1.0))
            self._draw_text(prop_x + pad, 10, "Properties", color=(1, 1, 1, 1))

            # Properties area background
            prop_y_off = prop_header_h + pad
            self._rounded_rect(prop_x, prop_y_off, prop_w, self.height - prop_y_off - pad, (0.10, 0.10, 0.10, 0.9))

            # Render properties for selected tool
            sel_tool = self.tools[self.selected]
            props = self.tool_properties.get(sel_tool, [])

            row_h = 28
            ry = prop_y_off + 8
            label_x = prop_x + pad
            control_x = prop_x + prop_w - 110

            # Title of selected tool
            self._draw_text(label_x, ry - 4, sel_tool, color=(1, 1, 1, 1))
            ry += 22

            for prop in props:
                if ry + row_h > self.height - pad:
                    break  # stop drawing if out of panel

                name = prop[0]
                kind = prop[1]

                # draw label
                self._draw_text(label_x, ry + 8, name, color=(0.9, 0.9, 0.9, 1.0))

                if kind == "Slider":
                    # prop format: (name, "Slider", value, min, max)
                    val = prop[2]
                    vmin = prop[3]
                    vmax = prop[4]
                    t = float(val - vmin) / float(max(1e-6, vmax - vmin))
                    # draw slider track
                    track_x = control_x
                    track_w = 80
                    track_y = ry + 8
                    glColor4f(0.25, 0.25, 0.25, 1.0)
                    glBegin(GL_QUADS)
                    glVertex2f(track_x, track_y - 4)
                    glVertex2f(track_x + track_w, track_y - 4)
                    glVertex2f(track_x + track_w, track_y + 4)
                    glVertex2f(track_x, track_y + 4)
                    glEnd()
                    # knob
                    knob_x = track_x + t * track_w - 6
                    glColor4f(0.85, 0.85, 0.85, 1.0)
                    glBegin(GL_QUADS)
                    glVertex2f(knob_x, track_y - 8)
                    glVertex2f(knob_x + 12, track_y - 8)
                    glVertex2f(knob_x + 12, track_y + 8)
                    glVertex2f(knob_x, track_y + 8)
                    glEnd()

                elif kind == "Checkbox":
                    # prop format: (name, "Checkbox", bool)
                    checked = bool(prop[2])
                    box_size = 14
                    bx = control_x + 20
                    by = ry + 4
                    glColor4f(1, 1, 1, 1) if checked else glColor4f(0.25, 0.25, 0.25, 1)
                    glBegin(GL_QUADS)
                    glVertex2f(bx, by)
                    glVertex2f(bx + box_size, by)
                    glVertex2f(bx + box_size, by + box_size)
                    glVertex2f(bx, by + box_size)
                    glEnd()

                elif kind == "Radio":
                    # prop format: (name, "Radio", [options], idx)
                    options = prop[2]
                    sel_idx = prop[3]
                    opt_x = control_x
                    for i, opt in enumerate(options):
                        dot_x = opt_x + i * 60
                        # circle background
                        glColor4f(0.9, 0.9, 0.9, 1.0) if i == sel_idx else glColor4f(0.3, 0.3, 0.3, 1.0)
                        # draw small square as fake radio
                        glBegin(GL_QUADS)
                        glVertex2f(dot_x, ry + 6)
                        glVertex2f(dot_x + 12, ry + 6)
                        glVertex2f(dot_x + 12, ry + 18)
                        glVertex2f(dot_x, ry + 18)
                        glEnd()
                        self._draw_text(dot_x + 16, ry + 8, opt, color=(0.9, 0.9, 0.9, 1.0))

                elif kind == "Swatch":
                    col = prop[2]
                    sw_x = control_x + 20
                    sw_y = ry + 4
                    glColor4f(*col)
                    glBegin(GL_QUADS)
                    glVertex2f(sw_x, sw_y)
                    glVertex2f(sw_x + 28, sw_y)
                    glVertex2f(sw_x + 28, sw_y + 20)
                    glVertex2f(sw_x, sw_y + 20)
                    glEnd()

                elif kind == "Dropdown":
                    opts = prop[2]
                    sel_idx = prop[3]
                    box_x = control_x
                    box_w = 110
                    glColor4f(0.2, 0.2, 0.2, 1.0)
                    glBegin(GL_QUADS)
                    glVertex2f(box_x, ry + 4)
                    glVertex2f(box_x + box_w, ry + 4)
                    glVertex2f(box_x + box_w, ry + 24)
                    glVertex2f(box_x, ry + 24)
                    glEnd()
                    self._draw_text(box_x + 6, ry + 12, opts[sel_idx], color=(0.95, 0.95, 0.95, 1.0))

                ry += row_h

        finally:
            glPopMatrix()
