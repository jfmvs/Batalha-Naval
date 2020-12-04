import pygame as pg
from entities import Ship, Camera


class Renderer:

    _debug_font = None

    @staticmethod
    def init():
        Renderer._debug_font = pg.font.SysFont('times new roman', 16)

    @staticmethod
    def render_debug_msg(surface, msg, pos, centered: bool = False, color: (list, tuple) = (255, 255, 255)):
        text_surface = Renderer._debug_font.render(msg, True, color)
        coords = pos
        if centered:
            coords = (pos[0] - text_surface.get_width() // 2,
                      pos[1] - text_surface.get_height() // 2)
        surface.blit(text_surface, coords)

    @staticmethod
    def render_text(surface, msg, pos, centered=False, font='Arial', size=16, color=(255,255,255)):
        font = pg.font.SysFont(font, size)
        render_surface = font.render(msg, True, color)
        coords = list(pos)
        if centered:
            coords[0] -= render_surface.get_width()  // 2
            coords[1] -= render_surface.get_height() // 2
        surface.blit(render_surface, coords)

    @staticmethod
    def render_ship(surface, ship: Ship, camera: (Camera, None) = None):
        pos     = (ship.position.x, ship.position.y)
        Renderer.render_sprite(surface, ship.sprite, pos, centered=True, camera=camera)

    @staticmethod
    def render_sprite(surface: pg.Surface, sprite: pg.Surface, pos: (list, tuple),
                      camera: (Camera, None) = None, centered: bool = False):
        coords = list(pos)

        if centered:
            coords[0] -= sprite.get_width() // 2
            coords[1] -= sprite.get_height() // 2
        if camera is not None:
            coords[0] -= camera.position.x - surface.get_width() // 2
            coords[1] -= camera.position.y - surface.get_height() // 2

        surface.blit(sprite, coords)
