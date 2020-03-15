from opengl_first_attempts import *
import json


def main():
    x = input('[center (lista dwuelem), begin_angle (radiany), end_angle (radiany), begin_rad (float), end_rad (float), steps (int)], prosze podac tak jak by sie liste podawalo, np: [[0, 0], 0, 10, 0, 0.5, 100]')
    x = json.loads(x)
    draw(lambda: spiral(*x), once=False)

