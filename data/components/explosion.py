import pygame as pg
import random

from .. import prepare


class Explosion(pg.sprite.Sprite):
    images_one = [prepare.GFX['explosions']['boom1_{}'.format(x)]
                  for x in range(7)]
    images_two = [pg.transform.smoothscale(prepare.GFX['explosions'][
                  'boom2_{}'.format(x)], (50, 50)) for x in range(9)]

    def __init__(self, location):
        pg.sprite.Sprite.__init__(self)
        if random.randint(1, 2) == 1:
            self.images = Explosion.images_one
        else:
            self.images = Explosion.images_two
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(topleft=location)
        self.animation_timer = 0
        self.animation_time = 100

    def update(self, dt):
        self.animation_timer += dt
        if self.animation_timer > self.animation_time:
            self.animation_timer -= self.animation_time
            self.image_index += 1
            if self.image_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.image_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
