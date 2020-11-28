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
        indica a direção do movimento do navio

    Métodos
    -------
    update(dt):
        muda a posição do navio
    rotate(dt, angle):
        muda o ângulo do navio
    get_angle():
        retorna o ângulo do navio
    get_pos():
        retorna a posição do navio
    get_center():
        retorna a posição central do navio
    draw(surface):
        renderiza o navio no objecto pygame.Surface especificado

    """

    def __init__(self, pos: (list, tuple, pg.Vector2), speed: int = 250, angle: float = 0):
        """
        Descrição
        ---------
        Inicializa a instância da classe Ship

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
        self._speed = speed
        self._angle = angle
        self._sprite = pg.image.load('assets/player.png').convert_alpha()
        self._sprite = pg.transform.scale(self._sprite, (120, 20))

    @property
    def direction(self):
        direction = pg.Vector2(1.0, 0.0)
        direction.rotate_ip(self._angle)
        return direction

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

    def rotate(self, dt: float, angle: float):
        """
        Descrição
        ---------
        Altera o ângulo do navio com o eixo x

        Parâmetros
        ----------
        dt : float
            variação de tempo
        angle : float
            variação do ângulo do navio

        Retorno
        -------
        None

        """

        self._angle += angle * dt
        self._angle = self._angle % 360

    def get_angle(self):
        """
        Descrição
        ---------
        Getter para o atributo `_angle`

        Retorno
        -------
        float

        """

        return self._angle

    def get_pos(self):
        """
        Descrição
        ---------
        Getter para o atributo `_position`

        Retorno
        -------
        pygame.Vector2

        """

        return self._position

    def get_center(self):
        """
        Descrição
        ---------
        Retorna a posição do centro do navio

        Retorno
        -------
        pygame.Vector2

        """

        return self._position.x, self._position.y

    def draw(self, surface: pg.Surface):
        """
        Descrição
        ---------
        Renderiza o objeto do atributo _sprite na superfície dada como
        parâmetro. No modo debug, também renderiza uma linha
        representante da direção

        Parâmetros
        ----------
        surface : pygame.Surface
            superfície onde o navio deve ser renderizado

        Retorno
        -------
        None

        """

        modeled = pg.transform.flip(self._sprite, True, False)
        modeled = pg.transform.rotate(modeled, -self._angle)
        coords = (self._position.x - modeled.get_width() // 2, self._position.y - modeled.get_height() // 2)
        surface.blit(modeled, coords)

        if '-o' not in sys.argv:
            length = 40
            coord1 = self._position.x, self._position.y
            coord2 = int(coord1[0] + self.direction.x * length), int(coord1[1] + self.direction.y * length)
            coord1 = int(coord1[0]), int(coord1[1])
            pg.gfxdraw.line(surface, *coord1, *coord2, (223, 32, 203))
