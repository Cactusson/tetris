import pygame as pg

from .. import prepare


class VolumeBar(pg.sprite.Sprite):
    def __init__(self, size, center):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.empty_image = self.make_empty_image()
        self.rect = self.empty_image.get_rect(center=center)
        self.update_image()

    def make_empty_image(self):
        image = pg.Surface((self.size + (self.size + self.size // 2) * 9,
                            self.size * 2)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        return image

    def make_squares(self):
        self.squares = pg.sprite.Group()
        self.squares_list = []
        amount = int(prepare.music_volume * 10)
        for i in range(amount):
            square = pg.sprite.Sprite()
            square.image = pg.Surface((self.size, self.size * 2)).convert()
            square.image.fill(pg.Color('black'))
            square.rect = square.image.get_rect()
            square.rect.left = i * (self.size + self.size // 2)
            self.squares.add(square)
            self.squares_list.append(square)

    def update_image(self):
        self.image = self.empty_image.copy()
        self.make_squares()
        self.squares.draw(self.image)

    def change_volume(self, delta):
        if delta < 0:
            if prepare.music_volume > 0:
                prepare.music_volume -= 0.1
                if prepare.music_volume < 0:
                    prepare.music_volume = 0
        elif delta > 0:
            if prepare.music_volume < 1.0:
                prepare.music_volume += 0.1
                if prepare.music_volume > 1.0:
                    prepare.music_volume = 1.0
        pg.mixer.music.set_volume(prepare.music_volume)
        self.update_image()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
