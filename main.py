import sys
from random import randint
import pygame as pg
from core import *
from entities import *


class App:
    azul = pg.image.load('assets\\mazul.png')
    mazul = pg.image.load('assets\mazul.png')
    verde = pg.image.load('assets\\verde.png')
    menu = pg.image.load('assets\menu.png')

    def transformando(self):
        escalaVida = 137/Ship.vidaTotal
        vida = int(escalaVida * Ship.vidaAtual)
        App.verde = pg.transform.scale(App.verde, (vida, 18))
        escalaXP = 140 / Ship.xpNecessaria
        barraxp = int(escalaXP * Ship.xp)
        if Ship.xp <= Ship.xpNecessaria:
            App.azul = pg.transform.scale(App.mazul, (barraxp, 20))
        else:
            App.azul = pg.transform.scale(App.mazul, (140, 20))

    def status(self):
        if type(Ship.health) == int:
            Ship.vidaTotal = 100 + 20*Ship.health
        if type(Ship.nivelTotal) == int:
            Ship.xpNecessaria = 100 + 10*Ship.nivelTotal
        else:
            Ship.maximo = True
        if Ship.power == 5:
            Ship.power = 'MAX'
        if Ship.calibre == 4:
            Ship.calibre = 'MAX'
        if Ship.health == 7:
            Ship.health = 'MAX'
        if Ship.guns == 3:
            Ship.guns = 'MAX'
        if Ship.nivelTotal == 19:
            Ship.nivelTotal = 'MAX'

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
        SpriteManager.load('menu', 'assets/menu.PNG')
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
            Ship.xp += 100
        if kbd[pg.K_k]:
            Ship.xp -= 100
        if kbd[pg.K_u]:
            if Ship.xp >= Ship.xpNecessaria:
                if type(Ship.power) == int:
                    Ship.nivelTotal += 1
                    Ship.xp -= Ship.xpNecessaria
                    Ship.power += 1
        if kbd[pg.K_i]:
            if Ship.xp >= Ship.xpNecessaria:
                if type(Ship.calibre) == int:
                    Ship.nivelTotal += 1
                    Ship.xp -= Ship.xpNecessaria
                    Ship.calibre += 1
        if kbd[pg.K_o]:
            if Ship.xp >= Ship.xpNecessaria:
                if type(Ship.health) == int:
                    Ship.nivelTotal += 1
                    Ship.xp -= Ship.xpNecessaria
                    Ship.vidaAtual += 20
                    Ship.health += 1
        if kbd[pg.K_p]:
            if Ship.xp >= Ship.xpNecessaria:
                if type(Ship.guns) == int:
                    Ship.nivelTotal += 1
                    Ship.xp -= Ship.xpNecessaria
                    Ship.guns += 1
        if kbd[pg.K_m]:
            if Ship.vidaAtual > 10:
                Ship.vidaAtual -= 10
        if kbd[pg.K_n]:
            Ship.vidaAtual += 10

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
        App.transformando(self)
        App.status(self)


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


    def _render(self):
        """Construir cena"""

        for npc in self.npcs:
            Renderer.render_ship(self._SCREEN, npc, self.camera)
        for crate_pos in self.crates:
            Renderer.render_sprite(self._SCREEN, SpriteManager.get('crate'), crate_pos, self.camera)


        Renderer.render_ship(self._SCREEN, self.player, self.camera)
        for bullet in BulletManager._bullets:
            Renderer.render_sprite(self._SCREEN, SpriteManager.get('cannon-ball'), (bullet.x, bullet.y), centered=True)

        Renderer.render_sprite(self._SCREEN, SpriteManager.get('menu'), (400, 70), centered=True)
        self._SCREEN.blit(self.verde, (149, 31))
        self._SCREEN.blit(self.azul, (148, 80))
        Renderer.render_text(self._SCREEN, f'{Ship.calibre}', (418, 73), font='Calibri', size=18, color=(0, 0, 0))
        Renderer.render_text(self._SCREEN, f'{Ship.power}', (410, 31), font='Calibri', size=18, color=(0, 0, 0))
        Renderer.render_text(self._SCREEN, f'{Ship.health}', (538, 31), font='Calibri', size=18, color=(0, 0, 0))
        Renderer.render_text(self._SCREEN, f'{Ship.guns}', (530, 74), font='Calibri', size=18, color=(0, 0, 0))
        Renderer.render_text(self._SCREEN, f'{Ship.nivelTotal}', (352, 13), font='Calibri', size=18, color=(0, 0, 0))
        if Ship.maximo is False:
            Renderer.render_text(self._SCREEN, f'{Ship.xp}/{Ship.xpNecessaria}', (180, 60), font='Calibri', size=18,
                                 color=(0, 0, 0))
            if Ship.xp >= Ship.xpNecessaria:
                Renderer.render_text(self._SCREEN, 'Você pode melhorar um atributo!', (370, 12), font='Calibri',
                                     size=17, color=(0, 0, 0))
                if type(Ship.power) == int:
                    Renderer.render_text(self._SCREEN, '[Press U]', (402, 52), font='Calibri', size=16, color=(0, 0, 0))
                if type(Ship.calibre) == int:
                    Renderer.render_text(self._SCREEN, '[Press I]', (410, 102),
                                         font='Calibri', size=16, color=(0, 0, 0))
                if type(Ship.health) == int:
                    Renderer.render_text(self._SCREEN, '[Press O]', (525, 52), font='Calibri',
                                         size=16, color=(0, 0, 0))
                if type(Ship.guns) == int:
                    Renderer.render_text(self._SCREEN, '[Press P]', (536, 100), font='Calibri',
                                         size=16, color=(0, 0, 0))
        else:
            Renderer.render_text(self._SCREEN, 'MAXIMO ATINGIDO', (180, 60), font='Calibri', size=16, color=(0, 0, 0))
        Renderer.render_text(self._SCREEN, f'{Ship.vidaAtual}/{Ship.vidaTotal}', (178, 11),
                             font='Calibri', size=18,color=(0, 0, 0))


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

