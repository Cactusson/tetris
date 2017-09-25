import pygame as pg

from .. import prepare
from ..components.preview import Preview
from ..components.label import Label


class Box(pg.sprite.Sprite):
    def __init__(self, center, width=100, height=50,
                 color=pg.Color('#FCC0C0')):
        pg.sprite.Sprite.__init__(self)
        self.image = prepare.GFX['other']['box']
        self.rect = self.image.get_rect(center=center)


class GUI:
    def __init__(self, location=(487, 50)):
        self.width = 200
        self.height = 500
        self.preview = Preview((self.width // 2, 105), self.update_image)

        self.time_box = Box((self.width // 2, 240))
        self.level_box = Box((self.width // 2, 340))
        self.lines_box = Box((self.width // 2, 440))
        self.boxes = pg.sprite.Group(self.time_box,
                                     self.level_box,
                                     self.lines_box)
        self.time_value = 0

        self.preview_label = Label(
            'Quicksand-Regular', 25, 'NEXT', pg.Color('black'),
            center=(100, 20))
        self.time_label = Label(
            'Quicksand-Regular', 25, 'TIME', pg.Color('black'), center=(
                self.time_box.rect.centerx, self.time_box.rect.centery - 45))
        self.level_label = Label(
            'Quicksand-Regular', 25, 'LEVEL', pg.Color('black'), center=(
                self.level_box.rect.centerx, self.level_box.rect.centery - 45))
        self.lines_label = Label(
            'Quicksand-Regular', 25, 'LINES', pg.Color('black'), center=(
                self.lines_box.rect.centerx, self.lines_box.rect.centery - 45))

        self.time = Label(
            'Quicksand-Regular', 25, '00:00', pg.Color('black'),
            center=self.time_box.rect.center)
        self.level = Label(
            'Quicksand-Regular', 25, '1', pg.Color('black'),
            center=self.level_box.rect.center)
        self.lines = Label(
            'Quicksand-Regular', 25, '0', pg.Color('black'),
            center=self.lines_box.rect.center)

        self.labels = pg.sprite.Group(self.preview_label,
                                      self.time_label,
                                      self.level_label,
                                      self.lines_label,
                                      self.time,
                                      self.level,
                                      self.lines)

        self.update_image()
        self.rect = self.image.get_rect(topleft=location)

    def get_time_string(self):
        minutes, seconds = (str(int(self.time_value // 60000)),
                            str(int((self.time_value % 60000) // 1000)))
        if len(minutes) == 1:
            minutes = '0' + minutes
        if len(seconds) == 1:
            seconds = '0' + seconds
        time_string = '{}:{}'.format(minutes, seconds)
        return time_string

    def update_time(self, dt):
        self.time_value += dt
        time_string = self.get_time_string()
        self.time.kill()
        self.time = Label(
            'Quicksand-Regular', 25, time_string, pg.Color('black'),
            center=self.time_box.rect.center)
        self.labels.add(self.time)
        self.update_image()

    def change_level(self, number):
        self.level.kill()
        self.level = Label(
            'Quicksand-Regular', 25, str(number), pg.Color('black'),
            center=self.level_box.rect.center)
        self.labels.add(self.level)
        self.update_image()

    def change_lines(self, amount):
        self.lines.kill()
        self.lines = Label(
            'Quicksand-Regular', 25, str(amount), pg.Color('black'),
            center=self.lines_box.rect.center)
        self.labels.add(self.lines)
        self.update_image()

    def update_image(self):
        self.image = pg.Surface((self.width, self.height)).convert()
        self.image.fill(pg.Color('#B2704E'))
        self.image.blit(self.preview.image, self.preview.rect)
        for box in self.boxes:
            self.image.blit(box.image, box.rect)
        for label in self.labels:
            self.image.blit(label.image, label.rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
