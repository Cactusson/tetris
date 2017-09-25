import pygame as pg

from .. import tools, prepare
from ..components.animations import Animation
from ..components.label import Label
from ..components.buttonsystem import ButtonSystem
# from ..components.task import Task


class Controls(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.basic_image = self.make_image()
        self.rect = self.basic_image.get_rect(
            center=prepare.SCREEN_RECT.center)
        self.update_button_system()
        self.update_image()
        self.last_image = None
        self.animations = pg.sprite.Group()
        self.play = False

    def start(self, image, rect):
        self.button_system.start()
        self.update_image()
        self.play = False
        self.last_image = pg.sprite.Sprite()
        self.last_image.image = image
        self.last_image.rect = rect
        self.rect.left = self.last_image.rect.right + 300
        animation = Animation(
            x=self.last_image.rect.x - self.last_image.rect.width - 500,
            y=self.rect.y, duration=1000, round_values=True)
        animation.callback = self.set_play
        animation.start(self.last_image.rect)
        self.animations.add(animation)
        animation = Animation(
            x=100, y=self.last_image.rect.y,
            duration=1000, round_values=True)
        animation.start(self.rect)
        self.animations.add(animation)

    def make_image(self):
        width, height = 600, 500
        image = pg.Surface((width, height)).convert()
        image.fill(pg.Color('#B2704E'))
        title = Label('Quicksand-Regular', 100, 'Controls', pg.Color('black'),
                      center=(width // 2, height // 2 - 200))
        image.blit(title.image, title.rect)
        return image

    def update_button_system(self):
        buttons = []
        names = ['move_left',
                 'move_right',
                 'rotate_counterclockwise',
                 'rotate_clockwise',
                 'soft_drop',
                 'hard_drop']
        for name in names:
            buttons.append(pg.key.name(prepare.controls[name]).upper())
        buttons.append('BACK')
        self.button_system = ButtonSystem(
            self.button_call, buttons, font_size=23, gap=15)

    def button_call(self, name):
        if name == 'BACK':
            self.next = 'MENU'
            self.persist['last_image'] = self.image.copy(), self.rect.copy()
            self.done = True
        else:
            if self.button_system.active_button is None:
                return
            self.button_system.toggle_lock()
            self.update_image()

    def set_play(self):
        self.play = True

    def finish(self):
        self.next = 'GAME'
        self.done = True

    def make_labels(self):
        self.labels = pg.sprite.Group()
        names = ['Move left',
                 'Move right',
                 'Rotate counterclockwise',
                 'Rotate clockwise',
                 'Soft drop',
                 'Hard drop']
        for name, button in zip(names, self.button_system.buttons_list):
            center = (self.button_system.rect.left + button.rect.centerx - 300,
                      self.button_system.rect.top + button.rect.centery)
            label = Label('Quicksand-Regular', 20, name, pg.Color('black'),
                          center=center)
            self.labels.add(label)

    def update_image(self):
        self.image = self.basic_image.copy()
        self.button_system.rect.center = (self.rect.width // 2 + 175,
                                          self.rect.height // 2 + 50)
        self.make_labels()
        self.image.blit(self.button_system.image, self.button_system.rect)
        for label in self.labels:
            self.image.blit(label.image, label.rect)

    def change_button(self, key):
        names = ['move_left',
                 'move_right',
                 'rotate_counterclockwise',
                 'rotate_clockwise',
                 'soft_drop',
                 'hard_drop']
        index = self.button_system.buttons_list.index(
            self.button_system.active_button)
        if key not in prepare.controls.values() and pg.key.name(key) != 'f':
            prepare.controls[names[index]] = key
        self.update_button_system()
        self.button_system.start(index)

    def startup(self, current_time, persistant):
        self.start_time = current_time
        self.persist = persistant
        image, rect = self.persist['last_image']
        del self.persist['last_image']
        self.start(image, rect)

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if not self.button_system.locked:
                if event.key == pg.K_ESCAPE:
                    self.next = 'MENU'
                    self.persist['last_image'] = (self.image.copy(),
                                                  self.rect.copy())
                    self.done = True
                elif self.play:
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        self.button_system.next_button('up')
                        self.update_image()
                    elif event.key == pg.K_DOWN or event.key == pg.K_s:
                        self.button_system.next_button('down')
                        self.update_image()
                    elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                        self.button_system.press_button()
            else:
                if event.key == pg.K_ESCAPE:
                    self.button_system.toggle_lock()
                else:
                    self.change_button(event.key)
                self.update_image()

    def draw(self, surface):
        surface.fill(pg.Color('#CD9D77'))
        surface.blit(self.image, self.rect)
        if self.last_image:
            surface.blit(self.last_image.image, self.last_image.rect)

    def update(self, surface, current_time, dt):
        self.current_time = current_time
        self.animations.update(dt * 1000)
        self.draw(surface)
