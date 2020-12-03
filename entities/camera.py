import pygame as pg
from .navios import Ship


class Camera:
    def __init__(self, pos: (list, tuple), size, zoom=1.0, speed=150):
        self._position = pg.Vector2(pos)
        self._zoom     = zoom
        self._speed    = speed
        self.width, self.height = size

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position.x = value[0]
        self._position.y = value[1]

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value: float):
        if value > Camera._ZOOM_MAX:
            self._zoom = Camera._ZOOM_MAX
        elif value < Camera._ZOOM_MIN:
            self._zoom = Camera._ZOOM_MIN
        else:
            self._zoom = value

    def zoom_in(self):
        self.zoom += 0.01

    def zoom_out(self):
        self.zoom -= 0.01

    def center(self, target: Ship):
        self._position = target.position