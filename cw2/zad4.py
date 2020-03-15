from app import Application
from viewport import Viewport
from window import Window
from drawing import ChessTable, Cube, TeaPot
import random
import pygame
import time
from drawing import TeaPot
from operator import add, mul
from math import sin, pi, fmod, cos
from OpenGL.GLUT import *
import numpy as np


class MyApp(Application):
    def __init__(self):
        self.delta_time = 0
        super(MyApp, self).__init__(window=Window(800,600, mode='glut', window_name='Lokalny imbryczek jezdzi sb po szachownicy, sterowanie wsad'))

    def run(self):
        colors = ((1,0,0), (0,1,0), (0,0,1), (0,1,1), (1,1,0), (1,1,1))
        szach = ChessTable((2, 2), (20, 20))
        imbrk = TeaPot(color=(1,0,0), solid=False)
        # colors = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1), (1, 1, 0), (1, 1, 1))
        # imbrk = Cube(colors)
        # colors = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1), (1, 1, 0), (1, 1, 1))
        # qb_cen = Cube(colors)
        # qb_cen.transform = (6,1,6)
        imbrk.transform = (8,1,8)
        # szach.transform = (0,0,0)
        self.window.viewports[0].zfar = 100
        self.window.viewports[0].camera.pos = (0,0,0)
        self.window.viewports[0].camera.transform = (20,10,20)
        self.window.viewports[0].camera.look_at_pos = (9,1,8)
        self.window.viewports[0].camera.rot_xy = None

        self.keys = dict()

        def keyboard_func(key, x, y):
            self.keys[key] = True

        def keyboard_up_func(key, x, y):
            self.keys[key] = False

        def display_func():
            current_time = time.time()
            movement_x = -self.keys.get(b'd', 0) + self.keys.get(b'a', 0)
            movement_y = -self.keys.get(b'w', 0) + self.keys.get(b's', 0)
            imbrk.rotation = tuple((np.array(imbrk.rotation) + (np.array([0,1,0]) * movement_x * self.delta_time * 60)) % 360)
            imbrk.transform = tuple(np.array(imbrk.transform) - imbrk.left_vector * movement_y * self.delta_time * 5)
            self.window.viewports[0].camera.look_at_pos = imbrk.transform
            # imbrk.transform = self.window.viewports[0].camera.transform
            self.draw_all()
            self.delta_time = time.time() - current_time



        # def motion(x, y):
        #     self.mouse_rot = ((x-int(glutGet(GLUT_WINDOW_WIDTH) / 2)) * self.delta_time * self.btn_clicked * 50,(int(glutGet(GLUT_WINDOW_HEIGHT) / 2)-y) * self.delta_time * self.btn_clicked * 50)
        #     self.window.viewports[0].camera.rot_xy = tuple(map(lambda itm1, itm2: (itm1 + itm2) % 360, self.window.viewports[0].camera.rot_xy, self.mouse_rot))
        #     print(x,y)
        #     glutWarpPointer(int(glutGet(GLUT_WINDOW_WIDTH) / 2),
        #                     int(glutGet(GLUT_WINDOW_HEIGHT) / 2))

        # glutMotionFunc(motion)
        # glutMouseFunc(mouse_button_func)
        glutKeyboardFunc(keyboard_func)
        # # glutSpecialFunc()
        glutKeyboardUpFunc(keyboard_up_func)
        glutDisplayFunc(display_func)

        glutMainLoop()


def main():
    x = MyApp()

    x.init()

    x.run()
