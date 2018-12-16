from input_decorator import has_input


SAMPLE = r'''
/->-\        -
|   |  /----\-
| /-+--+-\  |-
| | |  | v  |-
\-+-/  \-+--/-
  \------/   -
'''


class Legend:
    vertical_path = '|'
    horizontal_path = '-'
    intersection = '+'
    crash = 'x'
    forward = '/'
    back = '\\'


CART_DIR = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
}

CART_PATH = {
    '^': '|',
    '>': '-',
    'v': '|',
    '<': '-',
}


@has_input
def part_one(input):
    cart_map = []
    for line in input.split('\n'):
        cart_map.append(list(line))

    for i in range(len(cart_map)):
        for j in range(len(cart_map[i])):
            position = cart_map[i][j]
            if position in CART_DIR.keys():
                # ('>' <next turn>, <previous track>)
                cart_map[i][j] = (position, 0, CART_PATH[position])

    while True:
        move_carts(cart_map)


def move_carts(cart_map):

    moved = set()

    for i in range(len(cart_map)):
        for j in range(len(cart_map[i])):
            position = cart_map[i][j]
            if not isinstance(position, tuple) or (i, j) in moved:
                continue

            cart = position

            diff_row, diff_col = CART_DIR[cart[0]]
            next_pos = cart_map[i+diff_row][j+diff_col]

            cart_map[i][j] = cart[2]

            if next_pos == Legend.intersection:
                cart = get_next_move(cart, next_pos)

            elif isinstance(next_pos, tuple):
                print '%s,%s' % (i+diff_row, j+diff_col)
                cart = Legend.crash

            elif next_pos == Legend.forward or next_pos == Legend.back:
                turn = hit_turn(cart[0], next_pos)
                cart = (turn, cart[1], next_pos)
            else:
                cart = (cart[0], cart[1], next_pos)

            cart_map[i+diff_row][j+diff_col] = cart
            moved.add((i+diff_row, j+diff_col))



def hit_turn(cart, bank):
    if cart == '^':
        if bank == Legend.forward:
            return '>'
        if bank == Legend.back:
            return '<'
    if cart == '>':
        if bank == Legend.forward:
            return '^'
        if bank == Legend.back:
            return 'v'
    if cart == 'v':
        if bank == Legend.forward:
            return '<'
        if bank == Legend.back:
            return '>'
    if cart == '<':
        if bank == Legend.forward:
            return 'v'
        if bank == Legend.back:
            return '^'


def get_next_move(cart, next_pos):
    # left, straight, right
    next_turn = cart[1]
    next_cart = ''
    curr_cart = cart[0]
    if next_turn == 0:
        if curr_cart == '^':
            next_cart = '<'
        if curr_cart == '>':
            next_cart = '^'
        if curr_cart == 'v':
            next_cart = '>'
        if curr_cart == '<':
            next_cart = 'v'

    elif next_turn == 1:
        next_cart = cart[0]

    elif next_turn == 2:
        if curr_cart == '^':
            next_cart = '>'
        if curr_cart == '>':
            next_cart = 'v'
        if curr_cart == 'v':
            next_cart = '<'
        if curr_cart == '<':
            next_cart = '^'

    next_manuver = (next_turn + 1) % 3
    return (next_cart, next_manuver, next_pos)


def print_map(cart_map):
    for line in cart_map:
        print line

# 101,87
@has_input
def part_two(input):
    cart_map = []
    for line in input.split('\n'):
        cart_map.append(list(line))

    total_carts = 0
    for i in range(len(cart_map)):
        for j in range(len(cart_map[i])):
            position = cart_map[i][j]
            if position in CART_DIR.keys():
                # ('>' <next turn>, <previous track>)
                cart_map[i][j] = (position, 0, CART_PATH[position])
                total_carts += 1

    while True:
        total_carts = move_carts_remove_on_crash(cart_map, total_carts)
        if total_carts == 1:
            for i in range(len(cart_map)):
                for j in range(len(cart_map[i])):
                    position = cart_map[i][j]
                    if isinstance(position, tuple):
                        print '%s,%s' % (i, j)
            break


def move_carts_remove_on_crash(cart_map, total_carts):

    moved = set()

    for i in range(len(cart_map)):
        for j in range(len(cart_map[i])):
            position = cart_map[i][j]
            if not isinstance(position, tuple) or (i, j) in moved:
                continue

            cart = position

            diff_row, diff_col = CART_DIR[cart[0]]
            next_pos = cart_map[i+diff_row][j+diff_col]

            cart_map[i][j] = cart[2]

            if next_pos == Legend.intersection:
                cart = get_next_move(cart, next_pos)

            elif isinstance(next_pos, tuple):
                print '%s,%s' % (i+diff_row, j+diff_col)
                total_carts -= 2
                print total_carts
                cart = next_pos[2]

            elif next_pos == Legend.forward or next_pos == Legend.back:
                turn = hit_turn(cart[0], next_pos)
                cart = (turn, cart[1], next_pos)
            else:
                cart = (cart[0], cart[1], next_pos)

            cart_map[i+diff_row][j+diff_col] = cart
            moved.add((i+diff_row, j+diff_col))

    return total_carts