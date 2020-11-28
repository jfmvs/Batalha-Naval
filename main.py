import sys
import pygame as pg
from core import *


class App:
    def __init__(self):
        """Construtor"""

        # dados do funcionamento de App

        self._SCREEN_WIDTH     = 800
        self._SCREEN_HEIGHT    = 600
        self._SCREEN           = pg.display.set_mode((self._SCREEN_WIDTH, self._SCREEN_HEIGHT))
        self._BACKGROUND_COLOR = (53, 54, 55)
        self._CLOCK            = pg.time.Clock()
        self._TARGET_FPS       = 60
        self._running          = False
        self._current_fps      = 60
        pg.display.set_caption('Batalha Naval - Camera')

        # itens do jogo

        self.framebuffer = pg.Surface((1600, 1200))
        self.npcs = [
            Ship((200, 100), angle=70),
            Ship((500, 400), angle=-90),
            Ship((600, 100), angle=80),
            Ship((700, 600), angle=-120),
            Ship((100, 400)),
            Ship((400, 700), angle=90),
        ]
        self.player               = Ship((375, 275), angle=-90, speed=150)
        self.player_angular_speed = 150
        self.camera               = Camera((400, 300), 800, 600)
        self.camera.set_focus(self.player)

    def _update(self, dt, event):
        """Mudanças de estado"""

        if event.type == pg.QUIT:
            self._running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._running = False

        kbd = pg.key.get_pressed()

        if kbd[pg.K_a]:
            self.player.rotate(dt, -self.player_angular_speed)
        if kbd[pg.K_d]:
            self.player.rotate(dt,  self.player_angular_speed)

        if kbd[pg.K_UP]:
            self.camera.zoom_in()
        elif kbd[pg.K_DOWN]:
            self.camera.zoom_out()

        self.player.update(dt)
        self.camera.update()

    def _render(self):
        """Construir cena"""

        # renderize o mundo em framebuffer

        self.framebuffer.fill((57, 141, 212))

        for npc in self.npcs:
            npc.draw(self.framebuffer)

        self.player.draw(self.framebuffer)

    def _render_debug_data(self):
        """Dados para depuração"""

        Text.render(self._SCREEN, 'camera pos:      x: {:.2f},     y: {:.2f}'.format(
            self.camera.position[0], self.camera.position[1]
        ), (10, 5), 16, color=(255,255,255))
        Text.render(self._SCREEN, f'scale: {self.camera.zoom:.2f}', (10, 20), 16, color=(255,255,255))
        Text.render(self._SCREEN, f'fps: {self._current_fps:}', (10, 40), 16, color=(255,255,255))
        Text.render(self._SCREEN, 'player pos:     x: {:.2f},   y: {:.2f}'.format(
            *self.player.position
            ), (10, 80), 16, color=(255,255,255)
        )
        Text.render(
            self._SCREEN, f'player angle: {self.player.angle:.2f}', (10, 100), 16, color=(255,255,255)
        )

    def run(self):
        """Iniciar jogo"""

        self._running = True
        while self._running:
            dt = self._CLOCK.tick(self._TARGET_FPS) / 1000
            self._current_fps = int(1 / dt)
            event = pg.event.poll()
            self._update(dt, event)
            self._SCREEN.fill(self._BACKGROUND_COLOR)
            self._render()
            self._SCREEN.blit(self.camera.get_modeled(self.framebuffer), (0,0))
            if '-o' not in sys.argv:
                self._render_debug_data()
            pg.display.update()


def main():
    pg.init()
    app = App()
    app.run()
    pg.quit()


if __name__ == '__main__':
    main()

