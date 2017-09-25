import pygame as pg

from .. import tools, prepare
from ..components.animations import Animation
from ..components.label import Label
from ..components.buttonsystem import ButtonSystem
from ..components.hstable import HSTable


class HighScore(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.basic_image = self.make_image()
        self.rect = self.basic_image.get_rect(
            center=prepare.SCREEN_RECT.center)
        self.hstable = HSTable(30)
        self.button_system = ButtonSystem(
            self.button_call, ['BACK', 'CLEAR'], font_size=25, gap=30)
        self.update_image()
        self.last_image = None
        self.animations = pg.sprite.Group()
        self.play = False

    def start_from_menu(self, image, rect):
        self.play = False
        self.last_image = pg.sprite.Sprite()
        self.last_image.image = image
        self.last_image.rect = rect
        self.rect.left = self.last_image.rect.right + 500
        animation = Animation(
            x=self.last_image.rect.x - self.last_image.rect.width - 500,
            y=self.rect.y, duration=1000, round_values=True)
        animation.callback = self.set_play
        animation.start(self.last_image.rect)
        self.animations.add(animation)
        animation = Animation(
            x=self.last_image.rect.x, y=self.last_image.rect.y,
            duration=1000, round_values=True)
        animation.start(self.rect)
        self.animations.add(animation)

    def set_play(self):
        self.play = True

    def make_image(self):
        width, height = 400, 500
        image = pg.Surface((width, height)).convert()
        image.fill(pg.Color('#B2704E'))
        title = Label('Quicksand-Regular', 60, 'HIGH SCORE', pg.Color('black'),
                      center=(width // 2, height // 2 - 200))
        image.blit(title.image, title.rect)
        return image

    def update_image(self):
        self.image = self.basic_image.copy()
        self.hstable.rect.center = (self.rect.width // 2,
                                    self.rect.height // 2 - 25)
        self.image.blit(self.hstable.image, self.hstable.rect)
        self.button_system.rect.center = (self.rect.width // 2,
                                          self.rect.height // 2 + 185)
        self.image.blit(self.button_system.image, self.button_system.rect)

    def button_call(self, name):
        if name == 'BACK':
            self.next = 'MENU'
            self.persist['last_image'] = self.image.copy(), self.rect.copy()
            self.done = True
        elif name == 'CLEAR':
            self.hstable.clear()
            self.update_image()

    def startup(self, current_time, persistant):
        self.start_time = current_time
        self.persist = persistant
        self.hstable.update_image()
        self.update_image()
        image, rect = self.persist['last_image']
        del self.persist['last_image']
        self.start_from_menu(image, rect)

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if self.play:
                if event.key == pg.K_ESCAPE:
                    self.next = 'MENU'
                    self.persist['last_image'] = (self.image.copy(),
                                                  self.rect.copy())
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
        surface.fill(pg.Color('#CD9D77'))
        surface.blit(self.image, self.rect)
        if self.last_image:
            surface.blit(self.last_image.image, self.last_image.rect)

    def update(self, surface, current_time, dt):
        self.current_time = current_time
        self.animations.update(dt * 1000)
        self.draw(surface)
