import pygame as pg
from .ship import Ship
import math

class Npc(Ship):
    def __init__(self, pos: (list, tuple, pg.Vector2), stage, gun_type, guns, sprite: pg.Surface, player, **kwargs):
        super().__init__(pos, stage, gun_type, guns, sprite, **kwargs)
        self.player = player

    def update_sprite(self, dt):
        self._render_sprite = pg.transform.rotate(self._original_sprite, self._angle)
        target = self.player.position - self.position
        for gun in self.guns:
            self._render_sprite = gun.ready_aim(self._render_sprite, target, dt)

    def update(self, dt, event):

        attack_angle = (self.angle - self.player.angle + 180) % 360
        max_distance, optimal_distance, min_distance = 100, 50, 30
        distance = self.player.position - self.position
        distance = math.sqrt(distance[0] ** 2 + distance[1] ** 2)

        if max_distance > distance > optimal_distance and 90 < attack_angle < 270:
            self.increase_speed()
        elif distance > max_distance and 150 < attack_angle < 210:
            self.increase_speed()
        else:
            self.decrease_speed()

        if distance > max_distance:
            if attack_angle > 180:
                self.rotate(dt, True)
            elif attack_angle < 180:
                self.rotate(dt)
        elif distance > optimal_distance:
            if attack_angle > 190:
                self.rotate(dt, True)
            elif attack_angle < 170:
                self.rotate(dt)
        else:
            if attack_angle < 180:
                self.rotate(dt, True)
            elif attack_angle > 180:
                self.rotate(dt)

        self.change_speed()
        self.move(dt)
        self.update_sprite(dt)
