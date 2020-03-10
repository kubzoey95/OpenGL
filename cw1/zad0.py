from app import Application
from viewport import Viewport
from window import Window
from drawing import Lines
import random
import pygame
import time
from drawing import Triangles
from operator import add, mul
from math import sin, pi, fmod


class MyApp(Application):
    def __init__(self):
        super(MyApp, self).__init__()

    def run(self):
        rekt2 = Triangles((-0.5, -0.5, 0), (0.5, -0.5, 0), (0.5, 0.5, 0), colors=[(1, 0, 0), (0, 1, 0), (0, 0, 1)])
        delta_time = 0
        v_port2 = Viewport(400, 300, 400, 300, 50, 0.001, clear_before_draw=True)
        v_port1 = self.window.viewports[0]
        self.window.viewports = (self.window.viewports[0], v_port2)
        v_port1.camera.look_at_pos = (0.3, 0,0)
        rotate = True
        tme = 0
        colors = rekt2.colors
        while True:
            tme = fmod(tme + (delta_time * 2*pi * rotate), 2*pi)
            curr_time = time.time()
            self.draw_all()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        rotate = not rotate
            print(colors)
            print(rekt2.colors)
            rekt2.colors = tuple([tuple(map(mul, color, ((sin(tme) + 1) / 2, ) * len(color))) for color in colors])
            delta_time = time.time() - curr_time


x = MyApp()

x.init()

x.run()
