import copy
import random

from . import data
from .figure import Figure


class Matrix:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.matrix = [[0 for i in range(width)] for j in range(height)]
        self.standard_topleft = (0, 3)
        self.next_figure = None
        self.current_figure = None
        self.figure_index = None
        self.figure_topleft = None

    def get_new_figure(self):
        if self.next_figure is not None:
            figure_data = self.next_figure
        else:
            figure_data = random.choice(data.figures)
        self.current_figure = Figure(figure_data)
        self.figure_index = data.figures.index(figure_data) + 1
        self.figure_topleft = list(self.standard_topleft)
        self.next_figure = random.choice(data.figures)

    def add_current_figure(self):
        top, left = self.figure_topleft
        length = len(self.current_figure.matrix)
        if left < 0:
            offset = -left
            cols = [0, length + left]
            left = 0
        else:
            offset = 0
            cols = [left, left + length]
        for row_num, row in enumerate(self.matrix[top:top+length]):
            for col_num, elem in enumerate(row[cols[0]:cols[1]]):
                if self.current_figure.matrix[row_num][col_num + offset] == 1:
                    if elem != 0:
                        raise Exception('Something is wrong!')
                    self.matrix[
                        row_num + top][col_num + left] = self.figure_index

    def erase_current_figure(self):
        top, left = self.figure_topleft
        length = len(self.current_figure.matrix)
        if left < 0:
            cols = [0, length + left]
            left = 0
        else:
            cols = [left, left + length]
        for row_num, row in enumerate(self.matrix[top:top+length]):
            for col_num, elem in enumerate(row[cols[0]:cols[1]]):
                if elem == self.figure_index:
                    self.matrix[row_num + top][col_num + left] = 0

    def rotate(self, clockwise):
        if not self.check_rotate(clockwise):
            self.rotate_figure(clockwise)
        else:
            self.wallkick(clockwise)

    def rotate_figure(self, clockwise):
        self.erase_current_figure()
        self.current_figure.rotate(clockwise)
        self.add_current_figure()

    def check_rotate(self, clockwise):
        top, left = self.figure_topleft
        length = len(self.current_figure.matrix)
        if (left < 0 or left + length > self.width or
                top + length > self.height):
            return True
        self.current_figure.rotate(clockwise)
        overlaps = False
        for row_num, row in enumerate(self.matrix[top:top+length]):
            for col_num, elem in enumerate(row[left:left+length]):
                if self.current_figure.matrix[row_num][col_num] == 1:
                    if elem > 10:
                        overlaps = True
        self.current_figure.rotate(not clockwise)
        return overlaps

    def wallkick(self, clockwise):
        if self.check('left'):
            self.move_figure('left')
            if not self.check_rotate(clockwise):
                self.rotate_figure(clockwise)
                return
            else:
                self.move_figure('right')
        if self.check('right'):
            self.move_figure('right')
            if not self.check_rotate(clockwise):
                self.rotate_figure(clockwise)
            else:
                self.move_figure('left')

    def check(self, side):
        for row_num, row in enumerate(self.matrix):
            for col_num, elem in enumerate(row):
                if side == 'bottom':
                    if elem == self.figure_index:
                        if row_num == self.height - 1:
                            return False
                        if self.matrix[row_num + 1][col_num] > 10:
                            return False
                elif side == 'left':
                    if elem == self.figure_index:
                        if col_num == 0:
                            return False
                        if self.matrix[row_num][col_num - 1] > 10:
                            return False
                elif side == 'right':
                    if elem == self.figure_index:
                        if col_num == self.width - 1:
                            return False
                        if self.matrix[row_num][col_num + 1] > 10:
                            return False
        return True

    def stop_figure(self):
        for row_num, row in enumerate(self.matrix):
            for col_num, elem in enumerate(row):
                if elem == self.figure_index:
                    self.matrix[row_num][col_num] = self.figure_index + 10

    def descend_figure(self):
        self.erase_current_figure()
        self.figure_topleft[0] += 1
        self.add_current_figure()

    def move_figure(self, side):
        if not self.check(side):
            return
        self.erase_current_figure()
        if side == 'left':
            self.figure_topleft[1] -= 1
        elif side == 'right':
            self.figure_topleft[1] += 1
        self.add_current_figure()

    def check_free_space(self):
        top, left = self.figure_topleft
        length = len(self.current_figure.matrix)
        for row_num, row in enumerate(self.matrix[top:top+length]):
            for col_num, elem in enumerate(row[left:left+length]):
                if self.current_figure.matrix[
                        row_num - top][col_num - left] == 1:
                    if elem != 0:
                        return False
        return True

    def get_full_rows(self):
        full_rows = []
        for row_num, row in enumerate(self.matrix):
            if len([elem for elem in row if elem > 10]) == len(row):
                full_rows.append(row_num)
        return full_rows

    def erase_row(self, row_num):
        for col_num in range(len(self.matrix[row_num])):
            self.matrix[row_num][col_num] = 0

    def descend_matrix(self, full_rows):
        new_matrix = [
            [0 for i in range(self.width)] for j in range(self.height)]
        steps = len(full_rows)
        rows_to_descend = []
        for row_num, row in enumerate(self.matrix):
            if row_num in full_rows:
                steps -= 1
                if steps < 0:
                    raise Exception('descend_matrix does not work')
                continue
            if any(row) and steps > 0:
                rows_to_descend.append((row_num, steps))
            for col_num, elem in enumerate(row):
                new_matrix[row_num + steps][col_num] = elem
        self.matrix = new_matrix
        return rows_to_descend

    def get_preview(self):
        preview_template = data.previews[self.figure_index - 1][
                                     self.current_figure.index]
        top, left = self.figure_topleft
        new_matrix = copy.deepcopy(self.matrix)
        while self.check('bottom'):
            self.descend_figure()
        preview_top = None
        preview_left = None
        for row_num, row in enumerate(self.matrix):
            for col_num, elem in enumerate(row):
                if elem == self.figure_index:
                    if preview_top is None:
                        preview_top = row_num
                    if preview_left is None:
                        preview_left = col_num
                    elif col_num < preview_left:
                        preview_left = col_num
        self.matrix = new_matrix
        self.figure_topleft = [top, left]
        return preview_template, preview_top, preview_left
