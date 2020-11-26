import pygame as pg


class Camera:

    _ZOOM_MIN = 0.3
    _ZOOM_MAX = 2.0

    def __init__(self, pos, w, h):
        self._position = list(pos)
        self._width    = w
        self._height   = h
        self._zoom     = 1.0

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

    def set_zoom(self, value):
        if value > Camera._ZOOM_MAX:
            self._zoom = Camera._ZOOM_MAX
        elif value < Camera._ZOOM_MIN:
            self._zoom = Camera._ZOOM_MIN
        else:
            self._zoom = value

    def zoom_in(self):
        self.set_zoom(self._zoom + 0.01)

    def zoom_out(self):
        self.set_zoom(self._zoom - 0.01)

    def get_zoom(self):
        return self._zoom

    def get_modeled(self, surface):
        modeled = pg.Surface((self._width, self._height))
        tmp = pg.transform.scale(surface, (
            int(surface.get_width()  * self.get_zoom()),
            int(surface.get_height() * self.get_zoom())
        ))
        modeled.blit(tmp, (0, 0), self.get_rect())
        return modeled