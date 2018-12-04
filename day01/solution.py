from input_decorator import has_input

SAMPLE = '''
+1
+1
-2
'''

SAMPLE2 = '''
+7
+7
-2
-7
-4
'''


@has_input
def part_one(input):

    current_freq = 0
    for difference in input.strip().splitlines():
        current_freq += int(difference)

    print current_freq


@has_input
def part_two(input):
    current_freq = 0
    seen = set()
    found = None

    while not found:
        for difference in input.strip().splitlines():
            seen.add(current_freq)
            current_freq += int(difference)
            if current_freq in seen:
                found = current_freq
                break
    print found
