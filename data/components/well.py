import pygame as pg
import random

from .. import prepare
from . import data
from .animations import Animation
from .explosion import Explosion
from .matrix import Matrix
from .row import Row
from .task import Task
from .wizard import Wizard


class Well(pg.sprite.Sprite):
    def __init__(self, preview_block, lines_function, lose_function,
                 location, width=10, height=20):
        self.preview_block = preview_block
        self.lines_function = lines_function
        self.lose_function = lose_function
        self.state = 'PRE_PLAY'
        self.width = width
        self.height = height
        self.block_size = 25
        self.usual_move_time = 500
        self.stop_drop_move_time = 150
        self.move_time = self.usual_move_time
        self.matrix = Matrix(self.width, self.height)
        self.preview_width = 3
        self.frame_width = 5
        self.explosion_cooldown = 10
        self.explosion_time = 0
        self.wizard = None
        self.wizard_animation = None
        self.rows = pg.sprite.Group()
        self.tasks = pg.sprite.Group()
        self.animations = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.alphas = [255 for _ in range(self.height)]
        self.empty_image = self.make_empty_image()
        self.image = self.empty_image.copy()
        self.rect = self.image.get_rect(topleft=location)

    def start(self, now):
        self.state = 'PLAY'
        self.add_new_figure(now)

    def add_new_figure(self, now):
        self.matrix.get_new_figure()
        colorname = data.colors[data.figures.index(self.matrix.next_figure)]
        self.preview_block.update_image(self.matrix.next_figure[0], colorname)
        lost = not self.matrix.check_free_space()
        if lost:
            self.lose_function()
            self.state = 'LOST'
        else:
            self.matrix.add_current_figure()
            self.update_image()
            self.update_preview()
            self.move_timer = now

    def player_action(self, action):
        if action == 'stop_soft_drop':
            self.stop_soft_drop()
        elif self.state != 'PLAY':
            return
        elif action == 'left':
            self.matrix.move_figure('left')
        elif action == 'right':
            self.matrix.move_figure('right')
        elif action == 'rotate_clockwise':
            self.matrix.rotate(True)
        elif action == 'rotate_counterclockwise':
            self.matrix.rotate(False)
        elif action == 'start_soft_drop':
            self.start_soft_drop()
        elif action == 'hard_drop':
            self.hard_drop(self.current_time)
        if (action == 'right' or action == 'left' or
                action.startswith('rotate')):
            self.update_image()
            self.update_preview()

    def ground_figure(self, now):
        self.matrix.stop_figure()
        full_rows = self.matrix.get_full_rows()
        if full_rows:
            self.update_image()
            self.state = 'ROW_CLEAR'
            self.create_wizard(min(full_rows))
            prepare.SFX['whoosh'].play()
            task = Task(self.splash_rows, 50, 10, args=(full_rows,))
            task.chain(Task(self.erase_full_rows, args=(full_rows,)))
            self.tasks.add(task)
        else:
            self.add_new_figure(now)

    def start_soft_drop(self):
        self.move_time = self.stop_drop_move_time

    def stop_soft_drop(self):
        self.move_time = self.usual_move_time

    def hard_drop(self, now):
        while self.matrix.check('bottom'):
            self.matrix.descend_figure()
        self.ground_figure(now)

    def erase_full_rows(self, full_rows):
        for row in full_rows:
            self.matrix.erase_row(row)
            self.alphas[row] = 255
        self.lines_function(len(full_rows))
        self.descend_rows(full_rows)

    def create_wizard(self, row_num):
        if self.wizard_animation:
            self.wizard_animation.kill()
        location = (-55, self.rect.y + self.frame_width + 1 +
                    (self.block_size + 1) * row_num - 15)
        self.wizard = Wizard(location)
        animation = Animation(
            x=self.rect.x - self.wizard.rect.width - 10, y=self.wizard.rect.y,
            duration=400, round_values=True, transition='out_quad')
        animation.callback = self.wizard_get_back
        animation.start(self.wizard.rect)
        self.animations.add(animation)

    def wizard_get_back(self):
        self.wizard_animation = Animation(
            x=-55, y=self.wizard.rect.y, duration=400, round_values=True,
            transition='out_quad')
        self.wizard_animation.callback = self.kill_wizard
        self.wizard_animation.start(self.wizard.rect)
        self.animations.add(self.wizard_animation)

    def kill_wizard(self):
        self.wizard = None

    def splash_rows(self, rows):
        step_alpha = 20
        for row_num in rows:
            self.alphas[row_num] = max(self.alphas[row_num] - step_alpha, 0)
        self.update_image()

    def descend_rows(self, full_rows):
        self.update_image()
        rows_to_descend = self.matrix.descend_matrix(full_rows)
        if rows_to_descend:
            self.animations.add(self.create_rows_animations(rows_to_descend))
        else:
            self.stop_descending()

    def create_rows_animations(self, rows_to_descend):
        animations = pg.sprite.Group()
        for row_num, steps in rows_to_descend:
            for row in self.rows:
                if row.number == row_num:
                    path = (self.block_size + 1) * steps
                    x = row.rect.x
                    y = row.rect.y + path
                    animation = Animation(
                        x=x, y=y, duration=400, round_values=True,
                        transition='out_quad')
                    if not animations:
                        animation.callback = self.stop_descending
                    animations.add(animation)
                    animation.start(row.rect)
                    break
        return animations

    def stop_descending(self):
        self.state = 'PLAY'
        self.add_new_figure(self.current_time)

    def update_preview(self):
        preview_template, preview_top, preview_left = self.matrix.get_preview()
        self.preview = []
        for point in preview_template:
            x = ((point[0] + preview_left) * (self.block_size + 1) +
                 self.rect.x + self.frame_width)
            y = ((point[1] + preview_top) * (self.block_size + 1) +
                 self.rect.y + self.frame_width)
            self.preview.append([x, y])

    def make_empty_image(self):
        frame = pg.Surface(
            (self.block_size * self.width + self.width + 1 +
                self.frame_width * 2,
             self.block_size * self.height + self.height + 1 +
                self.frame_width * 2)).convert()
        frame.fill(pg.Color('black'))
        image = pg.Surface(
            (self.block_size * self.width + self.width + 1,
             self.block_size * self.height + self.height + 1)).convert()
        image.fill(pg.Color('gray'))
        for i in range(self.width):
            for j in range(self.height):
                block = pg.Surface((self.block_size,
                                    self.block_size)).convert()
                block.fill(pg.Color('white'))
                image.blit(block, (1 + (self.block_size + 1) * i,
                                   1 + (self.block_size + 1) * j))
        frame.blit(image, (self.frame_width, self.frame_width))

        return frame

    def create_explosion(self, now):
        self.explosion_time = now
        x = random.randint(0, self.rect.width)
        y = random.randint(0, self.rect.height)
        self.explosions.add(Explosion((x, y)))

    def update_image(self):
        self.image = self.empty_image.copy()
        self.rows.empty()
        for row_num in range(self.height):
            row = Row(row_num, self.matrix.matrix[row_num],
                      self.alphas[row_num])
            self.rows.add(row)

    def draw(self, surface):
        self.image = self.empty_image.copy()
        for row in self.rows:
            topleft = (row.rect.left + self.frame_width,
                       row.rect.top + self.frame_width)
            self.image.blit(row.image, topleft)
        self.explosions.draw(self.image)
        surface.blit(self.image, self.rect)
        if self.wizard:
            surface.blit(self.wizard.image, self.wizard.rect)
        if self.state == 'PLAY':
            pg.draw.lines(surface,
                          pg.Color(data.colors[self.matrix.figure_index - 1]),
                          True, self.preview, self.preview_width)

    def update(self, now, dt):
        self.current_time = now
        if self.state == 'PLAY':
            if now - self.move_timer >= self.move_time:
                self.move_timer = now
                if self.matrix.check('bottom'):
                    self.matrix.descend_figure()
                else:
                    self.ground_figure(now)
                if self.state == 'PLAY':
                    self.update_image()
        elif self.state == 'LOST':
            if now - self.explosion_cooldown >= self.explosion_time:
                self.create_explosion(now)
        self.tasks.update(dt * 1000)
        self.animations.update(dt * 1000)
        self.explosions.update(dt * 1000)
