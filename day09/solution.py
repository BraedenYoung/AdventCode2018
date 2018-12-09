from collections import defaultdict
from  collections import deque

from input_decorator import has_input


SAMPLE = '''
10 players; last marble is worth 1618 points
'''
# 9 players; last marble is worth 25 points
# 10 players; last marble is worth 1618 points


@has_input
def part_one(input):
    input = input.split(' ')
    players, highest_marble = map(int, (input[0], input[-2]))

    ring = deque([0, ])
    start_game(ring, players, highest_marble)


def start_game(ring, players, highest_marble):
    player_score = defaultdict(int)
    current_player = 1

    for marble in range(1, highest_marble + 1):
        round_score = play_marble(ring, marble)
        player_score[current_player] += round_score
        current_player = (current_player + 1) % players

    print max(player_score.values())


def play_marble(ring,  marble):
    score = 0
    if marble % 23 == 0:
        score += marble
        ring.rotate(7)
        score += ring.pop()
        ring.rotate(-1)
        return score

    ring.rotate(-1)
    ring.append(marble)
    return score

@has_input
def part_two(input):
    input = input.split(' ')
    players, highest_marble = map(int, (input[0], input[-2]))

    ring = deque([0, ])
    start_game(ring, players, highest_marble*100)
