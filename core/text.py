import pygame as pg


class Text:
    """
    Descrição
    ---------
    Classes com funções ajudantes para renderizar texto

    Métodos
    -------
    render(surface, text, pos, size, color):
        Rendereiza texto usando a posição `pos` como canto superior
        esquerdo
    render_centered(surface, text, pos, size, color):
        Renderiza texto usando a posição `pos` como centro do texto
    """

    @staticmethod
    def render(surface: pg.Surface, text: str, pos: (list, tuple), size: int, color: (list, tuple)=(0, 0, 0)):
        """
        Descrição
        ---------
        Renderiza texto em um objeto pygame.Surface usando o parâmetro
        `pos` como canto superior esquerdo da região onde o texto é
        renderizado

        Parâmetros
        ----------
        surface : pygame.Surface
            objeto onde o texto será renderizado
        text : str
            texto a ser renderizado
        pos : list, tuple
            canto superior esquerdo da região onde o texto é
            renderizado
        size : int
            tamanho da fonte
        color : list, tuple, opcional
            cor da fonte (default (0,0,0))

        Retorno
        -------
        None

        """

        font = pg.font.SysFont('times new roman', size)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)

    @staticmethod
    def render_centered(surface: pg.Surface, text: str, pos: (list, tuple), size: int, color: (list, tuple)=(0, 0, 0)):
        """
        Descrição
        ---------
        Renderiza texto em um objeto pygame.Surface usando o parâmetro
        `pos` como centro da região onde o texto é renderizado

        Parâmetros
        ----------
        surface : pygame.Surface
            objeto onde o texto será renderizado
        text : str
            texto a ser renderizado
        pos : list, tuple
            canto superior centro da região onde o texto é
        renderizado
        size : int
            tamanho da fonte
        color : list, tuple, opcional
            cor da fonte (default (0,0,0))

        Retorno
        -------
        None

        """

        font = pg.font.SysFont('times new roman', size)
        text_surface = font.render(text, True, color)
        coords = (pos[0] - text_surface.get_width() // 2,
                  pos[1] - text_surface.get_height() // 2)
        surface.blit(text_surface, coords)

