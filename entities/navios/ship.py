import pygame as pg
from entities import Battery

class Ship:

    SHIP_STATS = {

        2: {
            "Turning Rate": 24,
            "Top Speed": "%.2f" % 40,
            "Speed Targets": [0, 30, 60, 90, 120],
            "Acceleration": 1.5
        }
    }

    SPRITES = {}

    @staticmethod
    def init(*args):
        for level, sprite in args:
            Ship.SPRITES[level] = sprite

    def __init__(self, pos: (list, tuple, pg.Vector2), stage, gun_type, guns, **kwargs):

        self._position         = pg.Vector2(*pos)
        self._angle            = kwargs.get('angle', 0)


        self.stage = stage
        self.stats = Ship.SHIP_STATS[self.stage]

        self._angular_speed = self.stats["Turning Rate"]

        self.speed = 0
        self.speed_target = 0
        self.speed_target_list = self.stats["Speed Targets"]
        self.acceleration = self.stats["Acceleration"]

        self.gun_type = gun_type
        self.guns = [Battery(self, i, gun_type) for i in range(guns)]

        self._render_sprite    = pg.transform.rotate(self.original_sprite, self._angle)
        self.camera = kwargs.get('camera')

    @property
    def original_sprite(self):
        return Ship.SPRITES[self.stage]

    @property
    def direction(self):
        direction = pg.Vector2(1.0, 0.0)
        direction.rotate_ip(self._angle)
        return direction

    @property
    def angle(self):
        return self._angle

    @property
    def position(self):
        return self._position

    @property
    def sprite(self):
        return self._render_sprite

    def move(self, dt: float):
        self._position.x += self.direction.x * self.speed * dt
        self._position.y -= self.direction.y * self.speed * dt

    def rotate(self, dt: float, reverse: bool = False):
        mod = -1 if reverse else 1
        self._angle += self._angular_speed * mod * dt
        self._angle %= 360

    def change_speed(self):
        if self.speed < self.speed_target_list[self.speed_target]:
            self.speed = min(self.speed_target_list[self.speed_target], self.speed + self.acceleration)
        elif self.speed > self.speed_target_list[self.speed_target]:
            self.speed = max(self.speed_target_list[self.speed_target], self.speed - self.acceleration)

    def increase_speed(self):
        if self.speed_target < 4:
            self.speed_target += 1

    def decrease_speed(self):
        if self.speed_target > 0:
            self.speed_target -= 1

    def shoot_guns(self):
        for gun in self.guns:
            gun.fire()

    def update_sprite(self, dt):
        self._render_sprite = pg.transform.rotate(self.original_sprite, self._angle)
        target = (0, 0)
        for gun in self.guns:
            self._render_sprite = gun.ready_aim(self._render_sprite, target, dt)

    def update(self, dt, event):
        self.update_sprite(dt)
