import pygame as pg

from .. import prepare
from .buttonsystem import ButtonSystem
from .label import Label
from .volumebar import VolumeBar


class SettingsModule(pg.sprite.Sprite):
    def __init__(self, button_call):
        pg.sprite.Sprite.__init__(self)
        self.empty_image = self.make_empty_image()
        self.rect = self.empty_image.get_rect()
        self.button_call = button_call
        self.button_system = None
        self.volume_bar = None
        self.state = None
        self.start()

    def start(self):
        if self.state == 'SOUND':
            index = 0
        elif self.state == 'CONTROLS':
            index = 1
        else:
            index = 0
        self.state = 'MAIN'
        self.title = Label(
            'Quicksand-Regular', 60, 'SETTINGS', pg.Color('black'),
            center=(self.rect.width // 2, self.rect.height // 2 - 200))
        self.button_system = ButtonSystem(
            self.button_call, ['SOUND', 'CONTROLS', 'BACK'],
            font_size=25, gap=30)
        self.button_system.start(index)
        self.button_system.rect.center = (self.rect.width // 2,
                                          self.rect.height // 2)
        self.volume_bar = None
        self.update_image()

    def make_empty_image(self):
        width, height = 600, 500
        image = pg.Surface((width, height)).convert()
        image.fill(pg.Color('#B2704E'))
        return image

    def update_image(self):
        self.image = self.empty_image.copy()
        self.image.blit(self.title.image, self.title.rect)
        if self.button_system:
            self.button_system.draw(self.image)
        if self.volume_bar:
            self.volume_bar.draw(self.image)
        if self.state == 'CONTROLS':
            self.make_labels()
            for label in self.labels:
                self.image.blit(label.image, label.rect)

    def change_to_sound(self):
        self.state = 'SOUND'
        self.title = Label(
            'Quicksand-Regular', 60, 'SOUND', pg.Color('black'),
            center=(self.rect.width // 2, self.rect.height // 2 - 200))
        self.button_system = ButtonSystem(
            self.button_call, ['BACK'],
            font_size=25, gap=30)
        self.button_system.rect.center = (self.rect.width // 2,
                                          self.rect.height // 2 + 100)
        self.volume_bar = VolumeBar(25, (self.rect.width // 2,
                                         self.rect.height // 2))

    def change_to_controls(self):
        self.state = 'CONTROLS'
        self.title = Label(
            'Quicksand-Regular', 60, 'CONTROLS', pg.Color('black'),
            center=(self.rect.width // 2, self.rect.height // 2 - 200))
        self.update_button_system()
        self.volume_bar = None

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
        self.button_system.rect.center = (self.rect.width // 2 + 175,
                                          self.rect.height // 2 + 50)

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
