import abc
import pygame as pg


class Container(abc.ABC):
    def __init__(self, player, pos, sprite):
        self.position = pos
        self.player  = player
        self.sprite  = sprite
        self.mask    = pg.mask.from_surface(self.sprite)
        self.active  = True

    @abc.abstractmethod
    def effect(self):
        pass

    def overlap(self):
        player_mask = pg.mask.from_surface(self.player.sprite)
        offset = (
                int(self.player.position.x - self.player.sprite.get_width()  / 2 - self.position[0]),
                int(self.player.position.y - self.player.sprite.get_height() / 2 - self.position[1])
            )

        result = self.mask.overlap(player_mask, offset)
        if result and self.active:
            self.effect()
            self.active = False