# start the program and prereq
import glfw
import sys
from OpenGL.GL import *

from modules.drawManager import *

draw_manager = drawManager()

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

    # forward GLFW mouse events into our GUI system (convert to framebuffer coords)
    def _window_to_framebuffer(x, y):
        # glfw cursor positions are in window coordinates; convert to framebuffer pixels
        fb_w, fb_h = glfw.get_framebuffer_size(window)
        win_w, win_h = glfw.get_window_size(window)
        if win_w == 0 or win_h == 0:
            return int(x), int(y)
        sx = fb_w / float(win_w)
        sy = fb_h / float(win_h)
        return int(x * sx), int(y * sy)

    def mouse_button_cb(win, button, action, mods):
        cx, cy = glfw.get_cursor_pos(win)
        fb_x, fb_y = _window_to_framebuffer(cx, cy)
        event = {'type': 'mouse_button', 'x': fb_x, 'y': fb_y, 'button': button, 'action': action}
        try:
            draw_manager.send_events(event)
        except Exception:
            pass

    def cursor_pos_cb(win, xpos, ypos):
        fb_x, fb_y = _window_to_framebuffer(xpos, ypos)
        event = {'type': 'mouse_move', 'x': fb_x, 'y': fb_y}
        try:
            draw_manager.send_events(event)
        except Exception:
            pass

    glfw.set_mouse_button_callback(window, mouse_button_cb)
    glfw.set_cursor_pos_callback(window, cursor_pos_cb)

    while not glfw.window_should_close(window):
        ## RENDERING HANDLER ##
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.77, 0.77, 0.77, 1)
        

        # tell drawmanager to draw all
        draw_manager.draw()

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