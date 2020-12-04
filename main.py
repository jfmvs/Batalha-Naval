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
        self._enemy_index      = 0
        pg.mouse.set_visible(False)
        pg.display.set_caption('Batalha Naval')

        # itens do jogo

        Renderer.init()

        SpriteManager.load('ship1', 'assets/Ship_Stage_1_Small.png')
        SpriteManager.load('ship2', 'assets/Ship_Stage_2_Small.png')
        SpriteManager.load('ship3', 'assets/Ship_Stage_3_Small.png')
        SpriteManager.load('crate', 'assets/floating-crate-3.png')
        SpriteManager.load('health-box', 'assets/health-box-2.png')
        SpriteManager.load('xp-crate', 'assets/xp-crate.png')
        SpriteManager.load('bullet', 'assets/Bullet_3.png')
        SpriteManager.load('crosshair', 'assets/crosshair.png')
        SpriteManager.rescale('crosshair', 0.5)

        BulletManager.set_sprite(SpriteManager.get('bullet'))

        Ship.init((1, SpriteManager.get('ship1')), (2, SpriteManager.get('ship2')), (3, SpriteManager.get('ship3')))

        self.camera = Camera((400, 300), self._SCREEN.get_size())
        self.player = Player((400, 300), stage=1,
                             gun_type='1x2', guns=2, camera=self.camera)

        self.npcs, self._enemy_index = self.new_enemies(self._enemy_index)

        self.crates = self.get_crates()
        self.menu = Menu(self.player)

    def new_enemies(self, index):
        ENEMY_LIST = [
            [Npc(self.camera.position + (randint(-400, 400), randint(-300, 300)), angle=randint(0, 360), stage=1,
                 gun_type='1x1', guns=1, camera=self.camera, player=self.player) for _ in range(1)],
            [Npc(self.camera.position + (randint(-400, 400), randint(-300, 300)), angle=randint(0, 360), stage=1,
                 gun_type='1x1', guns=1, camera=self.camera, player=self.player) for _ in range(2)],
            [Npc(self.camera.position + (randint(-400, 400), randint(-300, 300)), angle=randint(0, 360), stage=1,
                 gun_type='1x1', guns=1, camera=self.camera, player=self.player) for _ in range(3)],
            [Npc(self.camera.position + (randint(-400, 400), randint(-300, 300)), angle=randint(0, 360), stage=1,
                 gun_type='1x1', guns=1, camera=self.camera, player=self.player) for _ in range(4)],
            [Npc(self.camera.position + (randint(-400, 400), randint(-300, 300)), angle=randint(0, 360), stage=1,
                 gun_type='1x1', guns=2, camera=self.camera, player=self.player) for _ in range(2)],
            [Npc(self.camera.position + (randint(-400, 400), randint(-300, 300)), angle=randint(0, 360), stage=1,
                 gun_type='1x1', guns=2, camera=self.camera, player=self.player) for _ in range(3)],
            [Npc(self.camera.position + (randint(-400, 400), randint(-300, 300)), angle=randint(0, 360), stage=1,
                 gun_type='1x2', guns=2, camera=self.camera, player=self.player) for _ in range(3)],
            [Npc(self.camera.position + (randint(-400, 400), randint(-300, 300)), angle=randint(0, 360), stage=1,
                 gun_type='1x2', guns=3, camera=self.camera, player=self.player) for _ in range(3)],
            [Npc(self.camera.position + (randint(-400, 400), randint(-300, 300)), angle=randint(0, 360), stage=1,
                 gun_type='1x2', guns=3, camera=self.camera, player=self.player) for _ in range(4)]
        ]
        index += 1
        return ENEMY_LIST[index - 1], index

    def get_crates(self):
        crates = []

        for _ in range(randint(1, 5)):
            crates.append(
                HPContainer(self.player, (randint(0, 1600), randint(0, 1200)), SpriteManager.get('health-box'))
            )
        for _ in range(randint(1, 5)):
            crates.append(
                XPContainer(self.player, (randint(0, 1600), randint(0, 1200)), SpriteManager.get('xp-crate'))
            )
        return crates

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
        if kbd[pg.K_m]:
            if self.player.vidaAtual > 10:
                self.player.vidaAtual -= 10
        if kbd[pg.K_n]:
            self.player.vidaAtual += 10

        self.player.update(dt, event)
        self.camera.center(self.player)
        self.menu.update(event)

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

            for bullet in BulletManager.active_bullets():
                offset = (
                    int(bullet.x - (BulletManager.get_sprite_width()  / 2) - (npc.position.x - (npc.sprite.get_width() / 2) -
                                                               (self.camera.position[0] - (self._SCREEN_WIDTH / 2)))),
                    int(bullet.y - (BulletManager.get_sprite_height() / 2) - (npc.position.y - (npc.sprite.get_height() / 2)) +
                        (self.camera.position[1] - (self._SCREEN_HEIGHT / 2))))

                result = npc_mask.overlap(BulletManager.get_mask(), offset)
                if result and bullet.owner not in self.npcs:
                    npc.vidaAtual -= bullet.damage
                    bullet.lifetime = 0

        alive_npcs = []
        for npc in self.npcs:
            if npc.vidaAtual > 0:
                alive_npcs.append(npc)
            else:
                self.crates.append(XPContainer(self.player, npc.position, SpriteManager.get('xp-crate'), npc.stage))
        self.npcs = alive_npcs.copy()

        for bullet in BulletManager.active_bullets():
            offset = (
                int(bullet.x - (BulletManager.get_sprite_width() / 2) -
                    (self.player.position.x - (self.player.sprite.get_width() / 2) -
                    (self.camera.position[0] - (self._SCREEN_WIDTH / 2)))),
                int(bullet.y - (BulletManager.get_sprite_height() / 2) -
                    (self.player.position.y - (self.player.sprite.get_height() / 2)) +
                    (self.camera.position[1] - (self._SCREEN_HEIGHT / 2))))

            result = player_mask.overlap(BulletManager.get_mask(), offset)
            if result and not self.player == bullet.owner:
                self.player.vidaAtual -= bullet.damage
                bullet.lifetime = 0

        for crate in self.crates:
            crate.overlap()
            if not crate.active:
                self.crates.remove(crate)
                break

        BulletManager.update(dt)

        if len(self.npcs) == 0:
            self.npcs, self._enemy_index = self.new_enemies(self._enemy_index)


    def _render(self):
        """Construir cena"""

        for npc in self.npcs:
            Renderer.render_ship(self._SCREEN, npc, self.camera)
        for crate in self.crates:
            Renderer.render_sprite(self._SCREEN, crate.sprite, crate.position, self.camera)

        Renderer.render_ship(self._SCREEN, self.player, self.camera)

        for bullet in BulletManager.active_bullets():
            sprite = pg.transform.rotate(BulletManager.get_sprite(), bullet.angle)
            Renderer.render_sprite(self._SCREEN, sprite, (bullet.x, bullet.y), centered=True)

        self.menu.render(self._SCREEN)

        Renderer.render_sprite(self._SCREEN, SpriteManager.get('crosshair'), pg.mouse.get_pos(), centered=True)


    def _render_debug_data(self):
        """Dados para depuração"""

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

