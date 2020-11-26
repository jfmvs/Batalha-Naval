import sys
import pygame as pg
from pygame import gfxdraw


class Player:
    def __init__(self, pos, speed=250, angle=0, size=50):
        self._position      = pg.Vector2(*pos)
        self._speed         = speed
        self._angle         = angle
        self._size          = size

    @property
    def direction(self):
        direction = pg.Vector2(1.0, 0.0)
        direction.rotate_ip(self._angle)
        return direction

    def update(self, dt):
        self._position += self.direction * self._speed * dt

    def rotate(self, dt, angle):
        self._angle += angle * dt
        self._angle = self._angle % 360

    def get_angle(self):
        return self._angle

    def get_pos(self):
        return self._position

    def get_center(self):
        return self._position.x + self._size // 2, self._position.y + self._size // 2

    def draw(self, surface):
        pg.draw.rect(surface, (0,255,0), [self._position.x, self._position.y, self._size, self._size])

        if '-o' not in sys.argv:
            length    = 40
            coord1 = self.get_center()
            coord2 = int(coord1[0] + self.direction.x * length), int(coord1[1] + self.direction.y * length)
            coord1 = int(coord1[0]), int(coord1[1])
            pg.gfxdraw.line(surface, *coord1, *coord2, (223, 32, 203))

