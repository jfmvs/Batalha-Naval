from .container import Container

class CaliberContainer(Container):
    def __init__(self, player, pos, sprite):
        super().__init__(player, pos, sprite)

    def effect(self):
        self.player.calibre += 1

