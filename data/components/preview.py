import pygame as pg

from .. import prepare


class Preview:
    def __init__(self, center, update_function):
        self.update_image_in_gui = update_function
        self.width = 120
        self.height = 120
        self.block_size = 25
        self.frame_width = 4
        self.image = self.make_image()
        self.shader_image = pg.transform.smoothscale(
            prepare.GFX['other']['shader'], (self.block_size, self.block_size))
        self.rect = self.image.get_rect(center=center)

    def make_image(self):
        frame = pg.Surface((self.width + self.frame_width * 2,
                            self.height + self.frame_width * 2)).convert()
        frame.fill(pg.Color('black'))
        image = pg.Surface((self.width, self.height)).convert()
        image.fill(pg.Color('white'))
        frame.blit(image, (self.frame_width, self.frame_width))
        return frame

    def make_figure_image(self, figure, colorname):
        color = pg.Color(colorname)
        actual_cols = set()
        actual_rows = set()
        for row in range(len(figure)):
            for col in range(len(figure[0])):
                if figure[row][col]:
                    actual_rows.add(row)
                    actual_cols.add(col)

        width = len(actual_cols) * (self.block_size + 1) + 1
        height = len(actual_rows) * (self.block_size + 1) + 1
        image = pg.Surface((width, height)).convert()
        image.fill(pg.Color('white'))

        for row in actual_rows:
            for col in actual_cols:
                if figure[row][col]:
                    block = pg.Surface((self.block_size,
                                        self.block_size)).convert()
                    block.fill(color)
                    block.blit(self.shader_image, (0, 0))
                    new_col = col - min(actual_cols)
                    new_row = row - min(actual_rows)
                    image.blit(block, (
                        new_col * self.block_size + new_col + 1,
                        new_row * self.block_size + new_row + 1))

        location = (self.width // 2 - width // 2 + self.frame_width,
                    self.height // 2 - height // 2 + self.frame_width)
        return image, location

    def update_image(self, figure, colorname):
        self.image = self.make_image()
        figure_image, location = self.make_figure_image(figure, colorname)
        self.image.blit(figure_image, location)
        self.update_image_in_gui()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
