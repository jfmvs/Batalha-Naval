import pygame as pg
from .ship import Ship


class Player(Ship):
    def __init__(self, pos: (list, tuple, pg.Vector2), stage, gun_type, guns, sprite: pg.Surface, **kwargs):
        super().__init__(pos, stage, gun_type, guns, sprite, **kwargs)

        self.nivelTotal = 0
        self.xp = 0
        self.xpNecessaria = 100
        self.calibre = int(0)
        self.power = int(0)
        self.gun_count = int(0)
        self.health = int(0)
        self.maximo = False
        self.vidaTotal = 100 + 10 * self.health
        self.vidaAtual = 100

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
            if event.button == 1:
                for gun in self.guns:
                    gun.fire()

        for gun in self.guns:
            gun.reload = max([0, gun.reload - dt])

        self.change_speed()
        self.move(dt)
        self.update_sprite(dt)