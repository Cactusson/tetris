import pygame as pg


class Wizard(pg.sprite.Sprite):
    def __init__(self, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((55, 55)).convert()
        self.image.fill(pg.Color('lightblue'))
        self.rect = self.image.get_rect(topleft=location)
