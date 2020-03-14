from app import Application
from viewport import Viewport
from window import Window
from drawing import Lines, Composite, Cube
import random
import pygame
import time
from drawing import TeaPot
from operator import add, mul
from math import sin, pi, fmod, cos
from OpenGL.GLUT import *
import numpy as np
from ctypes import c_int


class MyApp(Application):
    def __init__(self):
        self.delta_time = 0
        super(MyApp, self).__init__(window=Window(800,600, mode='glut', window_name='Szescianki a co ??'))

    def run(self):
        colors = ((1,0,0), (0,1,0), (0,0,1), (0,1,1), (1,1,0), (1,1,1))
        qb_cen = Cube(colors)
        qb_cen.scale = (0.5, 0.5, 0.5)

        self.window.viewports[0].camera.pos = (0,0,0)
        self.window.viewports[0].camera.look_at_pos = None
        scale = 3

        qbs = [Cube(colors) for _ in range(6)]
        points = ((1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1),(0,0,-1))
        for qb, trans in zip(qbs, points):
            qb.transform = tuple(map(lambda itm: itm * scale, trans))

        lines = Lines(*[elem for point in points for elem in [(0,0,0), tuple(map(lambda itm: itm * scale, point))]], colors=((0,1,0), ))
        line = Lines((0,0,0), (0,0,0), colors=((0,0,1),))
        rots = [random.uniform(0, 360) for _ in range(3)]
        self.window.viewports[0].camera.transform = (0,0,10)
        glutWarpPointer(int(glutGet(GLUT_WINDOW_X) + glutGet(GLUT_WINDOW_WIDTH) / 2),
                        int(glutGet(GLUT_WINDOW_Y) + glutGet(GLUT_WINDOW_HEIGHT) / 2))
        def display_func():
            current_time = time.time()
            for qb, trans in zip(qbs, points):
                qb.rotation = tuple(map(add, qb.rotation, map(mul, trans, map(lambda itm: itm * self.delta_time, rots))))

            movement_x = self.keys.get(b'd', 0) - self.keys.get(b'a', 0)
            movement_y = -self.keys.get(b'w', 0) + self.keys.get(b's', 0)
            self.window.viewports[0].camera.move_forward(self.delta_time * 5 * movement_y)
            self.window.viewports[0].camera.move_left(self.delta_time * 5 * movement_x)
            self.draw_all()
            self.delta_time = time.time() - current_time

        self.keys = dict()

        def keyboard_func(key, x, y):
            self.keys[key] = True

        def keyboard_up_func(key, x, y):
            self.keys[key] = False

        self.btn_clicked = False
        self.mouse_pos = (0,0)
        self.mouse_rot = (0,0, 0)
        self.window.viewports[0].camera.look_at_pos = None

        def mouse_button_func(button, state, x, y):
            if button == GLUT_LEFT_BUTTON:
                self.mouse_pos = (x,y)
                # print(self.mouse_pos)
                self.btn_clicked = not state

        def motion(x, y):
            self.mouse_rot = ((x-int(glutGet(GLUT_WINDOW_WIDTH) / 2)) * self.delta_time * self.btn_clicked * 50,(int(glutGet(GLUT_WINDOW_HEIGHT) / 2)-y) * self.delta_time * self.btn_clicked * 50)
            self.window.viewports[0].camera.rot_xy = tuple(map(lambda itm1, itm2: (itm1 + itm2) % 360, self.window.viewports[0].camera.rot_xy, self.mouse_rot))
            print(x,y)
            glutWarpPointer(int(glutGet(GLUT_WINDOW_WIDTH) / 2),
                            int(glutGet(GLUT_WINDOW_HEIGHT) / 2))

        glutMotionFunc(motion)
        glutMouseFunc(mouse_button_func)
        glutKeyboardFunc(keyboard_func)
        # glutSpecialFunc()
        glutKeyboardUpFunc(keyboard_up_func)
        glutDisplayFunc(display_func)

        glutMainLoop()


x = MyApp()

x.init()

x.run()
