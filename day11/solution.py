import math

from input_decorator import has_input


SAMPLE = '''
1723
'''

POWER_GRID_SIZE = 300


@has_input
def part_one(input):

    serial_number = int(SAMPLE.strip())

    grid = [[0 for _ in range(POWER_GRID_SIZE)] for _ in range(POWER_GRID_SIZE)]
    get_current_levels(serial_number, grid)

    # print '\n'.join(map(lambda line: '|'.join([c.ljust(3) for c in map(str, line)]), grid))
    get_highest_power_block(grid)


def get_highest_power_block(grid):
    highest = (0, (0,0))
    for row in range(POWER_GRID_SIZE - 2):
        for col in range(POWER_GRID_SIZE - 2):
            curr = sum((grid[row][col],   grid[row][col+1],   grid[row][col+2],
                        grid[row+1][col], grid[row+1][col+1], grid[row+1][col+2],
                        grid[row+2][col], grid[row+2][col+1], grid[row+2][col+2]))
            if curr > highest[0]:
                highest = (curr, (row, col))

    print highest

def get_current_levels(serial_number, grid):
    for row in range(POWER_GRID_SIZE):
        for col in range(POWER_GRID_SIZE):
            grid[row][col] = calc_power(serial_number, col, row)


def calc_power(serial_number, x, y):
    rack_id = x + 10
    return (((((rack_id * y) + serial_number) * rack_id)/100) % 10) - 5

@has_input
def part_two(input):
    serial_number = int(SAMPLE.strip())

    grid = [[0 for _ in range(POWER_GRID_SIZE)] for _ in range(POWER_GRID_SIZE)]
    get_current_levels(serial_number, grid)
    get_highest_power_block_any_size(grid)

def get_highest_power_block_any_size(grid):
    highest = (0, (0, 0, 0)) # x, y, size

    for block_size in range(1, 300):
        for row in range(POWER_GRID_SIZE - (block_size - 1)):
            for col in range(POWER_GRID_SIZE - (block_size - 1)):
                block = get_block(grid, block_size, row, col)
                curr = sum(block)
                if curr > highest[0]:
                    highest = (curr, (row, col, block_size))

    print highest


def get_block(grid, size, x, y):
    block = []
    for i in range(size):
        for j in range(size):
            block.append(grid[x+i][y+j])

    return block
