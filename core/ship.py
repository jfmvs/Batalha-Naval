import sys
import pygame as pg
from pygame import gfxdraw


class Ship:
    """
    Descrição
    ------
    A classe encapsula a lógica do movimento e renderização dos navios.

    Atributos
    ---------
    _position : pygame.Vector2
        posição central do navio
    _speed : int
        taxa de mudança de posição em pixel/s
    _angle : float
        ângulo da direção do navio com o eixo x
    _sprite : pygame.Surface
        objeto para renderizar a imagem que representa o navio

    Propriedades
    ------------
    direction : pygame.Vector2
        retorna a direção do movimento do navio
    angle : float
        retorna o valor de `_angle`
    position : pygame.Vector2
        retorna o valor de `_position`
    center : pygame.Vector2
        retorna as coordenadas do centro do navio

    Métodos
    -------
    update(dt):
        muda a posição do navio
    rotate(angle):
        muda o ângulo do navio
    draw(surface):
        renderiza o navio no objecto pygame.Surface especificado
    """

    def __init__(self, pos: (list, tuple, pg.Vector2), sprite: pg.Surface, speed: int = 250, angle: float = 0):
        """
        Descrição
        ---------
        Inicializa uma instância de Ship

        Parâmetros
        ----------
        pos : list, tuple, pygame.Vector2
            posição central do navio
        speed : int, opcional
            taxa de mudança de posição do navio em pixel/s
            (default 250)
        angle : float, opcional
            ângulo do navio com o eixo x (default 0)
        """
        self._position = pg.Vector2(*pos)
        self._speed    = speed
        self._angle    = angle
        self._sprite   = sprite

    @property
    def direction(self):
        direction = pg.Vector2(-1.0, 0.0)
        direction.rotate_ip(self._angle)
        return direction

    @property
    def angle(self):
        return self._angle

    @property
    def position(self):
        return self._position

    @property
    def center(self):
        return self._position.x, self._position.y

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value: pg.Surface):
        self._sprite = value

    def update(self, dt: float):
        """
        Descrição
        ------
        Altera a posição do navio

        Parâmetros
        ----------
        dt : float
            variação de tempo

        Retorno
        -------
        None
        """
        self._position += self.direction * self._speed * dt

    def rotate(self, angle: float):
        """
        Descrição
        ---------
        Altera o ângulo do navio com o eixo x

        Parâmetros
        ----------
        angle : float
            variação do ângulo do navio

        Retorno
        -------
        None
        """
        self._angle += angle
        self._angle = self._angle % 360

    def draw(self, surface: pg.Surface):
        """
        Descrição
        ---------
        Renderiza `_sprite` na superfície dada como parâmetro. No modo
        debug, também renderiza uma linha representante da direção.

        Parâmetros
        ----------
        surface : pygame.Surface
            superfície onde o navio deve ser renderizado

        Retorno
        -------
        None
        """
        modeled = pg.transform.rotate(self._sprite, -self._angle)
        coords = (self._position.x - modeled.get_width() // 2, self._position.y - modeled.get_height() // 2)
        surface.blit(modeled, coords)

        if '-o' not in sys.argv:
            length = 40
            coord1 = self._position.x, self._position.y
            coord2 = int(coord1[0] + self.direction.x * length), int(coord1[1] + self.direction.y * length)
            coord1 = int(coord1[0]), int(coord1[1])
            pg.gfxdraw.line(surface, *coord1, *coord2, (223, 32, 203))
