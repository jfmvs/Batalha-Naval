import pygame as pg
from .ship import Ship


class Camera:
    """
    Descrição
    ---------
    O estado da classe altera a forma como um objeto é renderizado para
    melhor o representar no mundo

    Atributos
    ---------
    _ZOOM_MIN : float
        a menor valor aceitável para a escala
    _ZOOM_MAX : float
        o maior valor aceitável para a escala
    _position : list[float]
        a posição central da câmera
    _zoom : float
        escala de um objeto renderizável

    Propriedades
    ------------
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
    get_modeled(renderable):
        retorna uma superfície com as alterações necessárias para renderizar
        `renderable`
    """

    _ZOOM_MIN = 0.3
    _ZOOM_MAX = 2.0

    def __init__(self, pos: (list, tuple), zoom=1.0):
        """
        Descrição
        ---------
        Inicializa uma instância de Camera

        Parâmetros
        ----------
        pos : list, tuple
            posição central da câmera no mundo
        zoom : float, opcional
            a escala dos objetos renderizáveis (default  1.0)
        """

        self._position = pg.Vector2(pos)
        self._zoom     = zoom

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position.x = value[0]
        self._position.y = value[1]

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

    def get_modeled(self, renderable):
        """
        Descrição
        ---------
        Retorna um objeto pygame.Surface que representa como `renderable` deve
        ser renderizado na tela

        Parâmetro
        ---------
        renderable : any
            um objeto a ser renderizado

        Retorno
        -------
        pygame.Surface
        """
        if isinstance(renderable, Ship):
            modeled = pg.transform.scale(renderable.sprite, (
                int(renderable.sprite.get_width()  * self.zoom),
                int(renderable.sprite.get_height() * self.zoom)
            ))
            modeled = pg.transform.rotate(modeled, renderable.angle)
            return modeled
