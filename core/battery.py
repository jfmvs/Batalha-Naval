import math
import pygame as pg

class Battery:

    MOUNT_DATA = {
        2: [
        # posição inicial a partir do centro / ângulo inicial / limites de ângulos sentidos horário|anti-horário
            [(85,  0), 0, (210, 150)],
            [(75,  0), 0, (225, 135)],
            [(20, -4), 0, (20,  165)],
            [(20,  4), 0, (195, 340)]]
    }

    def __init__(self, ship, slot, gun_type):

        self.ship = ship
        self.mount, self.resting_angle, self.firing_angle = Battery.MOUNT_DATA[self.ship.stage][slot]
        self.mount = pg.Vector2(self.mount)

        self.number, self.caliber = [int(i) for i in gun_type.split("x")]
        self.reload = 0

        self.gun_angle = 0
        self.aim_angle = 0
        self.rotation_speed = 30

        self.original_image = pg.image.load(f"assets/{gun_type}_Gun_Small.png")
        self.image = pg.transform.rotate(self.original_image, (self.gun_angle + self.ship.angle) % 360)

    def ready_aim(self, ship_image, target, dt):

        # compensa a posição do mouse em relação a camera

        ship_width  = ship_image.get_width()
        ship_height = ship_image.get_height()

        # rotaciona a posição de acordo com a direção do navio
        gun_position = self.mount.rotate(-self.ship.angle)

        # centraliza a posição do navio
        render_position = gun_position + [ship_width / 2, ship_height / 2]

        offset = self.ship.camera.position - [self.ship.camera.width / 2, self.ship.camera.height / 2]
        gun_position += self.ship.position - offset

        vertical_aim   = (gun_position[1] - target[1])
        horizontal_aim = (target[0] - gun_position[0])

        if horizontal_aim == 0:
            self.aim_angle = 90 if vertical_aim >= 0 else 270

        else:
            self.aim_angle = abs(math.degrees(math.atan((vertical_aim / horizontal_aim))))
            if vertical_aim >= 0 and horizontal_aim >= 0:
                pass

            elif vertical_aim >= 0 and horizontal_aim < 0:
                self.aim_angle = 180 - self.aim_angle

            elif vertical_aim < 0 and horizontal_aim < 0:
                self.aim_angle += 180

            else:
                self.aim_angle = 360 - self.aim_angle

        self.aim_angle -= self.ship.angle

        if 180 > (self.aim_angle - self.gun_angle) % 360 >= 0:
            self.gun_angle = self.gun_angle + (self.rotation_speed * dt)
        else:
            self.gun_angle = self.gun_angle - (self.rotation_speed * dt)


        if self.firing_angle[0] < self.firing_angle[1]:
            if self.gun_angle < self.firing_angle[0]:
                self.gun_angle = self.firing_angle[0]

            elif self.gun_angle > self.firing_angle[1]:
                self.gun_angle = self.firing_angle[1]

        else:
            if self.firing_angle[1] < self.gun_angle < self.firing_angle[0]:
                if self.firing_angle[0] - self.gun_angle < self.gun_angle - self.firing_angle[1]:
                    self.gun_angle = self.firing_angle[0]

                elif self.gun_angle - self.firing_angle[1]:
                    self.gun_angle = self.firing_angle[1]

        self.gun_angle %= 360
        self.image = pg.transform.rotate(self.original_image, (self.gun_angle + self.ship.angle) % 360)

        gun_width  = self.image.get_width()
        gun_height = self.image.get_height()

        render_position -= [gun_width / 2, gun_height / 2]
        render_position = (int(render_position.x), int(render_position.y))

        ship_image.blit(self.image, render_position)
        return ship_image