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
        self._BACKGROUND_COLOR = (53, 54, 55)
        self._CLOCK            = pg.time.Clock()
        self._TARGET_FPS       = 60
        self._running          = False
        pg.display.set_caption('Batalha Naval - Zoom')

        self.framebuffer = pg.Surface((1600, 1200))
        self.rects = [
            (200, 100, 50, 50),
            (500, 400, 50, 50),
            (600,  10, 50, 50),
            (500, 400, 50, 50),
            ( 10, 400, 50, 50),
            (300, 350, 50, 50),
        ]

        self.camera_focus       = [400, 300]
        self.camera_scale       =  1.0
        self.camera_zoom_limits = (0.1, 3.0)

        self.player_pos         = [400, 300]

    def _update(self, dt, event):
        if event.type == pg.QUIT:
            self._running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._running = False

        kbd = pg.key.get_pressed()

        if kbd[pg.K_s]:
            self.camera_focus[1] -= 250 * dt
        elif kbd[pg.K_w]:
            self.camera_focus[1] += 250 * dt
        if kbd[pg.K_d]:
            self.camera_focus[0] -= 250 * dt
        elif kbd[pg.K_a]:
            self.camera_focus[0] += 250 * dt

        if kbd[pg.K_UP]:
            if self.camera_scale < self.camera_zoom_limits[1]:
                width_before  = self.framebuffer.get_width()  * self.camera_scale
                height_before = self.framebuffer.get_height() * self.camera_scale

                self.camera_scale += 0.01

                width_now  = self.framebuffer.get_width()  * self.camera_scale
                height_now = self.framebuffer.get_height() * self.camera_scale

                self.camera_focus[0] -= (width_now  - width_before)  // 2
                self.camera_focus[1] -= (height_now - height_before) // 2

        elif kbd[pg.K_DOWN]:
            if self.camera_scale > self.camera_zoom_limits[0]:
                width_before  = self.framebuffer.get_width()  * self.camera_scale
                height_before = self.framebuffer.get_height() * self.camera_scale

                self.camera_scale -= 0.01

                width_now  = self.framebuffer.get_width()  * self.camera_scale
                height_now = self.framebuffer.get_height() * self.camera_scale

                self.camera_focus[0] += (width_before  - width_now)  // 2
                self.camera_focus[1] += (height_before - height_now) // 2

    def _render(self):

        self.framebuffer.fill((57, 141, 212))

        for rect in self.rects:
            pg.draw.rect(self.framebuffer, (255, 0, 0), rect)

        frame = pg.transform.scale(self.framebuffer, (
            int(self.framebuffer.get_width()  * self.camera_scale),
            int(self.framebuffer.get_height() * self.camera_scale)
        ))

        self._SCREEN.blit(frame, (0, 0), (
            (self._SCREEN_WIDTH  - self.camera_focus[0])  // 2,
            (self._SCREEN_HEIGHT - self.camera_focus[1])  // 2,
            self._SCREEN_WIDTH, self._SCREEN_HEIGHT
        ))
        pg.draw.rect(self._SCREEN, (0, 255, 0), (
            int(self.player_pos[0] - 25 * self.camera_scale),
            int(self.player_pos[1] - 25 * self.camera_scale),
            int(50 * self.camera_scale),
            int(50 * self.camera_scale)
        ))
        render_text(self._SCREEN, f'{self.camera_scale:.2f}', (30, 570), 32)

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

