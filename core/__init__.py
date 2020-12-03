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
    Renderer
        contém a lógica de renderização dos objetos do jogo
"""

from .camera import *
from .ship import *
from .sprite_manager import *
from .renderer import *
from .player import *
from .bullet_manager import BulletManager
from .npc import *