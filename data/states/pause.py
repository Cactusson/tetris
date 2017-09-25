import pygame as pg

from .. import tools, prepare
from ..components.label import Label
from ..components.buttonsystem import ButtonSystem


class Pause(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.cover = self.make_cover_image()
        self.basic_image = self.make_image()
        self.rect = self.basic_image.get_rect(
            center=prepare.SCREEN_RECT.center)
        self.button_system = ButtonSystem(
            self.button_call, ['RESUME', 'SETTINGS', 'QUIT'])
        self.update_image()

    def start(self):
        self.button_system.start()
        self.update_image()

    def make_cover_image(self):
        cover = pg.Surface(prepare.SCREEN_SIZE).convert()
        cover.set_alpha(200)
        return cover

    def make_image(self):
        width = 400
        height = 400
        image = pg.Surface((width, height)).convert()
        image.fill(pg.Color('#B2704E'))
        title = Label('Quicksand-Regular', 30, 'PAUSE', pg.Color('black'),
                      center=(width // 2, 50))
        image.blit(title.image, title.rect)
        return image

    def update_image(self):
        self.image = self.basic_image.copy()
        self.button_system.rect.center = (self.rect.width // 2,
                                          self.rect.height // 2)
        self.image.blit(self.button_system.image, self.button_system.rect)

    def button_call(self, name):
        if name == 'RESUME':
            self.next = 'GAME'
            self.done = True
        elif name == 'SETTINGS':
            self.next = 'SETTINGS'
            self.done = True
        if name == 'QUIT':
            self.persist['quit'] = True
            self.next = 'GAME'
            self.done = True

    def startup(self, current_time, persistant):
        self.start_time = current_time
        self.persist = persistant
        if self.previous == 'GAME':
            self.subscreen = self.persist['screen']
            del self.persist['screen']
        screen = pg.display.get_surface()
        screen.blit(self.subscreen, (0, 0))
        screen.blit(self.cover, (0, 0))
        self.start()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next = 'GAME'
                self.done = True
            elif event.key == pg.K_UP or event.key == pg.K_w:
                self.button_system.next_button('up')
                self.update_image()
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                self.button_system.next_button('down')
                self.update_image()
            elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                self.button_system.press_button()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, surface, current_time, dt):
        self.current_time = current_time
        self.draw(surface)
