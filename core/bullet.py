import pygame
import math


class Bullet(object):

    BULLET_DATA = {
        # velocidade / tempo de vida
        3: [120, 5]

    }


    def __init__(self, position, angle, caliber):
        self.x, self.y = position
        self.angle = angle

        self.lifetime, self.speed = Bullet.BULLET_DATA[caliber]

        self.x_vel = round(math.cos(self.angle) * self.speed, 2)
        self.y_vel = round(math.sin(self.angle) * self.speed, 2)

    def travel(self, dt):
        self.x = self.x + self.x_vel / dt
        self.y = self.y + self.y_vel / dt

        self.lifetime -= 1 / dt

        if self.lifetime > 0:
            return True
        else:
            return False


    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bullets.append(bullet(x, y, mouse_x, mouse_y))

    for bullet_ in bullets:
        bullet_.draw(win, fps)
        if bullet_.lifetime <= 0:
            bullets.pop(bullets.index(bullet_))