from window import Window
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from viewport import Viewport
from drawing import default_scene
import pygame


class Application:
    def __init__(self, window=Window(800, 600)):
        self.window = window

    def init(self):
        glutInit(sys.argv)
        pygame.init()
        self.window.init()
        glEnable(GL_DEPTH_TEST)

    def draw_all(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.window.refresh()

    def run(self):
        raise NotImplementedError

    # def run_app_loop(self):
    #     while True:
    #         self.draw_all()
    #         self.main_f(pygame.event.get())
    #         pygame.time.wait(1000)

