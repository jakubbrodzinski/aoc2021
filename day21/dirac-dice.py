from collections import Counter


def throw_and_sum(nth_roll):
    return 3 * 3 * (nth_roll - 1) + 6


def game(p1_pos, p2_pos):
    def play_turn(pos, score, turn):
        turn += 1
        pos = (pos + throw_and_sum(turn) - 1) % 10 + 1
        return pos, score + pos, turn

    p1_score, p2_score = 0, 0
    turn = 0
    while True:
        p1_pos, p1_score, turn = play_turn(p1_pos, p1_score, turn)
        if p1_score >= 1000:
            break

        p2_pos, p2_score, turn = play_turn(p2_pos, p2_score, turn)
        if p2_score >= 1000:
            break

    return p1_score, p2_score, turn * 3


def res(r):
    return min(r[0], r[1]) * r[2]


assert throw_and_sum(1) == 6
assert throw_and_sum(8) == 69
assert game(4, 8) == (1000, 745, 993)
assert res(game(4, 8)) == 739785

print(res(game(6, 1)))

# part2
print('--------------')


def quantum_game(p1_pos, p2_pos):
    solutions = {}

    def throw(p1, p2, rolls_sum, throw_num):
        if throw_num == 3:
            pos = (p1[2] + rolls_sum - 1) % 10 + 1
            p1 = (p1[0], p1[1] + pos, pos)
            if p1[1] >= 21:
                return Counter({p1[0]: 1})
            else:
                return start_turn(p2, p1)
        else:
            winners = Counter({'p1': 0, 'p2': 0})
            winners += throw(p1, p2, rolls_sum + 1, throw_num + 1)
            winners += throw(p1, p2, rolls_sum + 2, throw_num + 1)
            winners += throw(p1, p2, rolls_sum + 3, throw_num + 1)
            return winners

    def start_turn(p1, p2):
        if (p1, p2) in solutions:
            return solutions.get((p1, p2))
        else:
            winners = Counter({'p1': 0, 'p2': 0})
            winners += throw(p1, p2, 1, 1)
            winners += throw(p1, p2, 2, 1)
            winners += throw(p1, p2, 3, 1)
            solutions[(p1, p2)] = winners
            return winners

    p1, p2 = ('p1', 0, p1_pos), ('p2', 0, p2_pos)
    return start_turn(p1, p2)


assert dict(quantum_game(4, 8)) == {'p1': 444356092776315, 'p2': 341960390180808}

print(quantum_game(6, 1).most_common(1)[0][1])
