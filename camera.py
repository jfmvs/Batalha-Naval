import pygame as pg


class Camera:
    def __init__(self, pos, w, h):
        self._position = list(pos)
        self._width  = w
        self._height = h

    def get_rect(self):
        return (
            self.get_pos()[0] - self._width // 2,
            self.get_pos()[1] - self._height // 2,
            self._width, self._height
        )

    def get_pos(self):
        return self._position

    def set_pos(self, x, y):
        self._position[0] = x
        self._position[1] = y

    def get_modeled(self, surface, scale):
        modeled = pg.Surface((self._width, self._height))
        tmp = pg.transform.scale(surface, (
            int(surface.get_width() * scale),
            int(surface.get_height() * scale)
        ))
        modeled.blit(tmp, (0, 0), self.get_rect())
        return modeled