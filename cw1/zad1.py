from app import Application
from viewport import Viewport
from window import Window
from drawing import Lines
import random
import pygame
import time
from drawing import Polygon


class MyApp(Application):
    def __init__(self):
        super(MyApp, self).__init__()

    def run(self):
        rekt2 = Polygon((-0.5, -0.5, 0), (0.5, -0.5, 0), (0.5, 0.5, 0), (-0.5, 0.5, 0), colors=[(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)])
        rekt = Polygon((-0.5, -0.5, 0), (0.5, -0.5, 0), (0.5, 0.5, 0), (-0.5, 0.5, 0), colors=[(1,0,0),(0,1,0),(0,0,1),(1,1,1)])
        delta_time = 0
        v_port2 = Viewport(400, 300, 400, 300, 50, 0.001, clear_before_draw=True)
        v_port1 = self.window.viewports[0]
        self.window.viewports = (self.window.viewports[0], v_port2)
        v_port1.camera.look_at_pos = (0.3, 0,0)
        rekt.transform = (0.5, 0.5, 0)
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
            rekt.rotation = (rekt.rotation[0] + 360 * delta_time * rotate, rekt.rotation[1], rekt.rotation[2])
            rekt2.rotation = (rekt2.rotation[0] + 180 * delta_time * rotate, rekt2.rotation[1], rekt2.rotation[2])
            delta_time = time.time() - curr_time


x = MyApp()

x.init()

x.run()
