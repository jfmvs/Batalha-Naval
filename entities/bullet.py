import math


class Bullet(object):

    BULLET_DATA = {
        # tempo de vida / velocidade / dano
        1: [1, 200, 5],
        2: [1.6, 150, 8],
        3: [3, 120, 15],
        4: [3, 135, 25],
        5: [3.5, 150, 40],
        6: [4, 160, 70]

    }


    def __init__(self, owner, position, angle, caliber):
        self.x, self.y = position
        self.angle = angle
        self.lifetime, self.speed, self.damage = Bullet.BULLET_DATA[caliber]
        self.owner = owner

        self.x_vel =  math.cos(math.radians(self.angle)) * self.speed
        self.y_vel = -math.sin(math.radians(self.angle)) * self.speed

    def travel(self, dt):
        self.x += self.x_vel * dt
        self.y += self.y_vel * dt
        self.lifetime -= dt

        if self.lifetime > 0:
            return True
        else:
            return False
