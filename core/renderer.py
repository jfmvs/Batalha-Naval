import pygame as pg
from .ship import Ship
from .camera import Camera


class Renderer:
    """
    Descrição
    ---------
    Renderer encapsula a lógica de renderização

    Atributos
    ---------
    _debug_font : pygame.Font
        guarda um obejto pygame.Font para a renderizar as mensagens de
        debug de App

    Métodos
    -------
    init():
        inicializa oos itens do estado de Renderer
    render_debug_msg(surface, msg, pos, centered, color):
        renderiza mensagens de debug em `surface`
    render_ship(surface, ship, camera):
        renderiza uma navio em `surface`
    """
    _debug_font = None

    @staticmethod
    def init():
        """
        Descrição
        ---------
        Inicializa os membros do estado de `Renderer`

        Retorno
        -------
        None
        """
        Renderer._debug_font = pg.font.SysFont('times new roman', 16)

    @staticmethod
    def render_debug_msg(surface, msg, pos, centered=False, color=(255, 255, 255)):
        """
        Descrição
        ---------
        Renderiza texto com a fonte específicada no estado em `surface`

        Parâmetros
        ----------
        surface : pygame.Surface
            superfície onde o texto será renderizado
        msg : str
            texto a ser renderizado
        pos : list, tuple
            posição onde o text será renderizado
        centered : bool, opcional
            bool que determina se `pos` será tratado como canto
            superior esquerdo ou posição central do texto
            (default False)
        color : list, tuple, opcional
            cor com a qual o texto é renderizado
            (default (255, 255, 255))

        Retorno
        -------
        None
        """
        text_surface = Renderer._debug_font.render(msg, True, color)
        coords = pos
        if centered:
            coords = (pos[0] - text_surface.get_width() // 2,
                      pos[1] - text_surface.get_height() // 2)
        surface.blit(text_surface, coords)

    @staticmethod
    def render_ship(surface, ship: Ship, camera: (Camera, None) = None):
        """
        Descrição
        ---------
        Renderiza um objeto Ship em `surface`

        Parâmetros
        ----------
        surface : pygame.Surface
            surperfície onde o navio será renderizado
        ship : Ship
            navio a ser renderizado
        camera : Camera, None, opcional
            camera que alterará a forma como `ship` é renderizado
            (default  None)

        Retorno
        -------
        None
        """

        rotated = pg.transform.rotate(ship.sprite, ship.angle)

        if camera is not None:
            surface.blit(rotated, (
                (ship.position.x - rotated.get_width()  // 2) - (camera.position.x - surface.get_width()  // 2),
                (ship.position.y - rotated.get_height() // 2) - (camera.position.y - surface.get_height() // 2),
            ))
        else:
            surface.blit(rotated, (
                ship.position.x - rotated.get_width() // 2,
                ship.position.y - rotated.get_height() // 2,
            ))
