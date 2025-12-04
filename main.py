# start the program and prereq
import glfw
from OpenGL.GL import *

from modules.floorManager import *
from modules.wall import *
from modules.guiManager import *


test_floormanager = FloorManager((800, 800))
test_floormanager.add_new_floor()

test_guimanager = guiManager()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 600, "openArchitect", None, None)

    if not window:
        glfw.terminate()
        return
    
    
    glfw.make_context_current(window)
    glutInit(sys.argv)

    # set up 2D orthographic projection and resize callback
    fb_width, fb_height = glfw.get_framebuffer_size(window)
    set_2d_projection(fb_width, fb_height)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    while not glfw.window_should_close(window):
        ## RENDERING HANDLER ##
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.77, 0.77, 0.77, 1)
        

        # first draw the grid and stuff for drawing

        test_floormanager.draw()

        # next, draw the ui in order of clicked

        test_guimanager.draw()

        ## EVENT HANDLING ##
        glfw.poll_events()


        ## SWAP BUFFERS ## (no clue what this does)
        glfw.swap_buffers(window)
    

    # ask to save and then terminate
    glfw.terminate()

def set_2d_projection(width, height):
    """Configure a simple orthographic projection for 2D rendering.
    Coordinates will be: x -> [0..width], y -> [0..height] with origin at top-left.
    """
    # make sure viewport matches framebuffer size
    glViewport(0, 0, width, height)

    # set projection matrix to orthographic
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # left, right, bottom, top, near, far
    # use top=0 so Y increases downwards (convenient for UI coordinates)
    glOrtho(0, width, height, 0, -1, 1)

    # switch back to modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # For 2D UI, disable depth testing and enable blending for transparency
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def framebuffer_size_callback(window, width, height):
    # When the framebuffer is resized, update viewport and projection
    set_2d_projection(width, height)

if __name__ == "__main__":
    main()