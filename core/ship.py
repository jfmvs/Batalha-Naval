import sys
import pygame as pg
from pygame import gfxdraw


class Ship:
    """
    Descrição
    ------
    A classe encapsula a lógica de movimento dos navios.

    Atributos
    ---------
    _position : pygame.Vector2
        posição central do navio
    _sprite : pygame.Surface
        referência a usado para renderizar a imagem que representa o
        navio
    _speed : int
        taxa de mudança de posição em pixel/s
    _angle : float
        ângulo da direção do navio com o eixo x
    _angular_speed : float
        taxa de mudança de ângulo em grau/s

    Propriedades
    ------------
    direction : pygame.Vector2
        retorna a direção do movimento do navio
    angle : float
        retorna o valor de `_angle`
    position : pygame.Vector2
        retorna o valor de `_position`
    speed : float
        retorna o valor de `_speed`
    angular_speed : float
        retorna o valor de `_angular_speed`

    Métodos
    -------
    move(dt):
        muda a posição do navio
    rotate(dt, reverse):
        muda o ângulo do navio
    """

    def __init__(self, pos: (list, tuple, pg.Vector2), sprite: pg.Surface, **kwargs):
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
        self._position         = pg.Vector2(*pos)
        self._original_sprite  = sprite
        self._speed            = kwargs.get('speed', 250)
        self._angle            = kwargs.get('angle', 0)
        self._angular_speed    = kwargs.get('angular_speed', 150)
        self._render_sprite    = pg.transform.rotate(self._original_sprite, self._angle)

    @property
    def direction(self):
        direction = pg.Vector2(1.0, 0.0)
        direction.rotate_ip(self._angle)
        return direction

    @property
    def angle(self):
        return self._angle

    @property
    def position(self):
        return self._position

    @property
    def speed(self):
        return self._speed

    @property
    def angular_speed(self):
        return self._angular_speed

    @property
    def sprite(self):
        return self._render_sprite

    def move(self, dt: float):
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
        self._position.x += self.direction.x * self._speed * dt
        self._position.y -= self.direction.y * self._speed * dt

    def rotate(self, dt: float, reverse: bool = False):
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
        mod = -1 if reverse else 1
        self._angle += self._angular_speed * mod * dt
        self._angle %= 360

        self._render_sprite = pg.transform.rotate(self._original_sprite, self._angle)

