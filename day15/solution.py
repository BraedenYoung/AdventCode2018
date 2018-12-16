from collections import deque

from input_decorator import has_input


SAMPLE = '''
#########  
#G......#
#.E.#...# 
#..##..G# 
#...##..# 
#...#...# 
#.G...G.# 
#.....G.#     
#########    
'''


class Unit(object):
    def __init__(self, type, position, health, attack=3):
        self.type = type
        self.position = position
        self.health = health
        self.attack = attack

    def __str__(self):
        return self.type

    def get_type_and_health(self):
        return '%s(%s)' % (self.type, self.health)


class UnitTypes:
    elf = 'E'
    goblin = 'G'


class Terrain:
    wall = '#'
    ground = '.'


class DeadElf(Exception):
    pass


class BattleGround(object):
    def __init__(self, arena, elves, goblins, spare_no_elf=False):
        self.arena = arena
        self.elves = elves
        self.goblins = goblins
        self.spare_no_elf = spare_no_elf

    def __str__(self):
        map_string = ''
        for index, lane in enumerate(self.arena):
            map_string += '{lane} | {units}\n'.format(lane=''.join(map(str, lane)), units=map(lambda u: u.get_type_and_health(), self.get_lane_units(index)))

        return map_string

    def get_lane_units(self, index):
        return [pos for pos in self.arena[index] if isinstance(pos, Unit)]

    def move_unit(self, unit, position):
        row, col = unit.position
        new_row, new_col = position

        self.arena[row][col] = Terrain.ground
        self.arena[new_row][new_col] = unit
        unit.position = position

    def get_sorted_units(self):
        units = list(self.elves)
        units.extend(self.goblins)
        return sorted(units, key=lambda unit: unit.position)

    def unit_killed(self, unit):
        if unit.type == UnitTypes.elf:
            if self.spare_no_elf:
                raise DeadElf
            self.elves.remove(unit)
        else:
            self.goblins.remove(unit)

        row, col = unit.position
        self.arena[row][col] = Terrain.ground

    def neighbours(self, unit):
        row, col = unit.position
        ordered_adjacent = [self.arena[row-1][col], self.arena[row][col-1], self.arena[row][col+1], self.arena[row+1][col]]
        filtered_adjacent = []
        for pos in ordered_adjacent:
            if isinstance(pos, Unit):
                if pos.type == unit.type:
                    continue
            if pos == Terrain.wall:
                continue
            filtered_adjacent.append(pos)

        return filtered_adjacent

    def neighbour_positions(self, unit):
        row, col = unit.position
        ordered_adjacent = [(row-1, col), (row, col-1), (row, col+1), (row+1, col)]
        filtered_adjacent = []
        for pos in ordered_adjacent:
            curr_x, curr_y = pos
            p = self.arena[curr_x][curr_y]

            if isinstance(p, Unit):
                if p.type == unit.type:
                    continue
            if p == Terrain.wall:
                continue
            filtered_adjacent.append(pos)

        return filtered_adjacent

    def get_adjacent(self, position, exclude_unit=None):
        row, col = position
        ordered_adjacent = [(row-1, col), (row, col-1), (row, col+1), (row+1, col)]
        filtered_adjacent = []
        for pos in ordered_adjacent:
            curr_x, curr_y = pos
            p = self.arena[curr_x][curr_y]

            if isinstance(p, Unit):
                if p.type == exclude_unit:
                    continue
            if p == Terrain.wall:
                continue
            filtered_adjacent.append(pos)

        return filtered_adjacent


@has_input
def part_one(input):

    elves = []
    goblins = []
    arena = []

    for row_index, row in enumerate(input.strip().splitlines()):
        lane = []
        for column_index, position in enumerate(list(row)):
            if position == UnitTypes.elf:
                position = Unit(UnitTypes.elf, (row_index, column_index), 200)
                elves.append(position)
            elif position == UnitTypes.goblin:
                position = Unit(UnitTypes.goblin, (row_index, column_index), 200)
                goblins.append(position)

            lane.append(position)
        arena.append(lane)

    battleground = BattleGround(arena, elves, goblins)

    round = run_simulation(battleground)
    print (round + 1) * (sum([g.health for g in battleground.goblins]) + sum([e.health for e in battleground.elves]))


def run_simulation(battleground):
    round = 0
    while battleground.goblins and battleground.elves:
        units = battleground.get_sorted_units()
        for unit in units:
            neighbours = battleground.neighbours(unit)
            enemy_neighbours = [pos for pos in neighbours if isinstance(pos, Unit)]

            # Move
            if not enemy_neighbours:
                enemies = battleground.goblins if unit.type == UnitTypes.elf else battleground.elves
                nearest = []
                for enemy in enemies:
                    nearest.extend(battleground.neighbour_positions(enemy))

                choice, dist = get_closest(battleground, unit.position, nearest, unit.type)

                if choice:
                    for s in battleground.neighbour_positions(unit):
                        _, d = get_closest(battleground, s, [choice], unit.type)
                        if d == dist - 1:
                            battleground.move_unit(unit, s)
                            break

                neighbours = battleground.neighbours(unit)
                enemy_neighbours = [pos for pos in neighbours if isinstance(pos, Unit)]

            if any(enemy_neighbours):
                weakest_enemy = enemy_neighbours.pop(0)
                for enemy in enemy_neighbours:
                    if enemy.health < weakest_enemy.health:
                        weakest_enemy = enemy

                weakest_enemy.health -= unit.attack
                if weakest_enemy.health <= 0:

                    battleground.unit_killed(weakest_enemy)
                    units.remove(weakest_enemy)

                    if not battleground.elves or not battleground.goblins:
                        return round + 1

        round += 1
    return round


def get_closest(battle_ground, start, nearest, exclude_type):

    seen = set()
    queue = deque([(start, 0)])
    found_dist = None
    closest = []

    while queue:
        cell, dist = queue.popleft()
        if found_dist is not None and dist > found_dist:
            return closest, found_dist

        if cell in seen:
            continue

        seen.add(cell)
        if cell in nearest:
            return cell, dist

        for n in battle_ground.get_adjacent(cell, exclude_type):
            if n not in seen:
                queue.append((n, dist + 1))

    return closest, found_dist


@has_input
def part_two(input):

    elf_attack_power = 4
    while True:

        elves = []
        goblins = []
        arena = []

        for row_index, row in enumerate(input.strip().splitlines()):
            lane = []
            for column_index, position in enumerate(list(row)):
                if position == UnitTypes.elf:
                    position = Unit(UnitTypes.elf, (row_index, column_index), 200, elf_attack_power)
                    elves.append(position)
                elif position == UnitTypes.goblin:
                    position = Unit(UnitTypes.goblin, (row_index, column_index), 200)
                    goblins.append(position)

                lane.append(position)
            arena.append(lane)

        battleground = BattleGround(arena, elves, goblins, spare_no_elf=True)
        print battleground
        try:
            round = run_simulation(battleground)
        except DeadElf:
            elf_attack_power += 1
            continue

        print (round + 1) * (sum([g.health for g in battleground.goblins]) + sum([e.health for e in battleground.elves]))
