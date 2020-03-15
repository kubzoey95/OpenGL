from app import Application
from viewport import Viewport
from window import Window
from drawing import Lines
import random
import pygame
import time
from drawing import CubeZWykladu
from operator import add, mul
from math import sin, pi, fmod


class MyApp(Application):
    def __init__(self):
        super(MyApp, self).__init__(
            window=Window(800, 600, window_name='kostka,sterowanie strzalkami (strzalki trzeba klikac za kazdym razem), p zmienia perspektywe'))

    def run(self):
        rekt2 = CubeZWykladu()
        delta_time = 0
        # v_port2 = Viewport(400, 300, 400, 300, 50, 0.001, clear_before_draw=True)
        v_port1 = self.window.viewports[0]
        # self.window.viewports = (self.window.viewports[0], v_port2)
        # v_port1.camera.look_at_pos = (0.3, 0,0)
        rotate = True
        proj = ('persp', 'ortho')
        proj_iterator = 0
        move_vect = (0, 0, 0)
        while True:
            curr_time = time.time()
            self.draw_all()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        proj_iterator = (proj_iterator + 1) % 2
                        v_port1.projection = proj[proj_iterator]
                    if event.key == pygame.K_LEFT:
                        move_vect = (-delta_time / 2, 0, 0)
                    if event.key == pygame.K_RIGHT:
                        move_vect = (delta_time / 2, 0, 0)
                    if event.key == pygame.K_DOWN:
                        move_vect = (0, -delta_time / 2, 0)
                    if event.key == pygame.K_UP:
                        move_vect = (0, delta_time / 2, 0)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        move_vect = (0, move_vect[1], 0)
                    if event.key == pygame.K_RIGHT:
                        move_vect = (0, move_vect[1], 0)
                    if event.key == pygame.K_DOWN:
                        move_vect = (move_vect[0], 0, 0)
                    if event.key == pygame.K_UP:
                        move_vect = (move_vect[0], 0, 0)
                v_port1.camera.pos = tuple(map(add, v_port1.camera.pos, move_vect))
            delta_time = time.time() - curr_time

def main():
    x = MyApp()

    x.init()

    x.run()
