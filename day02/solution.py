from input_decorator import has_input


SAMPLE = '''
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
'''

SAMPLE2 = '''
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
'''

@has_input
def part_one(input):

    char_counts = {}
    pairs = []
    threes = []

    for box_id in input.strip().splitlines():
        counts = {}
        for c in set(box_id):
            counts[c] = box_id.count(c)

        if 2 in counts.values():
            pairs.append(box_id)
        if 3 in counts.values():
            threes.append(box_id)

        char_counts[box_id] = counts

    print len(pairs) * len(threes)


@has_input
def part_two(input):

    box_ids = input.strip().splitlines()
    comparison = ''
    finished = False

    for index, box_id in enumerate(box_ids):
        for chk_box in box_ids[index:]:
            comparison = [c for i, c in enumerate(box_id) if c == chk_box[i]]
            if len(comparison) == len(box_id) - 1:
                finished = True
                break
        if finished:
            break

    print ''.join(comparison)
