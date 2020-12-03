import sys
from random import randint
import pygame as pg
from core import *
from entities import *


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

        SpriteManager.load('ship', 'assets/Ship_Stage_2_Small.png')
        SpriteManager.load('crate', 'assets/floating-crate-3.png')
        SpriteManager.load('cannon-ball', 'assets/cannonball.png')
        SpriteManager.rescale('cannon-ball', 0.5)

        self.camera = Camera((400, 300), self._SCREEN.get_size())
        self.player = Player((400, 300), sprite=SpriteManager.get('ship'), stage=2,
                             gun_type='1x3', guns=1, camera=self.camera)
        self.npcs   = [
            Npc((randint(0, 1600), randint(0, 1200)), angle=randint(0, 360), sprite=SpriteManager.get('ship'), stage=2,
                   gun_type='1x3', guns=4, camera=self.camera, player=self.player)
            for _ in range(10)
        ]
        self.crates = [(randint(0, 1600), randint(0, 1200)) for _ in range(10)]
        self.crate_mask = pg.mask.from_surface(SpriteManager.get('crate'))
        self.menu = Menu(self.player)

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
        if kbd[pg.K_l]:
            self.player.xp += 10
        if kbd[pg.K_k]:
            self.player.xp -= 10
        if kbd[pg.K_u]:
            if self.player.xp >= self.player.xpNecessaria:
                if type(self.player.power) == int:
                    self.player.nivelTotal += 1
                    self.player.xp -= self.player.xpNecessaria
                    self.player.power += 1
        if kbd[pg.K_i]:
            if self.player.xp >= self.player.xpNecessaria:
                if type(self.player.calibre) == int:
                    self.player.nivelTotal += 1
                    self.player.xp -= self.player.xpNecessaria
                    self.player.calibre += 1
        if kbd[pg.K_o]:
            if self.player.xp >= self.player.xpNecessaria:
                if type(self.player.health) == int:
                    self.player.nivelTotal += 1
                    self.player.xp -= self.player.xpNecessaria
                    self.player.vidaAtual += 20
                    self.player.health += 1
        if kbd[pg.K_p]:
            if self.player.xp >= self.player.xpNecessaria:
                if type(self.player.guns) == int:
                    self.player.nivelTotal += 1
                    self.player.xp -= self.player.xpNecessaria
                    self.player.guns += 1
        if kbd[pg.K_m]:
            if self.player.vidaAtual > 10:
                self.player.vidaAtual -= 10
        if kbd[pg.K_n]:
            self.player.vidaAtual += 10

        self.player.update(dt, event)
        self.camera.center(self.player)

        player_mask = pg.mask.from_surface(self.player.sprite)

        for npc in self.npcs:
            npc.update(dt, event)
            npc_mask = pg.mask.from_surface(npc.sprite)
            offset = (
                int(self.player.position.x - self.player.sprite.get_width()  / 2 - npc.position.x + npc.sprite.get_width()  / 2),
                int(self.player.position.y - self.player.sprite.get_height() / 2 - npc.position.y + npc.sprite.get_height() / 2)
            )
            result = npc_mask.overlap(player_mask, offset)
            if result:
                print('Player-Ship collision detected')

            for bullet in BulletManager._bullets:
                sprite = SpriteManager.get('cannon-ball')
                bullet_mask = pg.mask.from_surface(sprite)
                offset = (
                    int(bullet.x - sprite.get_width()  / 2 - npc.position.x + npc.sprite.get_width()  / 2),
                    int(bullet.y - sprite.get_height() / 2 - npc.position.y + npc.sprite.get_height() / 2)
                )
                result = npc_mask.overlap(bullet_mask, offset)
                if result:
                    print('Ship-Bullet collision detected')


        for crate_pos in self.crates:
            offset = (
                int(self.player.position.x - self.player.sprite.get_width()  / 2 - crate_pos[0]),
                int(self.player.position.y - self.player.sprite.get_height() / 2 - crate_pos[1])
            )
            result = self.crate_mask.overlap(player_mask, offset)
            if result:
                print('Crate Collected')
                self.crates.remove(crate_pos)
                break

        BulletManager.update(dt)
        self.menu.update()


    def _render(self):
        """Construir cena"""

        for npc in self.npcs:
            Renderer.render_ship(self._SCREEN, npc, self.camera)
        for crate_pos in self.crates:
            Renderer.render_sprite(self._SCREEN, SpriteManager.get('crate'), crate_pos, self.camera)


        Renderer.render_ship(self._SCREEN, self.player, self.camera)
        for bullet in BulletManager._bullets:
            Renderer.render_sprite(self._SCREEN, SpriteManager.get('cannon-ball'), (bullet.x, bullet.y), centered=True)

        self.menu.render(self._SCREEN)


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

