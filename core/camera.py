import pygame as pg
from core.player import Player


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
        se atribuído, a câmera manterá o valor de _position como sua
        posição

    Métodos
    -------
    get_rect():
        retorna os dados da região visível do mundo

    get_pos():
        getter do atributo _position
    set_pos(x, y):
        altera o valor do atributo `_position`
    set_zoom(value):
        altera o valor do atributo `_zoom`
    zoom_in():
        aumento o valor do atributo `_zoom`
    zoom_out():
        diminui o valor do atributo `_zoom`
    get_zoom():
        retorna o valor de `_zoom`
    get_modeled(surface):
        retorna a área visível de surface como um objeto pygame.Surface
    set_focus(target):
        atribui um valor para `_target`
    update():
        o valor de _position é alterado para a posição de `_target`

    """

    _ZOOM_MIN = 0.3
    _ZOOM_MAX = 2.0

    def __init__(self, pos: (list, tuple), w: int, h: int):
        """
        Descrição
        ---------
        Inicializa a instância de Camera

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

    def get_rect(self):
        """
        Descrição
        ---------
        Retorna os dados da região visível do mundo para serem usados
        como um objeto pygame.Rect

        Retorno
        -------
        tuple

        """

        return (
            self.get_pos()[0] - self._width // 2,
            self.get_pos()[1] - self._height // 2,
            self._width, self._height
        )

    def get_pos(self):
        """
        Descrição
        ---------
        Getter para o atributo `_position`

        Retorno
        -------
        list
        """

        return self._position

    def set_pos(self, x: int, y: int):
        """
        Descrição
        ---------
        Setter para o atributo `_position`

        Parâmetros
        ----------
        x : int
            valor para o componente x do atributo `_position`
        y : int
            valor para o componente y do atributo `_position`

        Retorno
        -------
        None

        """

        self._position[0] = x
        self._position[1] = y

    def set_zoom(self, value: float):
        """
        Descricção
        ----------
        Setter para o atributo `_zoom`. Mantém o valor dentro do limite
        [`_ZOOM_MIN`, `_ZOOM_MAX`].

        Parâmetro
        ---------
        value : float
            novo valor para o atributo `_zoom`

        Retorno
        -------
        None

        """

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
        Aumenta o valor do atributo `_zoom` em um valor constante

        Retorno
        -------
        None

        """

        self.set_zoom(self._zoom + 0.01)

    def zoom_out(self):
        """
        Descrição
        ---------
        Diminui o valor do atributo `_zoom` em um valor constante

        Retorno
        -------
        None

        """

        self.set_zoom(self._zoom - 0.01)

    def get_zoom(self):
        """
        Descrição
        ---------
        Getter para o atributo `_zoom`

        Retorno
        -------
        float

        """

        return self._zoom

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
            int(surface.get_width()  * self.get_zoom()),
            int(surface.get_height() * self.get_zoom())
        ))
        modeled.blit(tmp, (0, 0), self.get_rect())
        return modeled

    def set_focus(self, target: Player):
        """
        Descrição
        ---------
        Setter para o atributo `_target`

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
        mantido como centro da janela se houver um valor atribuído ao
        atributo `_target`

        Retorno
        -------
        None

        """

        if self._target:
            self.set_pos(
                self._target.get_center()[0] * self.get_zoom(),
                self._target.get_center()[1] * self.get_zoom()
            )
