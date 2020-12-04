from .container import Container

class HPContainer(Container):
    def __init__(self, player, pos, sprite):
        super().__init__(player, pos, sprite)

    def effect(self):
        self.player.vidaAtual = min([self.player.vidaAtual + 10, self.player.vidaTotal])
