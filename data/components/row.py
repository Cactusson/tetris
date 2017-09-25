import pygame as pg

from .. import prepare
from . import data


class Row(pg.sprite.Sprite):
    def __init__(self, number, row, alpha):
        pg.sprite.Sprite.__init__(self)
        self.number = number
        self.row = row
        self.block_size = 25
        self.gap = 1
        self.size = ((self.gap + self.block_size) * len(row),
                     self.block_size)
        self.cover = pg.Surface(self.size).convert()
        self.cover.fill(0)
        self.cover.set_alpha(alpha)
        self.shader_image = pg.transform.smoothscale(
            prepare.GFX['other']['shader'], (self.block_size, self.block_size))
        self.alpha = alpha
        self.image = self.make_image()
        topleft = 0, self.gap + (self.block_size + self.gap) * self.number
        self.rect = self.image.get_rect(topleft=topleft)

    def make_image(self):
        image = pg.Surface(self.size).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        for col, elem in enumerate(self.row):
            if elem != 0:
                block = pg.Surface((self.block_size,
                                    self.block_size)).convert()
                if elem > 10:
                    color = pg.Color(data.colors[elem - 11])
                else:
                    color = pg.Color(data.colors[elem - 1])
                block.fill(color)
                block.blit(self.shader_image, (0, 0))
                # block.blit(self.cover, (0, 0))
                block.set_alpha(self.alpha)
                image.blit(block,
                           (col * (self.block_size + self.gap) + self.gap, 0))
        return image
