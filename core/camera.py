import pygame as pg
from .ship import Ship


class Camera:
    """
    Descrição
    ---------
    O estado da classe determina que região do mundo será renderizada
    na janela do jogo.

    Atributos
    ---------
    _ZOOM_MIN : float
        a menor valor aceitável para a escala
    _ZOOM_MAX : float
        o maior valor aceitável para a escala
    _position : list[float]
        a posição central da câmera
    _width : int
        largura da região visível do mundo
    _height : int
        altura da região visível do mundo
    _zoom : float
        escala da região vísivel do mundo
    _target : Player, opcional
        se atribuído, a câmera manterá `_position` como sua posição

    Propriedades
    ------------
    rect : tuple
        retorna os dados da região visível do mundo
    posistion : list
        retorna o valor de `_position`
    zoom : float
        retorna o valor de `_zoom`

    Setters
    -------
    posistion:
        altera o valor de `_position`
    zoom:
        altera o valor de `_zoom`


    Métodos
    -------
    zoom_in():
        aumento o valor de `_zoom`
    zoom_out():
        diminui o valor de `_zoom`
    get_modeled(surface):
        retorna a área visível de surface como um objeto pygame.Surface
    set_focus(target):
        atribui um valor para `_target`
    update():
        `_position` é alterado para a posição de `_target`
    """

    _ZOOM_MIN = 0.3
    _ZOOM_MAX = 2.0

    def __init__(self, pos: (list, tuple), w: int, h: int):
        """
        Descrição
        ---------
        Inicializa uma instância de Camera

        Parâmetros
        ----------
        pos : list, tuple
            posição central da câmera no mundo
        w : int
            largura da região visível do mundo
        h : int
            altura da regiãp visível do mundo
        """

        self._position = list(pos)
        self._width    = w
        self._height   = h
        self._zoom     = 1.0
        self._target   = None

    @property
    def rect(self):
        return (
            self.position[0] - self._width // 2,
            self.position[1] - self._height // 2,
            self._width, self._height
        )

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: (list, tuple)):
        self._position[0] = value[0]
        self._position[1] = value[1]

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value: float):
        if value > Camera._ZOOM_MAX:
            self._zoom = Camera._ZOOM_MAX
        elif value < Camera._ZOOM_MIN:
            self._zoom = Camera._ZOOM_MIN
        else:
            self._zoom = value

    def zoom_in(self):
        """
        Descrição
        ---------
        Aumenta `_zoom` em um valor constante

        Retorno
        -------
        None
        """
        self.zoom += 0.01

    def zoom_out(self):
        """
        Descrição
        ---------
        Diminui `_zoom` em um valor constante

        Retorno
        -------
        None
        """
        self.zoom -= 0.01

    def get_modeled(self, surface: pg.Surface):
        """
        Descrição
        ---------
        Retorna um objeto pygame.Surface que representa a área visível
        do parâmetro `surface`

        Parâmetro
        ---------
        surface : pygame.Surface
            o mundo que a câmera observa e restringe

        Retorno
        -------
        pygame.Surface
        """
        modeled = pg.Surface((self._width, self._height))
        tmp = pg.transform.scale(surface, (
            int(surface.get_width()  * self.zoom),
            int(surface.get_height() * self.zoom)
        ))
        modeled.blit(tmp, (0, 0), self.rect)
        return modeled

    def set_focus(self, target: Ship):
        """
        Descrição
        ---------
        Setter para `_target`

        Retorno
        -------
        None
        """
        self._target = target

    def update(self):
        """
        Descrição
        ---------
        Altera a posição da câmera para que centro de `_target` seja
        mantido como centro da janela se houver um valor atribuído a
        `_target`

        Retorno
        -------
        None
        """
        if self._target:
            self.position[0] = self._target.center[0] * self.zoom
            self.position[1] = self._target.center[1] * self.zoom
