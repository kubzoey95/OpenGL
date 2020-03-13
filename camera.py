from OpenGL.GL import *
from OpenGL.GLU import *
import squaternion
import numpy as np
from operator import add
import glm


class Camera:
    def __init__(self, pos, zfar, znear, ratio, fovy=45, up=(0, 1, 0), look_at_pos=(0, 0, 0), rot_xy = (0,0), transform=(0,0,0)):
        self.pos = pos
        self.real_pos = pos
        # self.rot = rot
        self.zfar = zfar
        self.znear = znear
        self.ratio = ratio
        self.fovy = fovy
        self.up = up
        self.look_at_pos = look_at_pos
        self.rot_xy = rot_xy
        self.transform = transform
        self.view_matrix = None
        self.left_vector = np.array([1,0,0])
        self.up_vector = np.array([0,1,0])
        self.front_vector = np.array([0,0,1])
        self.relative_transform = np.array([0,0,0])

    def refresh_pos(self):
        glRotatef(self.rot_xy[0], 0, 1, 0)
        glRotatef(-self.rot_xy[1], 1, 0, 0)
        glTranslatef(*[-coor for coor in self.transform])
        glTranslatef(*[-coor for coor in self.pos])
        print(np.array(self.transform) + np.array(self.pos))

    def look_at(self):
        self.look_at_pos and gluLookAt(*self.pos, *self.look_at_pos, *self.up)

    def translate_vector_in_direction(self, vect):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        self.view()
        translated_vector = np.matmul(self.view_matrix.transpose(), vect.transpose())
        glPopMatrix()
        return translated_vector

    def move_in_direction(self, direction):
        self.transform = tuple(self.translate_vector_in_direction(direction).transpose()[:3])
        print(self.transform)

    def view(self):
        self.look_at()
        self.refresh_pos()
        self.view_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        print('matr', self.view_matrix)
        self.left_vector = self.view_matrix[:3, 0]
        self.up_vector = self.view_matrix[:3, 1]
        self.front_vector = self.view_matrix[:3, 2]
        self.relative_transform = self.view_matrix[:3, 3]

        # tran = self.left_vector * self.relative_transform[0] + self.up_vector * self.relative_transform[1] + self.front_vector * self.relative_transform[2]

        print('tran', np.matmul(self.view_matrix[3, :3], self.view_matrix[:3,:3]))
        print('transform', np.array(self.pos) + np.array(self.transform))

