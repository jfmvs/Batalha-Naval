"""
Descrição
---------
    O pacote `core` contém as classes e funções utilizadas
    na lógica da classe `App` em main.py.

Classes
-------
    Camera
        define como objetos de jogo serão renderizados
    Ship
        define objetos que representam navios
    SpriteManager
        lida com o carregamento e armazenamento de sprites para que
        possam ser reutilizados por múltiplos objetos
    WorldManager
        divide o mundo em pedaços chamados chunks para reduzir o número
        de itens com os quais é preciso lidar
    Renderer
        contém a lógica de renderização dos objetos do jogo
"""

from .camera import *
from .ship import *
from .sprite_manager import *
from .world import *
from .renderer import *