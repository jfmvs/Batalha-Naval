import pygame as pg


def render_text(surface, text, pos, size, color=(0, 0, 0)):
    font = pg.font.SysFont('century', size)
    text_surface = font.render(text, True, color)
    coords = ( pos[0] - text_surface.get_width()  // 2,
               pos[1] - text_surface.get_height() // 2)
    surface.blit(text_surface, coords)


class App:
    def __init__(self):
        self._SCREEN_WIDTH     = 800
        self._SCREEN_HEIGHT    = 600
        self._SCREEN           = pg.display.set_mode((self._SCREEN_WIDTH, self._SCREEN_HEIGHT))
        self._BACKGROUND_COLOR = (0, 0, 255)
        self._CLOCK            = pg.time.Clock()
        self._running          = False
        pg.display.set_caption('Batalha Naval - Zoom')

    def _update(self, dt):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self._running = False

    def _render(self):
        render_text(self._SCREEN, 'Testando...', (400, 300), 36)

    def run(self):
        self._running = True
        while self._running:
            dt = self._CLOCK.tick(60)
            self._update(dt)
            self._SCREEN.fill(self._BACKGROUND_COLOR)
            self._render()
            pg.display.update()


def main():
    pg.init()
    app = App()
    app.run()
    pg.quit()


if __name__ == '__main__':
    main()

