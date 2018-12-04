from input_decorator import has_input


SAMPLE = '''
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
'''


class Claim:
    def __init__(self, padding_left, padding_top, width, height):
        self.padding_left = padding_left
        self.padding_top = padding_top
        self.width = width
        self.height = height

    def __str__(self):
        return "padding ({0}, {1}), size ({2}, {3})".format(self.padding_left,
                                                            self.padding_top,
                                                            self.width,
                                                            self.height)


class Fabric:
    def __init__(self, size=8):
        self.sheet = [[0 for _ in range(size)] for _ in range(size)]

    def __str__(self):
        return '\n'.join(map(lambda line: '|'.join(map(str, line)), self.sheet))


def parse_input(input):
    claims = {}
    for line in input.strip().splitlines():
        claim_id, dimensions = line.split('@')
        claim_id = claim_id[1:]

        padding, size = dimensions.split(':')
        padding_left, padding_top = map(int, padding.split(','))

        width, height = map(int, size.split('x'))
        claims[claim_id] = Claim(padding_left, padding_top, width, height)

    return claims


@has_input
def part_one(input):

    fabric = Fabric(size=1000)
    claims = parse_input(input)

    for claim_id, claim in claims.iteritems():
        for row_index, row in enumerate(fabric.sheet[claim.padding_top:claim.padding_top + claim.height]):
            for col_index, patch in enumerate(row[claim.padding_left:claim.padding_left + claim.width]):
                if fabric.sheet[claim.padding_top + row_index][claim.padding_left + col_index] != 0:
                    fabric.sheet[claim.padding_top + row_index][claim.padding_left + col_index] = 'x'
                    continue

                fabric.sheet[claim.padding_top + row_index][claim.padding_left + col_index] = claim_id

    contention_count = 0
    for row in fabric.sheet:
        for patch in row:
            if patch == 'x':
                contention_count += 1

    print contention_count


@has_input
def part_two(input):

    fabric = Fabric(size=1000)
    claims = parse_input(input)

    for claim_id, claim in claims.iteritems():
        for row_index, row in enumerate(fabric.sheet[claim.padding_top:claim.padding_top + claim.height]):
            for col_index, patch in enumerate(row[claim.padding_left:claim.padding_left + claim.width]):
                if fabric.sheet[claim.padding_top + row_index][claim.padding_left + col_index] != 0:

                    fabric.sheet[claim.padding_top + row_index][claim.padding_left + col_index] = 'x'
                    continue

                fabric.sheet[claim.padding_top + row_index][claim.padding_left + col_index] = claim_id

    for claim_id, claim in claims.iteritems():
        contention = False
        for row_index, row in enumerate(fabric.sheet[claim.padding_top:claim.padding_top + claim.height]):
            for col_index, patch in enumerate(row[claim.padding_left:claim.padding_left + claim.width]):
                if fabric.sheet[claim.padding_top + row_index][claim.padding_left + col_index] != claim_id:
                    contention = True
                    break
            if contention:
                break
        if not contention:
            print claim_id
            break
