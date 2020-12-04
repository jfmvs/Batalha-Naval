import pygame as pg
from .ship import Ship
import math

class Npc(Ship):
    def __init__(self, pos: (list, tuple, pg.Vector2), stage, gun_type, guns, player, **kwargs):
        super().__init__(pos, stage, gun_type, guns, **kwargs)
        self.player = player

    def update_sprite(self, dt):
        self._render_sprite = pg.transform.rotate(self.original_sprite, self._angle)
        target = self.player.position - self.position
        for gun in self.guns:
            self._render_sprite = gun.ready_aim(self._render_sprite, target, dt)

    def update(self, dt, event):
        attack_angle = (self.angle - self.player.angle) % 360
        difference_angle = ((math.degrees(math.atan2(self.position[0] - self.player.position[0],
                                                     self.player.position[1] - self.position[
                                                         1]))) + self.angle + 90) % 360
        min_distance = 200
        distance = self.player.position - self.position
        distance = math.sqrt(distance[0] ** 2 + distance[1] ** 2)

        if distance > min_distance:
            if 270 < difference_angle or difference_angle < 90:
                self.increase_speed()
                if 0 < difference_angle < 180:
                    self.rotate(dt, True)
                else:
                    self.rotate(dt)

            else:
                self.decrease_speed()

                if 0 < difference_angle < 180:
                    self.rotate(dt, True)
                else:
                    self.rotate(dt)
        else:

            if 270 < difference_angle or difference_angle < 90:
                self.decrease_speed()

            else:
                self.increase_speed()

            if attack_angle < 180:
                self.rotate(dt, True)
            elif attack_angle > 180:
                self.rotate(dt)

        self.change_speed()
        self.move(dt)
        self.update_sprite(dt)

