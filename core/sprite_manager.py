import pygame as pg


class SpriteManager:
    """
    Descrição
    ---------
    A classe SpriteManager serve para carregar e armazenar sprites como
    objetos pygame.Surface de forma que outros objetos do jogo possam
    acessar tais sprites através de referências no lugar de instâncias.

    Atributos
    ---------
    _sprites : dict
        um dicionário str-pygame.Surface que armazena as sprites

    Métodos
    -------
    load(key, path):
        carrega a sprite em no caminho `path` e a adiciona a `_sprites`
        usando a chave `key`
    get(key):
        retorna a sprite com chave `key`
    resize(key, size):
        muda o tamanho da sprite com chave `key`
    rescale(key, scale):
        reescala a sprite com chave `key`
    """

    _sprites = {}

    @staticmethod
    def load(key: str, path: str):
        """
        Descrição
        ---------
            Carrega uma sprite e a adiciona a `_sprites`, convertendo-a
            dependendendo de seu componente alpha

        Parâmetros
        ----------
        key : str
            chave sob a qual a sprite serà armazenada
        path : str
            caminho para a sprite

        Retorno
        -------
        None
        """
        sprite = pg.image.load(path)

        if sprite.get_alpha() is None:
            sprite = sprite.convert()
        else:
            sprite = sprite.convert_alpha()

        SpriteManager._sprites[key] = sprite

    @staticmethod
    def get(key):
        """
        Descrição
        ---------
        Retorna a sprite de chave `key`

        Parâmetros
        ----------
        key : str
            chave sob a qual a sprite está armazenada

        Retorno
        -------
        pygame.Surface
        """
        return SpriteManager._sprites[key]

    @staticmethod
    def resize(key, size):
        """
        Descrição
        ---------
        Muda o tamanho da imagem de chave `key` para o tamanho `size`

        Parâmetros
        ----------
        key : str
            chave sob a qual a sprite foi armazenada
        size : list, tuple
            novo tamanho em pixels para a sprite

        Retorno
        -------
        None
        """
        SpriteManager._sprites[key] = pg.transform.scale(SpriteManager._sprites[key], size)

    @staticmethod
    def rescale(key, scale):
        """
        Descrição
        ---------
        Reescale a sprite de chave `key` de acordo com `scale`

        Parâmetros
        ----------
        key : str
            chave sob a qual a sprite foi armazenada
        scale : float
            fator pelo qual o tamanho original da imagem de chave `key`
            é multiplicado para determinar seu novo tamanho

        Retorno
        -------
        None
        """
        img = SpriteManager.get(key)
        SpriteManager.resize(key, (int(img.get_width() * scale), int(img.get_height() * scale)))