import pygame as pg
from entities.bullet import Bullet

class BulletManager:

    _bullets = []

    @staticmethod
    def add(position, angle, caliber):
        BulletManager._bullets.append(Bullet(position, angle, caliber))

    @staticmethod
    def update(dt):
        alive = []
        for index, bullet in enumerate(BulletManager._bullets):
            if bullet.travel(dt):
                alive.append(bullet)

        BulletManager._bullets = alive

    @staticmethod
    def render(surface, camera):
        for bullet in BulletManager._bullets:
            pg.draw.circle(surface, (200,200,200), (bullet.x, bullet.y), 2)

