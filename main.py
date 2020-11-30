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
        self._BACKGROUND_COLOR = (57, 141, 212)
        self._CLOCK            = pg.time.Clock()
        self._TARGET_FPS       = 60
        self._running          = False
        self._current_fps      = 60
        pg.display.set_caption('Batalha Naval - Camera')

        # itens do jogo

        self.world = WorldManager((5600, 1200), (800, 600))

        SpriteManager.load('basic', 'assets/player.png')
        SpriteManager.rescale('basic', (120, 20))

        npcs = [
            Ship(( 200, 100), sprite=SpriteManager.get('basic'), angle=70),
            Ship((1200, 100), sprite=SpriteManager.get('basic'), angle=-90),
            Ship((2000, 100), sprite=SpriteManager.get('basic'), angle=80),
            Ship((2600, 100), sprite=SpriteManager.get('basic'), angle=-120),
            Ship((3300, 100), sprite=SpriteManager.get('basic')),
            Ship((4800, 100), sprite=SpriteManager.get('basic'), angle=90),
        ]

        for npc in npcs:
            self.world.add_obj(npc)

        self.player               = Ship((400, 300), sprite=SpriteManager.get('basic'), angle=135, speed=150)
        self.player_angular_speed = 150
        self.camera               = Camera((400, 300))

    def _update(self, dt, event):
        """Mudanças de estado"""

        if event.type == pg.QUIT:
            self._running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._running = False

        kbd = pg.key.get_pressed()

        if kbd[pg.K_a]:
            self.camera.position.x -= 250 * dt
            self.player.position.x -= 250 * dt
        if kbd[pg.K_d]:
            self.camera.position.x += 250 * dt
            self.player.position.x += 250 * dt

        if kbd[pg.K_w]:
            self.camera.position.y -= 250 * dt
            self.player.position.y -= 250 * dt
        elif kbd[pg.K_s]:
            self.camera.position.y += 250 * dt
            self.player.position.y += 250 * dt

    def _render(self):
        """Construir cena"""

        for chunk in self.world.get_active_chunks(self.player.position):
            chunk_objs = self.world.get_objs(chunk)
            for obj in chunk_objs:
                rotated = pg.transform.rotate(obj.sprite, obj.angle)
                self._SCREEN.blit(rotated, (
                    (obj.position.x - rotated.get_width()  // 2) - (self.camera.position.x - self._SCREEN_WIDTH  // 2),
                    (obj.position.y - rotated.get_height() // 2) - (self.camera.position.y - self._SCREEN_HEIGHT // 2),
                ))


        renderable = self.camera.get_modeled(self.player)
        self._SCREEN.blit(renderable, (
            (self.player.position.x - renderable.get_width()  // 2) - (self.camera.position.x - self._SCREEN_WIDTH  // 2),
            (self.player.position.y - renderable.get_height() // 2) - (self.camera.position.y - self._SCREEN_HEIGHT // 2),
        ))

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

