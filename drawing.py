from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import squaternion


class Scene:
    def __init__(self):
        self.objects = set()

    def draw_all(self):
        [object.draw_apply_transform() for object in self.objects]

    def add_object(self, object):
        self.objects.add(object)


default_scene = Scene()


class Drawing:
    def __init__(self, scene=default_scene, transform=(0,0,0), rotation=(0,0,0), scale=(1,1,1)):
        self.scenes = [scene]
        self.scenes[0].add_object(self)
        self.transform = transform
        self.rotation = rotation
        self.scale = scale
        self.parent = scene

    def draw_apply_transform(self):
        glPushMatrix()
        quat_rot = squaternion.euler2quat(*self.rotation, True)
        glTranslatef(*self.transform)
        rot_angle = np.degrees(2 * np.arccos(quat_rot.w))
        square_coef = np.sqrt(1 - np.square(quat_rot.w))
        if rot_angle > 0.001 and square_coef > 0.001:
            rot_x = quat_rot.x / square_coef
            rot_y = quat_rot.y / square_coef
            rot_z = quat_rot.z / square_coef
            glRotatef(rot_angle, rot_x, rot_y, rot_z)
        glScalef(*self.scale)
        self.draw()
        glPopMatrix()

    def draw(self):
        raise NotImplementedError


class PointsStream(Drawing):

    def __init__(self, points, scene=default_scene):
        self.points = points
        super(self.__class__, self).__init__(scene)

    def draw(self):
        glBegin(GL_POINTS)
        for point in self.points:
            glVertex3f(*point)
        glEnd()


class Lines(Drawing):
    def __init__(self, *points, colors=tuple(), scene=default_scene):
        self.points = points
        self.colors = colors
        super(self.__class__, self).__init__(scene)

    def draw(self):
        color_gen = (glColor3f(*color) for color in (self.colors if self.colors else []))

        def iterator():
            try:
                next(color_gen)
            except StopIteration:
                pass

        glBegin(GL_LINES)
        for point in self.points:
            iterator()
            glVertex3f(*point)
        glEnd()


class Rectangle(Drawing):
    def __init__(self, x1, y1, x2, y2, scene=default_scene):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        super(self.__class__, self).__init__(scene)

    def draw(self):
        glRectf(self.x1, self.y1, self.x2, self.y2)


class Polygon(Drawing):
    def __init__(self, *points, colors=None, scene=default_scene):
        self.points = points
        self.colors = colors
        super(self.__class__, self).__init__(scene)

    def draw(self):
        glBegin(GL_POLYGON)
        if self.colors is None:
            for point in self.points:
                glVertex3f(*point)
        else:
            for point, color in zip(self.points, self.colors):
                glColor3f(*color)
                glVertex3f(*point)
        glEnd()


class Triangles(Drawing):
    def __init__(self, *points, colors=None, scene=default_scene):
        self.points = points
        self.colors = colors
        super(self.__class__, self).__init__(scene)

    def draw(self):
        glBegin(GL_TRIANGLES)
        if self.colors:
            for point, color in zip(self.points, self.colors):
                glColor3f(*color)
                glVertex3f(*point)
        else:
            for point in self.points:
                glVertex3f(*point)

        glEnd()


class CubeZWykladu(Drawing):
    def __init__(self, scene=default_scene):
        super(self.__class__, self).__init__(scene)

    def draw(self):
        glBegin(GL_LINE_LOOP)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glEnd()

        glBegin(GL_LINE_LOOP)
        glColor3f(1.0, 0.5, 0.0)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glEnd()

        glBegin(GL_LINE_LOOP)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glEnd()

        glBegin(GL_LINE_LOOP)
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glEnd()

        glBegin(GL_LINE_LOOP)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glEnd()

        glBegin(GL_LINE_LOOP)
        glColor3f(0.5, 0.0, 0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glEnd()


class TeaPot(Drawing):
    def __init__(self, size=1, color=None, solid=True, scene=default_scene):
        self.solid = solid
        self.size = size
        self.color = color
        super(self.__class__, self).__init__(scene)

    def draw(self):
        if self.color:
            glColor3f(*self.color)
        if self.solid:
            glutSolidTeapot(self.size)
        else:
            glutWireTeapot(self.size)


class Composite(Drawing):
    def __init__(self, *objects, scene=default_scene):
        super(self.__class__, self).__init__(scene)
        for object in objects:
            for scene in object.scenes:
                scene.objects.remove(object)
            object.scenes = [default_scene]
            object.parent = self
        self.objects = objects

    def draw(self):
        for object in self.objects:
            object.draw_apply_transform()


class Cube(Drawing):
    def __init__(self, colors=None, scene=default_scene):
        self.colors = colors
        super(self.__class__, self).__init__(scene)

    def draw(self):
        color_gen = (glColor3f(*color) for color in (self.colors if self.colors else []))

        def iterator():
            try:
                next(color_gen)
            except StopIteration:
                pass

        glBegin(GL_QUADS)

        iterator()
        glVertex3f(-1, 1, 1)
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)

        iterator()
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, 1, -1)

        iterator()
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, 1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 1, -1)

        iterator()
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, -1, -1)

        iterator()
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1, 1)
        glVertex3f(-1, 1, 1)

        iterator()
        glVertex3f(1, 1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)
        glEnd()
