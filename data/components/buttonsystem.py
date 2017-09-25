import pygame as pg

from .. import prepare
from .button import Button


class ButtonSystem(pg.sprite.Sprite):
    def __init__(self, callback, names, gap=40,
                 font_name='Quicksand-Regular', font_size=30):
        self.active_button = None
        self.callback = callback
        self.buttons = self.make_buttons(names, gap, font_name,
                                         font_size)
        self.basic_image = self.make_image(gap)
        self.rect = self.basic_image.get_rect()
        self.locked = False
        self.start()

    def start(self, index=0):
        self.change_active_button(self.buttons_list[index])

    def make_buttons(self, names, gap, font_name, font_size):
        buttons = pg.sprite.Group()
        self.buttons_list = []
        button_width, button_height = self.get_button_size(
            names, font_name, font_size)
        for num, name in enumerate(names):
            button_center = (button_width // 2,
                             (button_height + gap) * num + button_height // 2)
            button = Button(button_center, name, 'Quicksand-Regular',
                            font_size, button_width, button_height)
            buttons.add(button)
            self.buttons_list.append(button)
        return buttons

    def get_button_size(self, names, font_name, font_size):
        width = 0
        height = 0
        for name in names:
            button = Button((0, 0), name, font_name, font_size)
            if button.rect.width > width:
                width = button.rect.width
            if button.rect.height > height:
                height = button.rect.height
        if width == 0:
            width = None
        else:
            width *= 1.4
        if height == 0:
            height = None
        else:
            height *= 1.2
        return width, height

    def make_image(self, gap):
        width = self.buttons.sprites()[0].rect.width
        button_height = self.buttons.sprites()[0].rect.height
        height = (len(self.buttons) * button_height + (len(self.buttons) - 1) *
                  gap)
        image = pg.Surface((width, height)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        return image

    def update_image(self):
        self.image = self.basic_image.copy()
        for button in self.buttons:
            self.image.blit(button.image, button.rect)

    def change_active_button(self, button):
        if self.active_button:
            self.active_button.unhover()
        self.active_button = button
        self.active_button.hover()
        self.update_image()

    def next_button(self, direction):
        if not self.active_button:
            return
        prepare.SFX['hover'].play()
        if direction == 'up':
            index = self.buttons_list.index(self.active_button) - 1
            if index < 0:
                index = len(self.buttons_list) - 1
        elif direction == 'down':
            index = self.buttons_list.index(self.active_button) + 1
            if index == len(self.buttons_list):
                index = 0
        self.change_active_button(self.buttons_list[index])

    def press_button(self):
        if not self.active_button:
            return
        prepare.SFX['click'].play()
        self.callback(self.active_button.name)

    def toggle_lock(self):
        if not self.active_button:
            return
        if self.locked:
            self.active_button.image = self.active_button.hover_image
        else:
            self.active_button.image = self.active_button.locked_image
        self.locked = not self.locked
        self.update_image()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
