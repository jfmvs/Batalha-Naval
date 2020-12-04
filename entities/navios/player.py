import pygame as pg
from .ship import Ship
from entities.battery import Battery


class Player(Ship):
    STAGE_STATUS = [30, 200, 500]

    def __init__(self, pos: (list, tuple, pg.Vector2), stage, gun_type, guns, **kwargs):
        super().__init__(pos, stage, gun_type, guns, **kwargs)

        self.nivelTotal = 0
        self.xp = 0
        self.xpNecessaria = 30
        self.calibre = int(2)
        self.power = int(0)
        self.gun_count = int(2)
        self.health = int(2)
        self.maximo = False
        self.vidaTotal = (20 * self.health) + Player.STAGE_STATUS[self.stage - 1]
        self.vidaAtual = 20

    def update_sprite(self, dt):
        self._render_sprite = pg.transform.rotate(self.original_sprite, self._angle)
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
            if event.button == 1:
                for gun in self.guns:
                    gun.fire()

        for gun in self.guns:
            gun.reload = max([0, gun.reload - dt])

        self.change_speed()
        self.move(dt)
        self.update_sprite(dt)

    def level_up(self):
        self.nivelTotal += 1
        self.xp -= self.xpNecessaria

    def gain_gun(self):
        self.gun_count += 1
        self.guns.append(Battery(self, self.gun_count - 1, self.gun_type))

