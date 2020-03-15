from app import Application
from viewport import Viewport
from window import Window
from drawing import Lines
import random
import pygame
import time
from drawing import Polygon
from operator import add


class MyApp(Application):
    def __init__(self):
        super(MyApp, self).__init__()

    def run(self):
        rekt1 = Polygon((-0.25, -0.25, 0), (0.25, -0.25, 0), (0.25, 0.25, 0), (-0.25, 0.25, 0), colors=[(1,0,0),(0,1,0),(0,0,1),(1,1,1)])
        rekt2 = Polygon((-0.25, -0.25, 0), (0.25, -0.25, 0), (0.25, 0.25, 0), (-0.25, 0.25, 0),
                        colors=[(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)])
        rekt3 = Polygon((-0.25, -0.25, 0), (0.25, -0.25, 0), (0.25, 0.25, 0), (-0.25, 0.25, 0),
                        colors=[(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)])
        rekt4 = Polygon((-0.25, -0.25, 0), (0.25, -0.25, 0), (0.25, 0.25, 0), (-0.25, 0.25, 0),
                        colors=[(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)])
        rekt1.transform = (-0.5, 0.5, 0)
        rekt2.transform = (0.5, 0.5, 0)
        rekt3.transform = (0.5, -0.5, 0)
        rekt4.transform = (-0.5, -0.5, 0)
        delta_time = 0
        v_port2 = Viewport(400, 300, 400, 300, 50, 0.001, clear_before_draw=False)
        v_port1 = self.window.viewports[0]
        self.window.viewports = (self.window.viewports[0], v_port2)
        v_port1.camera.pos = (0,0,2)
        v_port1.camera.look_at_pos = (0.3, 0,0)
        rotate = True
        while True:
            curr_time = time.time()
            print('time', delta_time)
            self.draw_all()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        rotate = not rotate
            rekt1.rotation = tuple(map(add, rekt1.rotation, (0,0, 90 * delta_time * rotate)))
            rekt2.rotation = tuple(map(add, rekt2.rotation, (0, 0, 180 * delta_time * rotate)))
            rekt3.rotation = tuple(map(add, rekt3.rotation, (0, 0, 50 * delta_time * rotate)))
            rekt4.rotation = tuple(map(add, rekt4.rotation, (0, 0, 360 * delta_time * rotate)))
            delta_time = time.time() - curr_time

def main():
    x = MyApp()

    x.init()

    x.run()

