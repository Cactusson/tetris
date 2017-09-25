import pygame as pg

from .. import prepare


class Button(pg.sprite.Sprite):
    """
    Button is some text on a bg. If you click on it, call (function)
    will be called.
    """
    def __init__(self, center, text, font_name, font_size,
                 width=None, height=None):
        pg.sprite.Sprite.__init__(self)
        self.name = text
        self.font = pg.font.Font(prepare.FONTS[font_name], font_size)
        self.make_images(text, width, height)
        self.image = self.idle_image
        self.rect = self.image.get_rect(center=center)

    def make_images(self, text, width, height):
        """
        Button changes its image depending if the player is hovering it or not.
        """
        idle_color = pg.Color('black')
        hover_color = pg.Color('white')
        hover_fill = pg.Color('purple')
        locked_color = pg.Color('white')
        locked_fill = pg.Color('red')
        if width is not None and height is not None:
            idle_image = pg.Surface((width, height)).convert()
            idle_image.set_alpha(0)
            idle_image = idle_image.convert_alpha()
            idle_text = self.font.render(text, True, idle_color)
            idle_image.blit(idle_text, idle_text.get_rect(
                center=idle_image.get_rect().center))
            hover_image = pg.Surface((width, height)).convert()
            hover_image.fill(hover_fill)
            hover_text = self.font.render(text, True, hover_color, hover_fill)
            hover_image.blit(hover_text, hover_text.get_rect(
                center=hover_image.get_rect().center))
            locked_image = pg.Surface((width, height)).convert()
            locked_image.fill(locked_fill)
            locked_text = self.font.render(
                text, True, locked_color, locked_fill)
            locked_image.blit(locked_text, locked_text.get_rect(
                center=locked_image.get_rect().center))
        else:
            idle_image = self.font.render(text, True, idle_color)
            hover_image = self.font.render(text, True, hover_color, hover_fill)
            locked_image = self.font.render(
                text, True, locked_color, locked_fill)

        self.idle_image = idle_image
        self.hover_image = hover_image
        self.locked_image = locked_image

    def hover(self):
        self.image = self.hover_image

    def unhover(self):
        self.image = self.idle_image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
