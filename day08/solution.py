from input_decorator import has_input


SAMPLE = '''
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
'''


class LicenseNode(object):
    def __init__(self, id, children_count, meta, children):
        self.id = id
        self.children_count = children_count
        self.meta = meta
        self.children = children

    def __str__(self):
        return '{id} : ({count}, {meta})'.format(id=self.id, count=self.children_count, meta=self.meta)


@has_input
def part_one(input):
    license = []
    for line in input.strip().splitlines():
        license.extend(map(int, line.split(' ')))
    print license

    node_map = {}
    parse_license(license=license, node_map=node_map)

    print sum([sum(node.meta) for node in node_map.values()])


def parse_license(license, node_map):
    node_id = get_next_node_id(node_map)
    children_count, meta_count = license[:2]

    node_map[node_id] = LicenseNode(node_id, children_count, None, [])

    if children_count == 0:
        node_map[node_id].meta = license[2:2+meta_count]
        print sum(node_map[node_id].meta)
        return license[meta_count + 2:], node_map[node_id]

    children = []
    license_segment = license[2:]
    while len(children) != children_count:

        license_segment, curr_children = parse_license(license_segment, node_map)
        children.append(curr_children)

    node_map[node_id].children = children
    node_map[node_id].meta = license_segment[:meta_count]

    return license_segment[meta_count:], children


def get_next_node_id(node_map):
    return len(node_map)


@has_input
def part_two(input):
    license = []
    for line in input.strip().splitlines():
        license.extend(map(int, line.split(' ')))
    print license

    node_map = {}
    _, _, values = parse_license_with_values(license=license, node_map=node_map)

    print values


def parse_license_with_values(license, node_map):
    node_id = get_next_node_id(node_map)
    children_count, meta_count = license[:2]

    node_map[node_id] = LicenseNode(node_id, children_count, None, [])

    if children_count == 0:
        node_map[node_id].meta = license[2:2+meta_count]
        return (license[meta_count + 2:],
                node_map[node_id],
                sum(node_map[node_id].meta))

    children = []
    license_segment = license[2:]
    values = []
    while len(children) != children_count:
        license_segment, curr_children, curr_value = parse_license_with_values(
            license_segment, node_map)
        values.append(curr_value)
        children.append(curr_children)

    node_map[node_id].children = children
    node_map[node_id].meta = license_segment[:meta_count]

    node_val = 0
    for val in node_map[node_id].meta:
        if val and val <= len(values):
            node_val += values[val-1]

    return license_segment[meta_count:], children, node_val
