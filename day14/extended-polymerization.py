from collections import Counter

import utils


def parse_input(file):
    def to_freq_map(t):
        freq_map = Counter()
        for i in range(0, len(t) - 1):
            k = t[i] + t[i + 1]
            freq_map[k] += 1
        return freq_map

    lines = utils.read_lines(file)

    rules = {}
    for i in range(2, len(lines)):
        i_rule, o_rule = lines[i][:-1].split(' -> ')
        rules[i_rule] = o_rule

    return to_freq_map(lines[0][:-1]), rules


freq_map, rules = parse_input('i1')


def step(f_map):
    nf_map = Counter()
    for k, v in f_map.items():
        if k in rules:
            r_in = rules[k]
            nf_map[k[0] + r_in] += v
            nf_map[r_in + k[1]] += v
    return nf_map


def steps(f_map, n):
    def get_result(f_map):
        occurs = Counter()
        for k, v in f_map.items():
            occurs[k[0]] += v
            occurs[k[1]] += v
        occurs = Counter({k: (v + 1) // 2 for k, v in occurs.items()})

        sorted_occurs = occurs.most_common()

        return sorted_occurs[0][1] - sorted_occurs[-1][1]

    for i in range(0, n):
        f_map = step(f_map)
    return get_result(f_map)


print(steps(freq_map, 10))
print('----')
print(steps(freq_map, 40))
