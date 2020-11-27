import sys
import pygame as pg
from pygame import gfxdraw


class Player:
    def __init__(self, pos, speed=250, angle=0):
        self._position      = pg.Vector2(*pos)
        self._speed         = speed
        self._angle         = angle
        self._sprite        = pg.image.load('assets/player.png').convert_alpha()
        self._sprite        = pg.transform.scale(self._sprite, (120, 20))

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
        return self._position.x, self._position.y

    def draw(self, surface):
        modeled = pg.transform.flip(self._sprite, True, False)
        modeled = pg.transform.rotate(modeled, -self._angle)
        coords = (self._position.x - modeled.get_width() // 2, self._position.y - modeled.get_height() // 2)
        surface.blit(modeled, coords)

        if '-o' not in sys.argv:
            length    = 40
            coord1 = self._position.x, self._position.y
            coord2 = int(coord1[0] + self.direction.x * length), int(coord1[1] + self.direction.y * length)
            coord1 = int(coord1[0]), int(coord1[1])
            pg.gfxdraw.line(surface, *coord1, *coord2, (223, 32, 203))

