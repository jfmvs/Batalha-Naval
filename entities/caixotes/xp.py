from .container import Container

class XPContainer(Container):
    XP_AWARDS = {
        1: 20,
        2: 100,
        3: 500
    }


    def __init__(self, player, pos, sprite, stage=1):
        super().__init__(player, pos, sprite)
        self.content = XPContainer.XP_AWARDS[stage]
    def effect(self):
        self.player.xp += self.content
