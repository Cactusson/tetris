import pygame as pg

from .. import prepare


class Label(pg.sprite.Sprite):
    """
    Just some text.
    """
    def __init__(self, font_name, font_size, text, color, center=None,
                 topleft=None, bg=None, width=None, height=None):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(prepare.FONTS[font_name], font_size)
        self.color = color
        self.text = text
        self.image = self.make_image(bg, width, height)
        if center:
            self.rect = self.image.get_rect(center=center)
        elif topleft:
            self.rect = self.image.get_rect(topleft=topleft)
        else:
            message = 'Center or topleft should be among the kwargs of Label'
            raise ValueError(message)

    def make_image(self, bg, width, height):
        if width and height:
            image = pg.Surface((width, height)).convert()
            if bg:
                image.fill(bg)
            else:
                image.set_alpha(0)
                image = image.convert_alpha()
            text = self.font.render(self.text, True, self.color)
            rect = text.get_rect(center=(width // 2, height // 2))
            image.blit(text, rect)
        else:
            image = self.font.render(self.text, True, self.color, bg)
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
