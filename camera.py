from OpenGL.GL import *
from OpenGL.GLU import *


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
        self.look_at_pos and gluLookAt(*self.pos, *self.look_at_pos, *self.up)

    def view(self):
        self.refresh_pos()
        self.look_at()
