from collections import namedtuple, Counter
from itertools import product

Player = namedtuple('Player', ['score', 'pos'])


def iterate(player: Player, inc):
    new_pos = (player.pos + inc) % 10
    new_score = player.score + new_pos + 1
    return Player(new_score, new_pos)


def solve1():
    player_0 = Player(0, 8)
    player_0_inc = 6
    player_1 = Player(0, 9)
    player_1_inc = 15

    steps = 0
    while True:
        player_0 = iterate(player_0, player_0_inc)
        player_0_inc = (player_0_inc + 18) % 10
        steps += 3
        if player_0.score >= 1000:
            print(player_0, player_1, steps)
            return player_1.score * steps
        player_1 = iterate(player_1, player_1_inc)
        player_1_inc = (player_1_inc + 18) % 10
        steps += 3
        if player_1.score >= 1000:
            print(player_0, player_1, steps)
            return player_0.score * steps


possible = Counter(map(sum, product([1, 2, 3], repeat=3)))
cache = dict()


def univers_in_which_playern_wins(player0, player1):
    label = (player0.score, player0.pos, player1.score, player1.pos)
    if label in cache:
        return cache[label]
    wins0, wins1 = 0, 0
    for dice0, count0 in possible.items():
        new_player0 = iterate(player0, dice0)
        if new_player0.score >= 21:
            wins0 += count0
            continue
        for dice1, count1 in possible.items():
            new_player1 = iterate(player1, dice1)
            if new_player1.score >= 21:
                wins1 += count1 * count0
                continue
            new_wins0, new_wins1 = univers_in_which_playern_wins(new_player0, new_player1)
            wins0 += new_wins0 * count0 * count1
            wins1 += new_wins1 * count0 * count1
    cache[label] = (wins0, wins1)
    return wins0, wins1


def solve2():
    player_0 = Player(0, 8)
    player_1 = Player(0, 9)
    wins0, wins1 = univers_in_which_playern_wins(player_0, player_1)
    return wins0, wins1


print(solve2())
