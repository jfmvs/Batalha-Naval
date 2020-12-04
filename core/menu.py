import pygame as pg
from .sprite_manager import SpriteManager
from .renderer import Renderer

class Menu:
    def __init__(self, player):
        SpriteManager.load('menu', 'assets/menu.PNG')
        SpriteManager.load('azul', 'assets/azul.png')
        SpriteManager.load('verde', 'assets/verde.png')

        self.player = player

    def transformando(self):
        escala_vida = 137 / self.player.vidaTotal
        vida        = int(escala_vida * self.player.vidaAtual)
        escalaXP    = 140 / self.player.xpNecessaria
        barraxp     = int(escalaXP * self.player.xp)

        SpriteManager.resize('verde', (vida, 18))

        try:
            if self.player.xp <= self.player.xpNecessaria:
                SpriteManager.resize('azul', (barraxp or 1, 20))
            else:
                SpriteManager.resize('azul', (140, 20))
        except ValueError:
            pass

    def status(self):
        if type(self.player.health) == int:
            self.player.vidaTotal = 100 + 20 * self.player.health
        if type(self.player.nivelTotal) == int:
            self.player.xpNecessaria = 100 + 10 * self.player.nivelTotal
        else:
            self.player.maximo = True

        if self.player.power == 5:
            self.player.power = 'MAX'
        if self.player.calibre == 4:
            self.player.calibre = 'MAX'
        if self.player.health == 7:
            self.player.health = 'MAX'
        if self.player.gun_count == 3:
            self.player.gun_count = 'MAX'
        if self.player.nivelTotal == 19:
            self.player.nivelTotal = 'MAX'

    def update(self, event):
        if self.player.xp >= self.player.xpNecessaria:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_u:
                    if type(self.player.power) == int:
                        self.player.level_up()
                        self.player.power += 1
                elif event.key == pg.K_i:
                    if type(self.player.calibre) == int:
                        self.player.level_up()
                        self.player.calibre += 1
                elif event.key == pg.K_o:
                    if type(self.player.health) == int:
                        self.player.level_up()
                        self.player.vidaAtual += 20
                        self.player.health += 1
                elif event.key == pg.K_p:
                    if type(self.player.gun_count) == int:
                        self.player.level_up()
                        self.player.gun_count += 1

        self.transformando()
        self.status()

    def render(self, surface):
        Renderer.render_sprite(surface, SpriteManager.get('menu'), (400, 70), centered=True)
        surface.blit(SpriteManager.get('verde'), (149, 31))
        surface.blit(SpriteManager.get('azul'), (148, 80))

        Renderer.render_text(surface, f'{self.player.calibre}',    (418, 73), font='Calibri', size=18, color=(0, 0, 0))
        Renderer.render_text(surface, f'{self.player.power}',      (410, 31), font='Calibri', size=18, color=(0, 0, 0))
        Renderer.render_text(surface, f'{self.player.health}',     (538, 31), font='Calibri', size=18, color=(0, 0, 0))
        Renderer.render_text(surface, f'{self.player.gun_count}',  (530, 74), font='Calibri', size=18, color=(0, 0, 0))
        Renderer.render_text(surface, f'{self.player.nivelTotal}', (352, 13), font='Calibri', size=18, color=(0, 0, 0))

        if self.player.maximo is False:
            Renderer.render_text(surface, f'{self.player.xp}/{self.player.xpNecessaria}',
                                 (180, 60), font='Calibri',  size=18, color=(0, 0, 0))

            if self.player.xp >= self.player.xpNecessaria:
                Renderer.render_text(
                    surface, 'Você pode melhorar um atributo!', (370, 12), font='Calibri', size=17, color=(0, 0, 0)
                )
                if type(self.player.power) == int:
                    Renderer.render_text(surface, '[Press U]', (402,  52),  font='Calibri', size=16, color=(0, 0, 0))
                if type(self.player.calibre) == int:
                    Renderer.render_text(surface, '[Press I]', (410, 102), font='Calibri', size=16, color=(0, 0, 0))
                if type(self.player.health) == int:
                    Renderer.render_text(surface, '[Press O]', (525,  52), font='Calibri', size=16, color=(0, 0, 0))
                if type(self.player.gun_count) == int:
                    Renderer.render_text(surface, '[Press P]', (536, 100), font='Calibri', size=16, color=(0, 0, 0))
        else:
            Renderer.render_text(surface, 'MAXIMO ATINGIDO', (180, 60), font='Calibri', size=16, color=(0, 0, 0))

        Renderer.render_text(surface, f'{self.player.vidaAtual}/{self.player.vidaTotal}',
                             (178, 11), font='Calibri', size=18, color=(0, 0, 0))

