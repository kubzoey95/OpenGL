from app import Application
from viewport import Viewport
from window import Window
from drawing import Lines, Composite
import random
import pygame
import time
from drawing import TeaPot
from operator import add, mul
from math import sin, pi, fmod, cos
from OpenGL.GLUT import *


class MyApp(Application):
    def __init__(self):
        self.delta_time = 0
        super(MyApp, self).__init__(window=Window(800,600, mode='glut', window_name='Zapraszam na herbatke:))))'))

    def run(self):
        tpot = TeaPot(color=(0,0,1), solid=False)
        tpots_around = [TeaPot(color=(0,1,0), solid=False) for _ in range(7)]
        for tpt in tpots_around:
            tpt.scale = (0.5, 0.5, 0.5)
        for index, tpt in enumerate(tpots_around):
            tpt.transform = (3*cos(index*(2*pi / len(tpots_around))),0,3*sin(index*(2*pi / len(tpots_around))))

        rotation_times = tuple([random.uniform(-360, 360) for _ in range(len(tpots_around))])

        composite_obj = Composite(*tpots_around)
        composite_rot = random.uniform(-360, 360)

        self.window.viewports[0].camera.pos = (0,1.5,5)
        self.window.viewports.append(Viewport(400,300, 400, 300, 50, 0.001, clear_before_draw=False, projection='persp'))
        self.window.viewports[1].camera.pos = (5, 5, 0)

        def display_func():
            current_time = time.time()
            tpot.rotation = (0,(tpot.rotation[1] + (self.delta_time * 360)) % 360,0)
            # tpots_around[0].rotation = (0,(tpot.rotation[1] + (self.delta_time * 180)) % 360,0)
            for tpt, rotation_time in zip(tpots_around, rotation_times):
                tpt.rotation = (0,(tpt.rotation[1] + (self.delta_time * rotation_time)) % 360,0)
            composite_obj.rotation = (0, composite_obj.rotation[1] + (self.delta_time * composite_rot) % 360,0)
            self.draw_all()
            self.delta_time = time.time() - current_time

        def keyboard_func(*args):
            print(args)

        glutKeyboardFunc(keyboard_func)
        glutDisplayFunc(display_func)

        glutMainLoop()


x = MyApp()

x.init()

x.run()
