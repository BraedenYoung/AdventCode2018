from collections import defaultdict

from input_decorator import has_input


SAMPLE = '''
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
'''


class Registers(object):
    def __init__(self, op=0,  a=0, b=0, c=0):
        self.op = op
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return str([self.a, self.b, self.c, self.d])

    def get_state(self):
        return [self.op, self.a, self.b, self.c]

    def get_register(self, index):
        return ['a', 'b', 'c'][index]

    def get_value(self, index):
        if isinstance(index, int):
            return [self.op, self.a, self.b, self.c][index]
        return {'op': self.op, 'a': self.a, 'b': self.b, 'c': self.c}[index]

    def set_value(self, index, value):
        if index == 0 or index == 'op':
            self.op = value
        if index == 1 or index == 'a':
            self.a = value
        if index == 2 or index == 'b':
            self.b = value
        if index == 3 or index == 'c':
            self.c = value

    def call_method(self, func, kwargs):
        getattr(self, func)(**kwargs)

    def addr(self, **kwargs):
        self.set_value(kwargs['c'], self.get_value(kwargs['a']) + self.get_value(kwargs['b']))

    def addi(self, **kwargs):
        self.set_value(kwargs['c'], self.get_value(kwargs['a']) + kwargs['b'])

    def mulr(self, **kwargs):
        self.set_value(kwargs['c'], self.get_value(kwargs['a']) * self.get_value(kwargs['b']))

    def muli(self, **kwargs):
        self.set_value(kwargs['c'], self.get_value(kwargs['a']) * kwargs['b'])

    def banr(self, **kwargs):
        self.set_value(kwargs['c'], self.get_value(kwargs['a']) & self.get_value(kwargs['b']))

    def bani(self, **kwargs):
        self.set_value(kwargs['c'], self.get_value(kwargs['a']) & kwargs['b'])

    def borr(self, **kwargs):
        self.set_value(kwargs['c'], self.get_value(kwargs['a']) | self.get_value(kwargs['b']))

    def bori(self, **kwargs):
        self.set_value(kwargs['c'], self.get_value(kwargs['a']) | kwargs['b'])

    def setr(self, **kwargs):
        self.set_value(kwargs['c'], self.get_value(kwargs['a']))

    def seti(self, **kwargs):
        self.set_value(kwargs['c'], kwargs['a'])

    def gtir(self, **kwargs):
        self.set_value(kwargs['c'], int(kwargs['a'] > self.get_value(kwargs['b'])))

    def gtri(self, **kwargs):
        self.set_value(kwargs['c'], int(self.get_value(kwargs['a']) > kwargs['b']))

    def gtrr(self, **kwargs):
        self.set_value(kwargs['c'], int(self.get_value(kwargs['a']) > self.get_value(kwargs['b'])))

    def eqir(self, **kwargs):
        self.set_value(kwargs['c'], int(kwargs['a'] == self.get_value(kwargs['b'])))

    def eqri(self, **kwargs):
        self.set_value(kwargs['c'], int(self.get_value(kwargs['a']) == kwargs['b']))

    def eqrr(self, **kwargs):
        self.set_value(kwargs['c'], int(self.get_value(kwargs['a']) == self.get_value(kwargs['b'])))



FUNC = {
    'addr': Registers.addr.__name__,
    'addi': Registers.addi.__name__,

    'mulr': Registers.mulr.__name__,
    'muli': Registers.muli.__name__,

    'banr': Registers.banr.__name__,
    'bani': Registers.bani.__name__,

    'borr': Registers.borr.__name__,
    'bori': Registers.bori.__name__,

    'setr': Registers.setr.__name__,
    'seti': Registers.seti.__name__,

    'gtir': Registers.gtir.__name__,
    'gtri': Registers.gtri.__name__,
    'gtrr': Registers.gtrr.__name__,

    'eqir': Registers.eqir.__name__,
    'eqri': Registers.eqri.__name__,
    'eqrr': Registers.eqrr.__name__,
}



@has_input
def part_one(input):

    captures, _ = digest_captured(input.strip().splitlines())

    more_than_three = 0
    for e in captures:
        before, operation, after = e
        matches = 0
        for op_name, func in FUNC.iteritems():
            state = Registers(*before)
            state.call_method(func, operation)

            if state.get_state() == after:
                matches += 1

        if matches >= 3:
            more_than_three += 1

    print more_than_three


def digest_captured(capture_list):
    line_break = False
    digest_tests = False

    capture = []
    captures = []
    program = []

    while capture_list:
        line = capture_list[0]
        if not digest_tests:
            if len(line) == 0:
                capture_list.pop(0)
                if line_break:
                    digest_tests = True
                    line_break = False
                    continue

                line_break = True
                continue

            line_break = False

            # This is the instruction
            if len(capture) == 1:
                parsed = map(int, line.split(' '))

                line = {chr(ord('a')+i):c for i, c in enumerate(parsed[1:])}
                line['op'] = parsed[0]

            # It's the register state
            else:
                line = eval(line.split(': ')[1])

            capture.append(line)
            if len(capture) == 3:
                captures.append(list(capture))
                capture = []

        # Digest the tests
        else:
            if len(line) == 0:
                capture_list.pop(0)
                continue

            parsed = map(int, line.split(' '))
            line = {chr(ord('a')+i):c for i, c in enumerate(parsed[1:])}
            line['op'] = parsed[0]
            program.append(line)
        capture_list.pop(0)

    return captures, program


@has_input
def part_two(input):
    captures, program = digest_captured(input.strip().splitlines())

    # Get all possible usages
    operation_possible_numbers = defaultdict(set)
    for c in captures:
        before, operation, after = c
        for op_name, func in FUNC.iteritems():
            state = Registers(*before)
            state.call_method(func, operation)

            if state.get_state() == after:
                operation_possible_numbers[op_name].add(operation['op'])



    # Get the operation for a number
    op_map = {}
    while len(op_map) != len(FUNC):
        for op_name, occurences in operation_possible_numbers.iteritems():
            if len(occurences) == 1:
                op_num = occurences.pop()
                op_map[op_name] = op_num
                for occurences in operation_possible_numbers.values():
                    if op_num in occurences:
                        occurences.remove(op_num)

    # Evaluate the program
    state = Registers()
    for line in program:
        op_name = op_map.keys()[op_map.values().index(line['op'])]

        state.call_method(op_name, line)

    print state.op
