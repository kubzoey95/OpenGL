from opengl_first_attempts import *


def main():
    draw_i(lambda i: draw_triangle() or cube_draw() or draw_line() or glRotatef(i / 100,0,1,0))

