import math


class Bullet(object):

    BULLET_DATA = {
        # tempo de vida / velocidade
        3: [2, 120]

    }


    def __init__(self, position, angle, caliber):
        self.x, self.y = position
        self.angle = angle

        self.lifetime, self.speed = Bullet.BULLET_DATA[caliber]

        self.x_vel = round(math.cos(self.angle) * self.speed, 2)
        self.y_vel = round(math.sin(self.angle) * self.speed, 2)

    def travel(self, dt):
        self.x = self.x + self.x_vel * dt
        self.y = self.y + self.y_vel * dt

        self.lifetime -= dt

        if self.lifetime > 0:
            return True
        else:
            return False
