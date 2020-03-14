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
        quat_rot = squaternion.euler2quat(self.rot_xy[1], self.rot_xy[0], 0, True)
        rot_angle = np.degrees(2 * np.arccos(quat_rot.w))
        square_coef = np.sqrt(1 - np.square(quat_rot.w))
        if rot_angle > 0.001 and square_coef > 0.001:
            rot_x = quat_rot.x / square_coef
            rot_y = quat_rot.y / square_coef
            rot_z = quat_rot.z / square_coef
            glRotatef(rot_angle, rot_x, rot_y, rot_z)
        glTranslatef(*[-coor for coor in self.transform])
        glTranslatef(*[-coor for coor in self.pos])

    def look_at(self):
        self.look_at_pos and gluLookAt(*self.pos, *self.look_at_pos, *self.up)

    def move_forward(self, amount):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        self.view()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        forward_normalized = self.front_vector / np.linalg.norm(self.front_vector)
        self.transform = tuple(np.array(self.transform) + (forward_normalized * amount))

    def move_left(self, amount):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        self.view()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        left_normalized = self.left_vector / np.linalg.norm(self.left_vector)
        self.transform = tuple(np.array(self.transform) + (left_normalized * amount))

    def view(self):
        self.look_at()
        self.refresh_pos()
        self.view_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.left_vector = self.view_matrix[:3, 0]
        self.up_vector = self.view_matrix[:3, 1]
        self.front_vector = self.view_matrix[:3, 2]
        self.relative_transform = self.view_matrix[:3, 3]
