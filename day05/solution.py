from input_decorator import has_input

SAMPLE = '''
dabAcCaCBAcCcaDA
'''


@has_input
def part_one(input):

    polymer = input.strip()

    reaction = True
    while reaction:
        polymer, reaction = polymer_reaction(polymer)

    print len(polymer)


def polymer_reaction(polymer):
    reaction = False
    for index, unit in enumerate(polymer):
        if index == len(polymer) - 1:
            break

        if unit.lower() == polymer[index + 1].lower():
            if unit != polymer[index + 1]:
                polymer = polymer[:index] + polymer[index + 2:]
                reaction = True
                break

    return polymer, reaction


def polymer_reaction_replace(polymer):
    reaction = False
    for index, unit in enumerate(polymer):
        if unit == '*':
            continue

        if index == len(polymer) - 1:
            break

        if unit.lower() == polymer[index + 1].lower():
            if unit != polymer[index + 1]:
                polymer[index] = '*'
                polymer[index + 1] = '*'
                reaction = True
                break

    return polymer, reaction


@has_input
def part_two(input):

    print 'using polymer_reaction_replace'

    polymer = input.strip()

    unit_evals = {}

    units = set(polymer.lower())

    for unit in units:
        test_polymer = polymer.replace(unit, '').replace(unit.upper(), '')
        unit_evals[unit] = run_reaction_test(test_polymer)

    min_unit = (unit[0], unit_evals[unit[0]])
    for unit, val in unit_evals.iteritems():
        if val < min_unit[1]:
            min_unit = (unit, val)

    print min_unit


def run_reaction_test(polymer):
    reaction = True
    while reaction:
        polymer, reaction = polymer_reaction(polymer)

    return len(polymer)