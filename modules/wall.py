# code to make the wall object
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class Wall:
    def __init__(self, start, end, width=4.0, color=(0.0, 0.0, 0.0, 1.0)):
        """Start and end are (x, y). Width is in pixels (framebuffer units). Color is RGBA tuple.
        Draws the wall as a filled rectangle (two triangles) so walls have visible thickness.
        """
        self.start = list(start)
        self.end = list(end)
        self.width = float(width)
        self.color = color

    def draw(self):
        x1, y1 = self.start
        x2, y2 = self.end

        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length == 0:
            return

        # perpendicular unit vector
        nx = -dy / length
        ny = dx / length

        half = self.width / 2.0
        ox = nx * half
        oy = ny * half

        # four corners of the wall quad
        p1 = (x1 + ox, y1 + oy)
        p2 = (x1 - ox, y1 - oy)
        p3 = (x2 - ox, y2 - oy)
        p4 = (x2 + ox, y2 + oy)

        glColor4f(*self.color)

        # draw as triangle fan (p1 -> p2 -> p3 -> p4)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(p1[0], p1[1])
        glVertex2f(p2[0], p2[1])
        glVertex2f(p3[0], p3[1])
        glVertex2f(p4[0], p4[1])
        glEnd()

        glFlush()