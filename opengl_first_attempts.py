import pygame
import math
import random
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import glm
import numpy as np


class Camera:
    def __init__(self, pos, zfar, znear, ratio, fovy=45, up=(0, 1, 0), look_at_pos=(0, 0, 0)):
        self.pos = pos
        # self.rot = rot
        self.zfar = zfar
        self.znear = znear
        self.ratio = ratio
        self.fovy = fovy
        self.up = up
        self.look_at_pos = look_at_pos

    def refresh_pos(self):
        glTranslatef(*[-coor for coor in self.pos])
        # glRotatef(*[-coor for coor in self.rot])

    def look_at(self):
        gluLookAt(*self.pos, *self.look_at_pos, *self.up)

    def view(self):
        self.refresh_pos()
        self.look_at()

class Screen:
    def __init__(self, size, camera: Camera):
        self.camera = camera
        self.camera.ratio = size[0] / size[1]
        self.size = size

    def unproject(self, pos):
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        proj = glGetDoublev(GL_PROJECTION_MATRIX)
        mat = np.linalg.inv(np.matmul(modelview, proj))
        vect = np.array((2 * (pos[0] / self.size[0]) - 1, 2 * ((self.size[1] - pos[1]) / self.size[1]) - 1,
                        (2 * (pos[2] - self.camera.znear) / (self.camera.zfar - self.camera.znear)) - 1, 1))
        result = np.matmul(vect, mat)
        result = np.array(result[:3]) / result[3]

        return result

    def apply_default_projection(self):
        gluPerspective(45, self.size[0] / self.size[1], self.camera.znear, self.camera.zfar)


class Viewport:

    all_viewports = set()

    def __init__(self, x, y, width, height, zfar, znear, fovy=45):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zfar = zfar
        self.znear = znear
        self.fovy = fovy
        self.camera = Camera((0, 0, 0), zfar, znear, width / height, fovy)
        self.all_viewports.add(self)

    @classmethod
    def refresh_all(cls):
        [viewport.view() for viewport in cls.all_viewports]

    def view(self):
        glPushMatrix()
        glViewport(self.x, self.y, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective()
        self.camera.view()
        glPopMatrix()


class Window:
    def __init__(self, screen: Screen):
        pygame.init()
        pygame.display.set_mode(screen.size, DOUBLEBUF | OPENGL)

    def refresh(self):
        pygame.display.flip()


verts = (
    ((1,-1,-1), (1,1,-1), (-1,1,-1), (-1,-1,-1), (1,-1,1), (1,1,1), (-1,-1,1), (-1,1,1))
)

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
)

surfs = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
)

colors = [(random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)) for _ in range(5)]

proj = False

def cube_draw():
    global proj
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                glMatrixMode(GL_PROJECTION)
                if proj:
                    gluPerspective(45, 800 / 600, 0.1, 50.0)
                else:
                    glOrtho(-2, 2, -2, 2, 0, 4)
                proj = not proj

    glBegin(GL_QUADS)
    x = 0
    for surf in surfs:
        for vert in surf:
            glColor3fv(colors[x % len(colors)])
            glVertex3fv(verts[vert])
            x += 1
    glEnd()

    glBegin(GL_LINES)
    glColor3fv((0, 0, 1))
    for edge in edges:
        for vert in edge:
            glVertex3f(*verts[vert])
    glEnd()


def draw_rect_moving(step):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    znear = 0.0001
    zfar = 50
    cam = Camera((0,0,7), zfar, znear, display[0] / display[1])
    scr = Screen(display, cam)
    scr.apply_default_projection()
    cam.refresh_pos()
    pygame.display.flip()
    close = False
    rect = [(-1,-1), (1,1)]
    move_vect = (0,0,)
    points = {(0,0,0)}
    mousedown = False
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_vect = (0, move_vect[1])
                if event.key == pygame.K_RIGHT:
                    move_vect = (0, move_vect[1])
                if event.key == pygame.K_DOWN:
                    move_vect = (move_vect[0], 0)
                if event.key == pygame.K_UP:
                    move_vect = (move_vect[0], 0)
                if event.key == pygame.K_SPACE:
                    ff = 0
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                close = True
                break
            if pygame.mouse.get_pressed()[0] or mousedown:
                pos = pygame.mouse.get_pos()
                if pos[0] <= display[0] and pos[1] <= display[1]:
                    result = scr.unproject(pos + (4,))
                    # result = (result[0], result[1], 0)
                    print(result)
                    points.add(tuple(result))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_vect = (move_vect[0] - step, move_vect[1])
                if event.key == pygame.K_RIGHT:
                    move_vect = (move_vect[0] + step, move_vect[1])
                if event.key == pygame.K_DOWN:
                    move_vect = (move_vect[0], move_vect[1] - step)
                if event.key == pygame.K_UP:
                    move_vect = (move_vect[0], move_vect[1] + step)
        # rect = [(rect[0][0] + move_vect[0], rect[0][1] + move_vect[1]), (rect[1][0] + move_vect[0], rect[1][1] + move_vect[1])]
        glTranslatef(-move_vect[0], -move_vect[1], 0)
        if close:
            break
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        perp_rect(*[p for point in rect for p in point])
        glColor3f(0, 1, 0)
        glPointSize(10)

        glBegin(GL_POINTS)
        for point in points:
            glVertex3f(*point)
        glEnd()
        pygame.display.flip()
        # pygame.time.wait(10)


def draw(func=lambda: None, once=False):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    glTranslatef(0, 0, -5)
    func()
    pygame.display.flip()
    close = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                close = True
                break
        if close:
            break
        if not once:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            func()
            pygame.display.flip()
            pygame.time.wait(10)


def draw_i(func=lambda: None, once=False):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    glTranslatef(0, 0, -10)
    func(0)
    pygame.display.flip()
    close = False
    i = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                close = True
                break
        if close:
            break
        if not once:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            func(i)
            pygame.display.flip()
            pygame.time.wait(10)
        i += 1


def draw_triangle_disap(i):
    glBegin(GL_TRIANGLES)
    points = [(0,0), (0,5), (5,0)]
    x = i / 100
    glColor3f(random.uniform(0,math.sin(x)),random.uniform(0,math.sin(x)),random.uniform(0,math.sin(x)))
    for point in points:
            glVertex2f(*point)
    glEnd()


def draw_triangle():
    glBegin(GL_TRIANGLES)
    points = [(0,0), (0,5), (5,0)]
    glColor3f(random.uniform(0,1),random.uniform(0,1),random.uniform(0,1))
    for point in points:
            glVertex2f(*point)
    glEnd()


def draw_line():
    glBegin(GL_LINES)
    points = [(0, 0), (5,5)]
    glColor3f(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
    for point in points:
        glVertex2f(*point)
    glEnd()


def zad1():
    draw_triangle() or cube_draw() or draw_line()


def triangle_strip():
    points = [(-1,-1),(-1,1),(1,-1),(1,1),(2,-1)]
    # val = random.uniform(-1,1)
    # for i in range(30):
    #     points.append((val, random.uniform(-2,2)))
    #     val = random.uniform(val,1)
    glColor3f(0,1,0)
    glLineWidth(4)
    glBegin(GL_TRIANGLE_STRIP)
    for point in points:
        glVertex2f(*point)
    glEnd()


def circle(center, rad):
    pass

def perp_rect(x1,y1,x2,y2):
    glBegin(GL_LINE_LOOP)
    glVertex2f(x1,y1)
    glVertex2f(x1, y2)
    glVertex2f(x2, y2)
    glVertex2f(x2, y1)
    glEnd()

def weird_rects():
    [perp_rect(*[glColor3f(*[random.uniform(0,1) for _ in range(3)]) or random.uniform(-5, 5) for _ in range(4)]) for _ in range(50)]

def triangle_fan(angle, subdivs, center, radius):
    points = [center]
    curr_angle = 0
    for i in range(subdivs + 1):
        points.append((center[0] + radius * math.cos(curr_angle), center[1] + radius * math.sin(curr_angle)))
        curr_angle += angle / subdivs
    glBegin(GL_TRIANGLE_FAN)
    for point in points:
        glColor3f(*[random.uniform(0,1) for _ in range(3)])
        glVertex2f(*point)
    glEnd()

def spiral(center, begin_angle, end_angle, begin_rad, end_rad, steps):
    curr_radius = begin_rad
    curr_angle = begin_angle
    angle_diff = (end_angle - begin_angle) / steps
    rad_diff = (end_rad - begin_rad) / steps
    points = []
    for i in range(steps + 1):
        points.append((center[0] + curr_radius * math.cos(curr_angle), center[1] + curr_radius * math.sin(curr_angle)))
        curr_radius += rad_diff
        curr_angle += angle_diff

    glBegin(GL_POINTS)
    for point in points:
        glColor3f(*[random.uniform(0, 1) for _ in range(3)])
        glVertex2f(*point)
    glEnd()

# def main():
#     pygame.init()
#     display = (800,600)
#     pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
#     gluPerspective(45, display[0] / display[1], 0.1, 50.0)
#
#     glTranslatef(0,0,-5)
#
#     glRotatef(0,0,0,0)
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#         glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
#         cube_draw()
#         pygame.display.flip()
#         glRotatef(0.5, 1,0,1)
#         # glTranslatef(0, 0, -0.1)
#         pygame.time.wait(10)

# main()