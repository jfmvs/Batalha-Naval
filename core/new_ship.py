#
import pygame as pg
import math

# Initialize pygame
pg.init()

# Clock set-up
CLOCK = pg.time.Clock()

# Display
pg.display.init()

# Game loop
running = True

# Screen setting
pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 0)
screen = pg.display.set_mode((1500, 1000))

# Font
font = pg.font.SysFont('century', 18)


def rad(angle):  # Abreviação
    return round(math.radians(angle), 2)


def ang(angle):  # Abreviação
    return round(math.degrees(angle), 2)

"""
Notas iniciais:

Todos os ângulos são medidos em graus quando possíveis

O ângulo é medido a partir do vetor horizontal para a direita (0 graus)

O ângulo aumenta no sentido anti-horário

Todos os cálculos são arrendados para 2 casas decimais

"""


class Battery:

    """
    A classe Battery é responsável pelas torretas do navio.


    Propriedades:

    ship : Armazena qual o navio a qual a torreta pertence

    mount : Coordenadas da torreta em relação ao centro da imagem de seu navio

    resting_angle : Ângulo inicial da torreta em relação ao navio


    number : Número de armas na torreta (atualmente sem uso)

    caliber : Calibre da(s) arma(s) na torreta (influencia dano)

    reload : Tempo de recarga (em segundos)


    gun_angle
    """
    def __init__(self, ship, slot, gun_type):

        mount_data = {
            2: [[(-45, 0), 0, (210, 150)], [(-35, 0), 0, (225, 135)], [(-11, 4), 0, (20, 165)],
                [(-11, -4), 0, (195, 340)]]
        }

        self.ship = ship
        self.mount, self.resting_angle, self.firing_angle = mount_data[self.ship.stage][slot]

        self.number, self.caliber = [int(i) for i in gun_type.split("x")]
        self.reload = 0

        self.gun_angle = 0
        self.aim_angle = 0
        self.rotation_speed = 30

        self.original_image = pg.image.load(f"gfx/{gun_type}_Gun_Small.png")
        self.image = pg.transform.rotate(self.original_image, (self.gun_angle + self.ship.angle) % 360)

    def ready_aim(self, ship_image, target, fps):

        ship_width, ship_height = ship_image.get_rect()[2:4]

        gun_position = [round(((self.mount[0] * math.cos(rad(self.ship.angle)))
                              - self.mount[1] * math.sin(rad(self.ship.angle))) + ship_width / 2, 2),
                       round(((-self.mount[0] * math.sin(rad(self.ship.angle)))
                              - self.mount[1] * math.cos(rad(self.ship.angle))) + ship_height / 2, 2)]

        render_position = gun_position

        gun_position = [gun_position[0] + self.ship.position[0], gun_position[1] + self.ship.position[1]]

        vertical_aim = gun_position[1] - target[1]
        horizontal_aim = target[0] - gun_position[0]
        if horizontal_aim == 0:
            if vertical_aim >= 0:
                self.aim_angle = 90
            else:
                self.aim_angle = 270

        else:
            self.aim_angle = abs(round(ang(math.atan((vertical_aim / horizontal_aim))), 2))

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
            self.gun_angle = round(self.gun_angle + (self.rotation_speed / fps), 2)
        else:
            self.gun_angle = round(self.gun_angle - (self.rotation_speed / fps), 2)


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

        self.gun_angle = self.gun_angle % 360
        self.image = pg.transform.rotate(self.original_image, (self.gun_angle + self.ship.angle) % 360)
        gun_width, gun_height = self.image.get_rect()[2:4]

        render_position = [
            int(render_position[0] - gun_width / 2), int(render_position[1] - gun_height / 2)
        ]

        ship_image.blit(self.image, render_position)
        return ship_image

    # def fire(self):

class Ship:

    def __init__(self, player, position, stage, gun_type, guns):
        ship_stats = {

            2: {
                "Turning Rate": 24,
                "Top Speed": "%.2f" % 40,
                "Speed Targets": [0, 30, 60, 90, 120],
                "Acceleration": 1.5
            }
        }

        self.player = player

        self._position = position
        self._angle = 0
        self.turning_rate = ship_stats[stage]["Turning Rate"]
        self.turning = 0
        self.turning_left = self.turning_right = False

        self.speed = 0
        self.speed_target = 0
        self.speed_target_list = ship_stats[stage]["Speed Targets"]
        self.acceleration = ship_stats[stage]["Acceleration"]
        self.increase_speed = False
        self.decrease_speed = False

        self.stage = stage
        self.stats = ship_stats[self.stage]

        self.original_image = pg.image.load(f"gfx/Ship_Stage_2_Small.png")
        self.image = pg.transform.rotate(self.original_image, self._angle)

        self.guns = [Battery(self, i, gun_type) for i in range(guns)]

    @property
    def angle(self):
        return self._angle

    @property
    def position(self):
        return self._position

    def update(self, fps, events):
        self.image = self.original_image.copy()

        if self.player:

            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        self.increase_speed = True
                        self.speed_target += 1

                    elif event.key == pg.K_s:
                        self.decrease_speed = True
                        self.speed_target -= 1

                    elif event.key == pg.K_a:
                        self.turning_left = True

                    elif event.key == pg.K_d:
                        self.turning_right = True

                elif event.type == pg.KEYUP:
                    if event.key == pg.K_w:
                        self.increase_speed = False

                    elif event.key == pg.K_s:
                        self.decrease_speed = False

                    elif event.key == pg.K_a:
                        self.turning_left = False

                    elif event.key == pg.K_d:
                        self.turning_right = False

            self.turning = self.turning_left - self.turning_right


        else:
            pass
            # Lais vai aqui


        if self.speed_target > 4:
            self.speed_target = 4
        elif self.speed_target < 0:
            self.speed_target = 0

        if self.speed < self.speed_target_list[self.speed_target]:
            self.speed = min(self.speed_target_list[self.speed_target], self.speed + self.acceleration)
        elif self.speed > self.speed_target_list[self.speed_target]:
            self.speed = max(self.speed_target_list[self.speed_target], self.speed - self.acceleration)

        if self.turning == -1:
            self._angle -= round(self.turning_rate / fps, 2)
        elif self.turning == 1:
            self._angle += round(self.turning_rate / fps, 2)

        self.turning = 0
        self._angle = self._angle % 360

        self.image = pg.transform.rotate(self.image, self._angle)

        self._position = [round(self._position[0] - (math.cos(rad(self._angle)) * self.speed / fps), 2),
                         round(self._position[1] + (math.sin(rad(self._angle)) * self.speed / fps), 2)]

        if self.player:
            target = pg.mouse.get_pos()
        else:
            pass

        for gun in self.guns:
            self.image = gun.ready_aim(self.image, target, fps)


running = True
ship = Ship(True, [200, 300], 2, "1x3", 4)
while running:
    dt = pg.time.Clock().tick(60) / 1000
    fps = int(1 / dt)

    events = list(pg.event.get())
    for event in events:
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
    screen.fill((100, 100, 255))
    ship.update(fps, events)
    screen.blit(ship.image, [int(ship.position[0]), int(ship.position[1])])
    pg.display.update()