# manages showing floors and switching between them

from modules.floor import Floor
from modules.wall import Wall

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math


class FloorManager:
    def __init__(self, size, pos = (0,0), zoom = 1, gridlinesEnabled = True):
        self.floors = []
        self.current_floor = -1
        self.draw_gridlines = gridlinesEnabled
        self.gridlines_cache = []
        self.width, self.height = size
        self.x, self.y = pos
        self.zoom = zoom
    
    def draw(self):
        # draw drawing surface here with a white rect with size self.width, self.height and offset by position. leave room to account for zoom
        self.draw_surface()
        # draw gridlines here using wall function.
        if self.gridlines_cache==[]:
            self.make_gridlines(resolution = 50) # 10 px between gridlines
        else:
            for line in self.gridlines_cache: # eventually add culling? maybe.
                line.draw()

        if self.current_floor != -1: # check. -1 means all are hidden.


            if hasattr(self.floors[self.current_floor], "draw"):
                self.floors[self.current_floor].draw()
            else:
                print("No draw function.")

    def add_existing_floor(self, floor):
        self.floors.append(floor) # add the floor to the floors.
        self.current_floor = len(self.floors)-1 # set to the just added floor. TAKE OUT LATER NERD!!!!!

    def add_new_floor(self, special_data = {}):
        # format special data eventually.
        self.floors.append(Floor(len(self.floors)+1)) # set the floor number to be the current length of self.floors
        self.current_floor = len(self.floors) -1

    def add_object_to_current_floor(self, object):
        # Adds an object to the current floor.
        current = self.floors[self.current_floor]
        current.add_object(object)

    def make_gridlines(self, resolution):
        for x in range(self.width//resolution):
            self.gridlines_cache.append(Wall((0, (x+1)*resolution), (self.width, (x+1)*resolution), 1, (0.5,0.5,0.5,1)))
        for y in range(self.width//resolution):
            self.gridlines_cache.append(Wall(((y+1)*resolution, 0), ((y+1)*resolution, self.height), 1, (0.5,0.5,0.5,1)))

    def draw_surface(self):
        # Draw the drawing surface background at position (self.x, self.y)
        # and scaled by self.zoom. Uses framebuffer/pixel coordinates because
        # main.py sets an orthographic projection matching the framebuffer.
        glPushMatrix()
        try:
            # apply translation and zoom
            glTranslatef(self.x, self.y, 0.0)
            glScalef(self.zoom, self.zoom, 1.0)

            # background (white)
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glBegin(GL_QUADS)
            glVertex2f(0.0, 0.0)
            glVertex2f(self.width, 0.0)
            glVertex2f(self.width, self.height)
            glVertex2f(0.0, self.height)
            glEnd()

            # border (thin, semi-contrast)
            glColor4f(0.0, 0.0, 0.0, 1.0)
            glLineWidth(1.0)
            glBegin(GL_LINE_LOOP)
            glVertex2f(0.0, 0.0)
            glVertex2f(self.width, 0.0)
            glVertex2f(self.width, self.height)
            glVertex2f(0.0, self.height)
            glEnd()
        finally:
            glPopMatrix()
