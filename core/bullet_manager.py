import pygame as pg
from entities.bullet import Bullet


class BulletManager:

    _bullets = []
    _sprite  = None
    _mask    = None

    @staticmethod
    def add(owner, position, angle, caliber):
        BulletManager._bullets.append(Bullet(owner, position, angle, caliber))

    @staticmethod
    def set_sprite(sprite):
        BulletManager._sprite = sprite
        BulletManager._mask   = pg.mask.from_surface(BulletManager._sprite)

    @staticmethod
    def update(dt):
        alive = []
        for index, bullet in enumerate(BulletManager._bullets):
            if bullet.travel(dt):
                alive.append(bullet)

        BulletManager._bullets = alive

    @staticmethod
    def render(surface):
        for bullet in BulletManager._bullets:
            pg.draw.circle(surface, (200,200,200), (bullet.x, bullet.y), 2)

    @staticmethod
    def active_bullets():
        return BulletManager._bullets

    @staticmethod
    def get_sprite():
        return BulletManager._sprite

    @staticmethod
    def get_sprite_width():
        return BulletManager._sprite.get_width()

    @staticmethod
    def get_sprite_height():
        return BulletManager._sprite.get_height()

    @staticmethod
    def get_mask():
        return BulletManager._mask

