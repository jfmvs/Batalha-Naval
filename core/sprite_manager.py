import pygame as pg


class SpriteManager:

    _sprites = {}

    @staticmethod
    def load(key: str, path: str):
        sprite = pg.image.load(path)

        if sprite.get_alpha() is None:
            sprite = sprite.convert()
        else:
            sprite = sprite.convert_alpha()

        SpriteManager._sprites[key] = sprite

    @staticmethod
    def get(key):
        return SpriteManager._sprites[key]

    @staticmethod
    def resize(key, size):
        SpriteManager._sprites[key] = pg.transform.scale(SpriteManager._sprites[key], size)

    @staticmethod
    def rescale(key, scale):
        img = SpriteManager.get(key)
        SpriteManager.resize(key, (int(img.get_width() * scale), int(img.get_height() * scale)))
