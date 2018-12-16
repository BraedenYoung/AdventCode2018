from input_decorator import has_input


SAMPLE = '''
2018
'''

@has_input
def part_one(input):

    recipes = [3, 7]
    elves = {0: 0, 1: 1}

    while len(recipes) < int(input) + 10:
        score = sum([int(recipes[index]) for index in elves.values()])
        recipes.extend(list(str(score)))
        for elf, index in elves.iteritems():
            elves[elf] = (index + (int(recipes[index]) + 1)) % len(recipes)

    print ''.join(map(str, recipes[int(input):(int(input) + 10)]))


@has_input
def part_two(input):

    recipes = '37'
    elves = {0: 0, 1: 1}

    number = input.strip()
    while number != recipes[-len(number):]:
        score = sum([int(recipes[index]) for index in elves.values()])
        recipes += str(score)
        for elf, index in elves.iteritems():
            elves[elf] = (index + (int(recipes[index]) + 1)) % len(recipes)

    print recipes.index(number)
