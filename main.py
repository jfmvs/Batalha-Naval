import sys
from random import randint
import pygame as pg
from core import *


class App:
    def __init__(self):
        """Construtor"""

        # dados do funcionamento de App

        self._SCREEN_WIDTH     = 800
        self._SCREEN_HEIGHT    = 600
        self._SCREEN           = pg.display.set_mode((self._SCREEN_WIDTH, self._SCREEN_HEIGHT))
        self._BACKGROUND_COLOR = (57, 141, 212)
        self._CLOCK            = pg.time.Clock()
        self._TARGET_FPS       = 60
        self._running          = False
        self._current_fps      = 60
        pg.display.set_caption('Batalha Naval - Testes')

        # itens do jogo

        Renderer.init()

        SpriteManager.load('basic', 'assets/basic-ship.png')
        SpriteManager.load('player', 'assets/ship-stage-2.png')
        SpriteManager.load('crate', 'assets/floating-crate-3.png')
        SpriteManager.load('menu', 'assets/menu-mortar.png')
        SpriteManager.resize('basic', (120, 20))
        SpriteManager.resize('player', (204, 20))
        SpriteManager.rescale('menu', 0.9)

        self.npcs   = [
            Ship((randint(0, 1600), randint(0, 1200)), sprite=SpriteManager.get('basic'), angle=randint(0, 360))
            for _ in range(10)
        ]
        self.crates = [(randint(0, 1600), randint(0, 1200)) for _ in range(10)]

        self.player = Ship((400, 300), sprite=SpriteManager.get('player'), angle=135, speed=150)
        self.camera = Camera((400, 300))

    def _update(self, dt, event):
        """Mudanças de estado"""

        if event.type == pg.QUIT:
            self._running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._running = False

        kbd = pg.key.get_pressed()

        if kbd[pg.K_a]:
            self.player.rotate(dt)
        if kbd[pg.K_d]:
            self.player.rotate(dt, True)

        self.player.move(dt)
        self.camera.follow(self.player, dt)

    def _render(self):
        """Construir cena"""

        for npc in self.npcs:
            Renderer.render_ship(self._SCREEN, npc, self.camera)
        for crate_pos in self.crates:
            Renderer.render_sprite(self._SCREEN, SpriteManager.get('crate'), crate_pos, self.camera)

        Renderer.render_ship(self._SCREEN, self.player, self.camera)

        Renderer.render_sprite(self._SCREEN, SpriteManager.get('menu'), (0, 0))

    def _render_debug_data(self):
        """Dados para depuração"""

        Renderer.render_debug_msg(self._SCREEN, pos=(10, 150 + 5), msg='camera pos:      x: {:.2f},     y: {:.2f}'.format(
            self.camera.position[0], self.camera.position[1]
        ))
        Renderer.render_debug_msg(self._SCREEN, pos=(10, 150 + 20), msg=f'scale: {self.camera.zoom:.2f}')
        Renderer.render_debug_msg(self._SCREEN, pos=(10, 150 + 60), msg='player pos:     x: {:.2f},   y: {:.2f}'.format(
            *self.player.position
        ))
        Renderer.render_debug_msg(self._SCREEN, pos=(10, 150 + 80), msg=f'player angle: {self.player.angle:.2f}')
        Renderer.render_debug_msg(self._SCREEN, pos=(10, 150 + 100), msg=f'fps: {self._current_fps:}')

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

