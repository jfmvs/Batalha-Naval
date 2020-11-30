"""
Descrição
---------
    O pacote `core` contém as classes e funções utilizadas
    na lógica da classe `App` em main.py.

Classes
-------
    Camera
        define a região visível do mundo, que será renderizada na tela.
    Player
        define o objeto a ser controlado pelo jogador e encapsula sua
        lógica de movimentação e renderização.
    Text
        contém métodos estáticos que facilitam a renderização de texto
        em objetos pygame.Surface.
    SpriteManager
        lida com o carregamento e armazenamento de sprites para que
        possam ser reutilizados por múltiplos objetos
"""

from .camera import *
from .ship import *
from .text   import *
from .sprite_manager import *