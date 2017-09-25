import pygame as pg

from .. import tools, prepare
from ..components.label import Label
from ..components.buttonsystem import ButtonSystem
from ..components.hstable import HSTable


class RestartMenu(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.basic_image = self.make_image()
        self.rect = self.basic_image.get_rect(
            center=(prepare.SCREEN_RECT.centerx - 150,
                    prepare.SCREEN_RECT.centery))
        self.hstable = HSTable(23)
        self.button_system = ButtonSystem(
            self.button_call, ['RESTART', 'QUIT'], font_size=22, gap=20)
        self.update_image()

    def start(self):
        self.button_system.start()
        self.hstable.update_image()
        self.update_image()

    def make_image(self):
        width = 250
        height = 450
        image = pg.Surface((width, height)).convert()
        image.fill(pg.Color('#B2704E'))
        # image.fill(pg.Color('#CD9D77'))
        title = Label('Quicksand-Regular', 30, 'Restart?', pg.Color('black'),
                      center=(width // 2, 50))
        image.blit(title.image, title.rect)
        return image

    def update_image(self):
        self.image = self.basic_image.copy()
        self.hstable.rect.center = (self.rect.width // 2,
                                    self.rect.height // 2 - 50)
        self.image.blit(self.hstable.image, self.hstable.rect)
        self.button_system.rect.center = (self.rect.width // 2,
                                          self.rect.height // 2 + 130)
        self.image.blit(self.button_system.image, self.button_system.rect)

    def button_call(self, name):
        if name == 'QUIT':
            self.persist['quit'] = True
        self.next = 'GAME'
        self.done = True

    def startup(self, current_time, persistant):
        self.start_time = current_time
        self.persist = persistant
        self.start()
        result = self.persist['result']
        del self.persist['result']
        self.hstable.get_result(result, True)
        self.update_image()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.persist['quit'] = True
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
            elif event.key == pg.K_k:
                print(self.hstable.rect, self.button_system.rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, surface, current_time, dt):
        self.current_time = current_time
        self.draw(surface)
