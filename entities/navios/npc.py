import pygame as pg
from .ship import Ship


class Npc(Ship):
    def __init__(self, pos: (list, tuple, pg.Vector2), stage, gun_type, guns, sprite: pg.Surface, player, **kwargs):
        super().__init__(pos, stage, gun_type, guns, sprite, **kwargs)
        self.player = player

    def update_sprite(self, dt):
        self._render_sprite = pg.transform.rotate(self._original_sprite, self._angle)
        target = self.player.position
        for gun in self.guns:
            self._render_sprite = gun.ready_aim(self._render_sprite, target, dt)

    def update(self, dt, event):

        if self.player.speed > self.speed:
            self.increase_speed()
        else:
            self.decrease_speed()

        self.change_speed()
        self.move(dt)
        self.update_sprite(dt)
