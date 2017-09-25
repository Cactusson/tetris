import pickle
import pygame as pg

from .. import prepare
from .label import Label


class HSTable(pg.sprite.Sprite):
    def __init__(self, font_size):
        pg.sprite.Sprite.__init__(self)
        self.font_size = font_size
        self.update_image()

    def make_image(self):
        gap = self.font_size // 3
        width = self.labels.sprites()[0].rect.width
        label_height = self.labels.sprites()[0].rect.height
        height = (len(self.labels) * label_height + (len(self.labels) - 1) *
                  gap)
        image = pg.Surface((width, height)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        for label in self.num_labels:
            image.blit(label.image, label.rect)
        for label in self.labels:
            image.blit(label.image, label.rect)
        return image

    def make_labels(self, underline=None):
        gap = self.font_size // 3
        labels = pg.sprite.Group()
        num_labels = pg.sprite.Group()
        label_width, label_height = self.get_label_size(self.font_size)
        for num, line in enumerate(prepare.results):
            if line != '-':
                lines, time = line
                line = '{} ({})'.format(lines, time)
            # text = '{}. {}'.format(num + 1, line)
            if underline == num:
                color = pg.Color('white')
                bg = pg.Color('blue')
            else:
                color = pg.Color('black')
                bg = None
            topleft = (0, (label_height + gap) * num)
            text = '{}.'.format(str(num + 1))
            num_label = Label('Quicksand-Regular', self.font_size, text,
                              pg.Color('black'), topleft=topleft)
            num_labels.add(num_label)
            topleft = (num_label.rect.width + 10,
                       (label_height + gap) * num)
            label = Label('Quicksand-Regular', self.font_size, line,
                          color, topleft=topleft, bg=bg,
                          width=label_width, height=label_height)
            labels.add(label)
        return num_labels, labels

    def get_label_size(self, font_size):
        width = 0
        height = 0
        for num, line in enumerate(prepare.results):
            line = str(line)
            label = Label('Quicksand-Regular', font_size, line,
                          pg.Color('black'), center=(0, 0))
            if label.rect.width > width:
                width = label.rect.width
            if label.rect.height > height:
                height = label.rect.height
        if width == 0:
            width = None
        else:
            width *= 1.4
        if height == 0:
            height = None
        else:
            height *= 1.2
        return width, height

    def get_result(self, result, underline=False):
        for index, line in enumerate(prepare.results):
            if line == '-':
                self.save_result(result, index)
                if underline:
                    self.update_image(index)
                else:
                    self.update_image()
                break
            elif result[0] >= int(line[0]):
                self.save_result(result, index)
                if underline:
                    self.update_image(index)
                else:
                    self.update_image()
                break

    def save_result(self, result, index):
        prepare.results.insert(index, result)
        prepare.results.pop()
        results_file = open('results', 'wb')
        pickle.dump(prepare.results, results_file)

    def update_image(self, underline=None):
        self.num_labels, self.labels = self.make_labels(underline)
        self.image = self.make_image()
        self.rect = self.image.get_rect()

    def clear(self):
        prepare.results = ['-', '-', '-', '-', '-']
        results_file = open('results', 'wb')
        pickle.dump(prepare.results, results_file)
        self.update_image()
