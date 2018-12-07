from input_decorator import has_input

import sys

from collections import defaultdict

SAMPLE = '''
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
'''

SIZE = 500
SAFE_DIST = 10000


class Destination(object):
    def __init__(self, col, row):
        self.x = row
        self.y = col

    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)


@has_input
def part_one(input):

    destinations = []
    grid = create_grid(SIZE)

    for coords in input.strip().splitlines():
        destinations.append(Destination(*map(int, coords.split(', '))))

    destinations.sort(key=lambda c: c.x + c.y)

    for index, destination in enumerate(destinations):
        grid[destination.x][destination.y] = chr(ord('0') + index)

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col != '.':
                continue

            grid[i][j] = check_position(destinations, i, j)

    # Identify edge characters
    infinite_chars = set()
    for c in range(SIZE):
        if grid[0][c] not in infinite_chars:
            infinite_chars.add(grid[0][c])
        if grid[c][0] not in infinite_chars:
            infinite_chars.add(grid[c][0])
        if grid[-1][c] not in infinite_chars:
            infinite_chars.add(grid[-1][c])
        if grid[c][-1] not in infinite_chars:
            infinite_chars.add(grid[c][-1])

    char_count = defaultdict(int)
    for row in grid:
        for col in row:
            if col not in infinite_chars:
                char_count[col] += 1

    print max(char_count.values())


def check_position(destinations, x, y):
    closest = (sys.maxint, -1)
    for index, destination in enumerate(destinations):
        if index == closest[1]:
            continue

        curr_dist = get_distance(destination, x, y)

        if curr_dist < closest[0]:
            closest = (curr_dist, index)

    for index, destination in enumerate(destinations):
        if index == closest[1]:
            continue

        curr_dist = get_distance(destination, x, y)
        if curr_dist == closest[0]:
            return '.'

    return chr(ord('0') + closest[1])


def create_grid(size):
    return [['.' for _ in range(size)] for _ in range(size)]


def print_grid(grid):
    print '\n'.join(['|'.join(l) for l in grid])


def get_distance(dest1, point_x, point_y):
    return sum((max(abs(dest1.x - point_x), abs(point_x - dest1.x)), max(abs(dest1.y - point_y), abs(point_y - dest1.y))))


@has_input
def part_two(input):

    destinations = []
    grid = create_grid(SIZE)

    for coords in input.strip().splitlines():
        destinations.append(Destination(*map(int, coords.split(', '))))

    destinations.sort(key=lambda c: c.x + c.y)

    for index, destination in enumerate(destinations):
        grid[destination.x][destination.y] = chr(ord('0') + index)

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            grid[i][j] = check_if_safe_zone(destinations, i, j)

    safe_count = 0
    for row in grid:
        for col in row:
            if col == '#':
                safe_count += 1

    print safe_count


def check_if_safe_zone(destinations, x, y):
    safe_count = 0
    for index, destination in enumerate(destinations):
        safe_count += get_distance(destination, x, y)
        if safe_count >= SAFE_DIST:
            return '.'

    return '#'
