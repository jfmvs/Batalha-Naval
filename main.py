import pygame as pg
from camera import Camera


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
        self._BACKGROUND_COLOR = (53, 54, 55)
        self._CLOCK            = pg.time.Clock()
        self._TARGET_FPS       = 60
        self._running          = False
        pg.display.set_caption('Batalha Naval - Zoom')

        self.framebuffer = pg.Surface((1600, 1200))
        self.scale = 1.0
        self.scale_limits = (0.3, 2.0)
        self.rects       = [
            (200, 100, 50, 50),
            (500, 400, 50, 50),
            (600,  10, 50, 50),
            (500, 400, 50, 50),
            ( 10, 400, 50, 50),
            (300, 350, 50, 50),
        ]
        self.player       = [375, 275, 50, 50]
        self.camera       = Camera((400, 300), 800, 600)

    def _update(self, dt, event):
        if event.type == pg.QUIT:
            self._running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._running = False

        kbd = pg.key.get_pressed()

        if kbd[pg.K_a]:
            self.player[0] -= 250 * dt
        if kbd[pg.K_d]:
            self.player[0] += 250 * dt

        if kbd[pg.K_w]:
            self.player[1] -= 250 * dt
        if kbd[pg.K_s]:
            self.player[1] += 250 * dt

        if kbd[pg.K_UP]:
            if self.scale < self.scale_limits[1]:
                self.scale += 0.01
        elif kbd[pg.K_DOWN]:
            if self.scale > self.scale_limits[0]:
                self.scale -= 0.01

        self.camera.set_pos(
            (self.player[0] + self.player[2]) * self.scale,
            (self.player[1] + self.player[3]) * self.scale
        )

    def _render(self):
        self.framebuffer.fill((57, 141, 212))
        for rect in self.rects:
            pg.draw.rect(self.framebuffer, (255, 0, 0), rect)
        pg.draw.rect(self.framebuffer, (0, 255, 0), self.player)

        self._SCREEN.blit(self.camera.get_modeled(self.framebuffer, self.scale), (0,0))

        # render_text(self._SCREEN, f'{self.camera_scale:.2f}', (30, 570), 32)

    def run(self):
        self._running = True
        while self._running:
            dt = self._CLOCK.tick(self._TARGET_FPS) / 1000
            event = pg.event.poll()
            self._update(dt, event)
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

