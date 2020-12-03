from .container import Container


class PowerContainer(Container):
    def __init__(self, player, pos, sprite):
        super().__init__(player, pos, sprite)

    def effect(self):
        self.player.power += 1
