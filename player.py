import pygame as pg


class Player:
    def __init__(self, pos, speed=250, angle=0, size=50):
        self._position      = pg.Vector2(*pos)
        self._speed         = speed
        self._angle         = angle
        self._size          = size

    def update(self, dt):
        direction = pg.Vector2(1.0, 0.0)
        direction.rotate_ip(self._angle)
        self._position += direction * self._speed * dt

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

