import pygame as pg
from .navios import Ship


class Camera:
    def __init__(self, pos: (list, tuple), size, speed=150):
        self._position = pg.Vector2(pos)
        self._speed    = speed
        self.width, self.height = size

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position.x = value[0]
        self._position.y = value[1]

    def center(self, target: Ship):
        self._position = target.position
