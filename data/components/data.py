import pygame as pg


figures = [
    [
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0]
        ],
        [
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0]
        ],
    ],
    [
        [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
        [
            [0, 1, 1],
            [0, 1, 0],
            [0, 1, 0]
        ],
        [
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 1]
        ],
        [
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 0]
        ],
    ],
    [
        [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ],
        [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ],
        [
            [0, 0, 0],
            [1, 1, 1],
            [1, 0, 0]
        ],
        [
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ],
    ],
    [
        [
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
    ],
    [
        [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ],
        [
            [0, 1, 0],
            [0, 1, 1],
            [0, 0, 1]
        ],
        [
            [0, 0, 0],
            [0, 1, 1],
            [1, 1, 0]
        ],
        [
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0]
        ],
    ],
    [
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
        [
            [0, 1, 0],
            [0, 1, 1],
            [0, 1, 0]
        ],
        [
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0]
        ],
        [
            [0, 1, 0],
            [1, 1, 0],
            [0, 1, 0]
        ],
    ],
    [
        [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ],
        [
            [0, 0, 1],
            [0, 1, 1],
            [0, 1, 0]
        ],
        [
            [0, 0, 0],
            [1, 1, 0],
            [0, 1, 1]
        ],
        [
            [0, 1, 0],
            [1, 1, 0],
            [1, 0, 0]
        ],
    ],
]

previews = [
    [
        [
            [0, 0],
            [4, 0],
            [4, 1],
            [0, 1]
        ],
        [
            [0, 0],
            [1, 0],
            [1, 4],
            [0, 4]
        ],
        [
            [0, 0],
            [4, 0],
            [4, 1],
            [0, 1]
        ],
        [
            [0, 0],
            [1, 0],
            [1, 4],
            [0, 4]
        ],
    ],
    [
        [
            [0, 0],
            [1, 0],
            [1, 1],
            [3, 1],
            [3, 2],
            [0, 2]
        ],
        [
            [0, 0],
            [2, 0],
            [2, 1],
            [1, 1],
            [1, 3],
            [0, 3]
        ],
        [
            [0, 0],
            [3, 0],
            [3, 2],
            [2, 2],
            [2, 1],
            [0, 1]
        ],
        [
            [0, 2],
            [1, 2],
            [1, 0],
            [2, 0],
            [2, 3],
            [0, 3]
        ],
    ],
    [
        [
            [0, 1],
            [2, 1],
            [2, 0],
            [3, 0],
            [3, 2],
            [0, 2]
        ],
        [
            [0, 0],
            [1, 0],
            [1, 2],
            [2, 2],
            [2, 3],
            [0, 3]
        ],
        [
            [0, 0],
            [3, 0],
            [3, 1],
            [1, 1],
            [1, 2],
            [0, 2]
        ],
        [
            [0, 0],
            [2, 0],
            [2, 3],
            [1, 3],
            [1, 1],
            [0, 1]
        ],
    ],
    [
        [
            [0, 0],
            [2, 0],
            [2, 2],
            [0, 2]
        ],
        [
            [0, 0],
            [2, 0],
            [2, 2],
            [0, 2]
        ],
        [
            [0, 0],
            [2, 0],
            [2, 2],
            [0, 2]
        ],
        [
            [0, 0],
            [2, 0],
            [2, 2],
            [0, 2]
        ],
    ],
    [
        [
            [0, 1],
            [1, 1],
            [1, 0],
            [3, 0],
            [3, 1],
            [2, 1],
            [2, 2],
            [0, 2]
        ],
        [
            [0, 0],
            [1, 0],
            [1, 1],
            [2, 1],
            [2, 3],
            [1, 3],
            [1, 2],
            [0, 2]
        ],
        [
            [0, 1],
            [1, 1],
            [1, 0],
            [3, 0],
            [3, 1],
            [2, 1],
            [2, 2],
            [0, 2]
        ],
        [
            [0, 0],
            [1, 0],
            [1, 1],
            [2, 1],
            [2, 3],
            [1, 3],
            [1, 2],
            [0, 2]
        ],
    ],
    [
        [
            [0, 1],
            [1, 1],
            [1, 0],
            [2, 0],
            [2, 1],
            [3, 1],
            [3, 2],
            [0, 2]
        ],
        [
            [0, 0],
            [1, 0],
            [1, 1],
            [2, 1],
            [2, 2],
            [1, 2],
            [1, 3],
            [0, 3]
        ],
        [
            [0, 0],
            [3, 0],
            [3, 1],
            [2, 1],
            [2, 2],
            [1, 2],
            [1, 1],
            [0, 1]
        ],
        [
            [0, 1],
            [1, 1],
            [1, 0],
            [2, 0],
            [2, 3],
            [1, 3],
            [1, 2],
            [0, 2]
        ],
    ],
    [
        [
            [0, 0],
            [2, 0],
            [2, 1],
            [3, 1],
            [3, 2],
            [1, 2],
            [1, 1],
            [0, 1]
        ],
        [
            [0, 1],
            [1, 1],
            [1, 0],
            [2, 0],
            [2, 2],
            [1, 2],
            [1, 3],
            [0, 3]
        ],
        [
            [0, 0],
            [2, 0],
            [2, 1],
            [3, 1],
            [3, 2],
            [1, 2],
            [1, 1],
            [0, 1]
        ],
        [
            [0, 1],
            [1, 1],
            [1, 0],
            [2, 0],
            [2, 2],
            [1, 2],
            [1, 3],
            [0, 3]
        ],
    ],
]

colors = [
    'cyan',
    'blue',
    'orange',
    'yellow',
    '#80cd32',
    'purple',
    'red',
]


def break_into_squares(figure):
    size = 20
    squares = []
    for row_num, row in enumerate(figure):
        for col_num, elem in enumerate(row):
            if elem:
                squares.append(pg.rect.Rect(
                    size * col_num, size * row_num, size, size))
    return squares


def get_squares(value_list):
    size = 20
    squares = []
    for row, col in value_list:
        squares.append(pg.rect.Rect(size * col, size * row, size, size))
    return squares


def get_pointlist(squares):
    points = []
    for square in squares:
        points.append(square.topleft)
        points.append(square.bottomleft)
        points.append(square.topright)
        points.append(square.bottomright)
    points = list(set(points))
    print(points)
    xs = [x for (x, y) in points]
    xs = list(set(xs))
    for x in xs:
        points_x = [point for point in points if point[0] == x]
        if len(points_x) % 2 != 0:
            low = points_x[0]
            high = points_x[0]
            for (x, y) in points_x:
                if y < low[1]:
                    low = (x, y)
                if y > high[1]:
                    high = (x, y)
            for point in points_x:
                if point != low and point != high:
                    points.remove(point)
    ys = [y for (x, y) in points]
    ys = list(set(ys))
    for y in ys:
        points_y = [point for point in points if point[1] == y]
        if len(points_y) % 2 != 0:
            low = points_y[0]
            high = points_y[0]
            for (x, y) in points_y:
                if x < low[0]:
                    low = (x, y)
                if x > high[0]:
                    high = (x, y)
            for point in points_y:
                if point != low and point != high:
                    points.remove(point)
    print(points)


def get_points_in_order(points):
    result = []
    current_point = points[0]
    index = 0
    opposite_index = 1
    result.append(current_point)
    points.remove(current_point)

    while points:
        candidates = [point for point in points if
                      point[index] == current_point[index]]

        lower = []
        higher = []
        for candidate in candidates:
            if candidate[opposite_index] < current_point[opposite_index]:
                lower.append(candidate)
            else:
                higher.append(candidate)

        if len(lower) == 0:
            chosen_group = higher
        elif len(higher) == 0:
            chosen_group = lower
        elif len(lower) == 1:
            chosen_group = lower
        elif len(higher) == 1:
            chosen_group = higher
        else:
            raise Exception('WRONG!')

        if len(chosen_group) == 0:
            raise Exception('OK, something is very wrong')
        if len(chosen_group) == 1:
            next_point = chosen_group[0]
        else:
            next_point = chosen_group[0]
            for point in chosen_group[1:]:
                old_diff = abs(next_point[opposite_index] -
                               current_point[opposite_index])
                new_diff = abs(point[opposite_index] -
                               current_point[opposite_index])
                if new_diff < old_diff:
                    next_point = point

        current_point = next_point
        result.append(current_point)
        index, opposite_index = opposite_index, index
        points.remove(current_point)

    return result


# figure = figures[-1][0]
# get_pointlist(figure)
value_list = [[18, 5], [19, 5], [19, 6], [19, 7]]
squares = get_squares(value_list)
points = [[100, 360],
          [100, 380],
          [120, 380],
          [120, 400],
          [140, 360],
          [140, 380],
          [160, 380],
          [160, 400]]

points_in_order = get_points_in_order(points)
# print(points_in_order)
