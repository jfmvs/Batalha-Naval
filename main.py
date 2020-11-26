import pygame as pg
from camera import Camera
from text   import Text


class App:
    def __init__(self):
        self._SCREEN_WIDTH     = 800
        self._SCREEN_HEIGHT    = 600
        self._SCREEN           = pg.display.set_mode((self._SCREEN_WIDTH, self._SCREEN_HEIGHT))
        self._BACKGROUND_COLOR = (53, 54, 55)
        self._CLOCK            = pg.time.Clock()
        self._TARGET_FPS       = 60
        self._running          = False
        self._current_fps      = 60
        pg.display.set_caption('Batalha Naval - Zoom')

        self.framebuffer = pg.Surface((1600, 1200))
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
            self.camera.zoom_in()
        elif kbd[pg.K_DOWN]:
            self.camera.zoom_out()

        self.camera.set_pos(
            (self.player[0] + self.player[2]) * self.camera.get_zoom(),
            (self.player[1] + self.player[3]) * self.camera.get_zoom()
        )

    def _render(self):
        self.framebuffer.fill((57, 141, 212))
        for rect in self.rects:
            pg.draw.rect(self.framebuffer, (255, 0, 0), rect)
        pg.draw.rect(self.framebuffer, (0, 255, 0), self.player)

        self._SCREEN.blit(self.camera.get_modeled(self.framebuffer), (0,0))

        Text.render(self._SCREEN, 'camera pos:      x: {:.2f},     y: {:.2f}'.format(
            self.camera.get_pos()[0], self.camera.get_pos()[1]
        ), (10, 5), 16, color=(255,255,255))
        Text.render(self._SCREEN, f'scale: {self.camera.get_zoom():.2f}', (10, 20), 16, color=(255,255,255))
        Text.render(self._SCREEN, f'fps: {self._current_fps:}', (10, 40), 16, color=(255,255,255))

    def run(self):
        self._running = True
        while self._running:
            dt = self._CLOCK.tick(self._TARGET_FPS) / 1000
            self._current_fps = int(1 / dt)
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

