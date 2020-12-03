import sys
import pygame as pg
from .battery import Battery
from .ship import Ship


class Player(Ship):
    def __init__(self, pos: (list, tuple, pg.Vector2), stage, gun_type, guns, sprite: pg.Surface, **kwargs):
        super().__init__(pos, stage, gun_type, guns, sprite, **kwargs)

    def update_sprite(self, dt):
        self._render_sprite = pg.transform.rotate(self._original_sprite, self._angle)
        target = pg.mouse.get_pos()
        for gun in self.guns:
            self._render_sprite = gun.ready_aim(self._render_sprite, target, dt)

    def update(self, dt, event):
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_w:
                self.increase_speed()
            elif event.key == pg.K_s:
                self.decrease_speed()

            elif event.key == pg.K_a:
                self.rotate(dt, True)
            elif event.key == pg.K_d:
                self.rotate(dt)

        elif event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                for gun in self.guns:
                    gun.fire(pg.mouse.get_pos())

        self.change_speed()
        self.move(dt)
        self.update_sprite(dt)
        self.shoot_guns(dt)