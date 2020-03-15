from opengl_first_attempts import *
import json


def main():
    x = input('[angle (w radianach), subdivs (int), center (lista dwuelem), radius (float)], prosze podac tak jak by sie liste podawalo, np: "[2, 10, [0, 0], 0.5]"')
    x = json.loads(x)
    draw(lambda: triangle_fan(*x), once=False)
