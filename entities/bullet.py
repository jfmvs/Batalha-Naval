import math


class Bullet(object):

    BULLET_DATA = {
        # tempo de vida / velocidade
        3: [2, 120]

    }


    def __init__(self, position, angle, caliber):
        self.x, self.y = position
        self.angle = angle
        print(self.angle)
        self.lifetime, self.speed = Bullet.BULLET_DATA[caliber]

        self.x_vel =  math.cos(math.radians(self.angle)) * self.speed
        self.y_vel = -math.sin(math.radians(self.angle)) * self.speed

        print(self.x_vel, self.y_vel)

    def travel(self, dt):
        self.x += self.x_vel * dt
        self.y += self.y_vel * dt
        self.lifetime -= dt

        if self.lifetime > 0:
            return True
        else:
            return False
