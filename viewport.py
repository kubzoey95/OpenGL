from OpenGL.GL import *
from OpenGL.GLU import *
from camera import Camera
from drawing import default_scene


class Viewport:

    all_viewports = set()

    def __init__(self, x, y, width, height, zfar, znear, fovy=45, clear_before_draw=False, projection='persp'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zfar = zfar
        self.znear = znear
        self.fovy = fovy
        self.camera = Camera((0, 0, 1), zfar, znear, width / height, fovy)
        self.clear_before_draw = clear_before_draw
        self.projection = projection
        self.all_viewports.add(self)

    @classmethod
    def refresh_all(cls):
        [viewport.view() for viewport in cls.all_viewports]

    def project(self):
        if self.projection == 'persp':
            gluPerspective(45, self.width / self.height, self.znear, self.zfar)
        elif self.projection == 'ortho':
            glOrtho(-self.width / self.height, self.width / self.height, -1, 1, self.znear, self.zfar)
            # glOrtho(0, self.width, self.height, 0, self.znear, self.zfar)

    # def refresh(self):
    #     glScissor(self.x, self.y, self.width, self.height)
    #     glEnable(GL_SCISSOR_TEST)
    #     if self.clear_before_draw:
    #         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #     glMatrixMode(GL_MODELVIEW)
    #     glPushMatrix()
    #     glLoadIdentity()
    #     self.camera.view()
    #     default_scene.draw_all()
    #     glMatrixMode(GL_PROJECTION)
    #     glPushMatrix()
    #     glViewport(self.x, self.y, self.width, self.height)
    #     glLoadIdentity()
    #     self.project()
    #     glMatrixMode(GL_PROJECTION)
    #     glPopMatrix()
    #     glMatrixMode(GL_MODELVIEW)
    #     glPopMatrix()
    #     glDisable(GL_SCISSOR_TEST)

    def refresh(self):
        glScissor(self.x, self.y, self.width, self.height)
        glEnable(GL_SCISSOR_TEST)
        if self.clear_before_draw:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glViewport(self.x, self.y, self.width, self.height)
        glLoadIdentity()
        self.project()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        self.camera.view()
        default_scene.draw_all()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glDisable(GL_SCISSOR_TEST)
