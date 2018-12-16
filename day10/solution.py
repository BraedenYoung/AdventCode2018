from input_decorator import has_input

import re

SAMPLE = '''
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
'''


class Point(object):
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def __str__(self):
        return 'pos : ({px}, {py}), vel : ({vx}, {vy})'.format(
            px=self.pos[0], py=self.pos[1], vx=self.vel[0], vy=self.vel[1])

    def px(self):
        return self.pos[0]

    def py(self):
        return self.pos[1]

    def vx(self):
        return self.vel[0]

    def vy(self):
        return self.vel[1]


MAP_SIZE = 45

@has_input
def part_one(input):

    input = SAMPLE

    position_pattern = re.compile('(position=<.*> )')
    velocity_pattern = re.compile('(velocity=<.*>$)')

    points = []

    for line in input.strip().splitlines():
        position_x, position_y = map(int, position_pattern.search(line).group(1).split('=')[-1][1:-2].split(', '))
        velocity_x, velocity_y = map(int, velocity_pattern.search(line).group(1).split('=')[-1][1:-1].split(', '))
        points.append(Point((position_x, position_y), (velocity_x, velocity_y)))

    for point in points:
        print point

    tundra = create_map()
    print_map(tundra)

    position_points(tundra, points)
    print ''

    print_map(tundra)

    for num in range(5):
        print('ITERATION :%s' % num)
        for point in points:
            update_point(point)
        tundra = create_map()
        position_points(tundra, points)
        print_map(tundra)

def update_point(point):
    point.pos = ((point.px() + point.vx()), (point.py() + point.vy()))

def position_points(area, points):
    for point in points:
        area[point.px()+(MAP_SIZE/2)-1][point.py()+(MAP_SIZE/2)-1] = '#'


def create_map():
    return [['.' for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]


def print_map(area):
    print '\n'.join(['|'.join(l) for l in area])


@has_input
def part_two(input):
    pass
