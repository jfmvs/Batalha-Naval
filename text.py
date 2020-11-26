import pygame as pg


class Text:

    @staticmethod
    def render(surface, text, pos, size, color=(0, 0, 0)):
        font = pg.font.SysFont('times new roman', size)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)

    @staticmethod
    def render_centered(surface, text, pos, size, color=(0, 0, 0)):
        font = pg.font.SysFont('times new roman', size)
        text_surface = font.render(text, True, color)
        coords = (pos[0] - text_surface.get_width() // 2,
                  pos[1] - text_surface.get_height() // 2)
        surface.blit(text_surface, coords)

