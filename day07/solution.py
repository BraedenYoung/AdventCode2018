from collections import defaultdict

from input_decorator import has_input


SAMPLE = '''
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
'''

# TASK = 0
# WORKER_COUNT = 2

TASK = 60
WORKER_COUNT = 5

@has_input
def part_one(input):

    instructions = defaultdict(list)
    dependencies = defaultdict(list)

    for line in input.strip().splitlines():
        first_step, second_step = line.split(" must be finished before step ")
        first_step = first_step[-1]
        second_step = second_step[0]

        instructions[first_step].append(second_step)
        dependencies[second_step].append(first_step)

    possible_roots = set(instructions.keys())
    for children in instructions.values():
        for child in children:
            if child in possible_roots:
                possible_roots.remove(child)

    starting_instructions = set(instructions.keys()) - set(dependencies.keys())

    print get_instruction_order(starting_instructions, instructions, dependencies)


def get_instruction_order(starting_instructions, instructions, depenendencies):

    available_instructions = sorted(starting_instructions)
    instruction_order = [available_instructions.pop(0)]

    if not available_instructions:
        # There was a central root node
        available_instructions = sorted(instructions[instruction_order[0]])

    while available_instructions:
        instruction = get_next_instruction(instruction_order, available_instructions, depenendencies)
        instruction_order.append(instruction)
        available_instructions.remove(instruction)

        for inst in instructions[instruction]:
            if inst not in instruction_order and inst not in available_instructions:
                available_instructions.append(inst)

        available_instructions.sort()

    return ''.join(instruction_order)


def get_next_instruction(instruction_order, available_instructions, depenendencies):
    for possible_inst in available_instructions:
        dependency_issue = False
        for dependency in depenendencies[possible_inst]:
            if dependency not in instruction_order:
                dependency_issue = True
                break
        if not dependency_issue:
            return possible_inst


@has_input
def part_two(input):

    instructions = defaultdict(list)
    dependencies = defaultdict(list)

    for line in input.strip().splitlines():
        first_step, second_step = line.split(" must be finished before step ")
        first_step = first_step[-1]
        second_step = second_step[0]

        instructions[first_step].append(second_step)
        dependencies[second_step].append(first_step)

    possible_roots = set(instructions.keys())
    for children in instructions.values():
        for child in children:
            if child in possible_roots:
                possible_roots.remove(child)

    starting_instructions = set(instructions.keys()) - set(dependencies.keys())

    print get_instruction_order_for_workers(starting_instructions, instructions, dependencies)


def get_instruction_order_for_workers(starting_instructions, instructions, depenendencies):

    available_instructions = sorted(starting_instructions)

    instruction_order = []
    current_time = 0

    workers = {}
    for i in range(WORKER_COUNT):
        workers[i] = (-1, '#')

    while len(instruction_order) + 1 != len(instructions.keys()) or available_instructions :

        assign_worker(workers, available_instructions, instruction_order, depenendencies)

        current_time += 1
        update_workers(workers, instructions, available_instructions, instruction_order)

    return ''.join(instruction_order), current_time


def check_on_workers(workers):
    return sum([w[0] for w in workers.values()])


def assign_worker(workers, available_instructions, instruction_order, depenendencies):
    for index, worker in workers.iteritems():
        if worker[0] > 0:
            continue
        elif worker[0] <= 0 and available_instructions:
            available_instructions.sort()
            task = get_next_instruction(instruction_order, available_instructions, depenendencies)
            if task:
                available_instructions.remove(task)
                workers[index] = ((ord(task) - 64) + TASK, task)

        else:
            workers[index] = (-1, '#')


def update_workers(workers, instructions, available_instructions, instruction_order):
    for worker, task in workers.iteritems():
        time, inst = task
        if time > 0:

            workers[worker] = (time - 1, inst)

            if workers[worker][0] == 0:
                instruction_order.append(inst)
                workers[worker] = (-1, '#')
                for new_tasks in instructions[inst]:
                    if new_tasks not in instruction_order and new_tasks not in available_instructions:
                        available_instructions.append(new_tasks)
