import pygame
from pygame.locals import *
from viewport import Viewport
from OpenGL.GLUT import *
from OpenGL.GL import *



class Window:
    all_windows = set()

    def __init__(self, *size, viewports=(Viewport(0, 0, 800, 600, 50, 0.001),), mode='pygame', **kwargs):
        self.x = size[0]
        self.y = size[1]
        self.viewports = viewports
        self.mode = mode
        self.additional_options = kwargs
        self.all_windows.add(self)

    @classmethod
    def refresh_all(cls):
        [window.refresh() for window in cls.all_windows]

    def refresh_viewports(self):
        [viewport.refresh() for viewport in self.viewports]

    def refresh(self, wait=10):
        self.refresh_viewports()
        if self.mode == 'pygame':
            pygame.display.flip()
            pygame.time.wait(wait)
        if self.mode == 'glut':
            glutSwapBuffers()
            glutPostRedisplay()
            glFlush()

    def init(self):
        if self.mode == 'pygame':
            pygame.display.set_mode((self.x, self.y), DOUBLEBUF | OPENGL)
        elif self.mode == 'glut':
            glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
            glutInitWindowSize(self.x, self.y)
            glutCreateWindow(b"%s" % str.encode(self.additional_options.get('window_name')))
