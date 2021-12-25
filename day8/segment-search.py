import utils


def parse_line(l):
    l = l[:-1].split(' | ')

    patterns = l[0].split(' ')
    patterns = sorted(patterns, key=lambda p: len(p))
    patterns = [set(p) for p in patterns]

    outputs = l[1].split(' ')
    outputs = [''.join(sorted(o)) for o in outputs]

    return patterns, outputs


def decode_patterns(encoded_patterns):
    def to_key(s):
        return ''.join(sorted(s))

    t = {}

    def decode_1_7_4_8():
        t[to_key(encoded_patterns[0])] = '1'
        t[to_key(encoded_patterns[1])] = '7'
        t[to_key(encoded_patterns[2])] = '4'
        t[to_key(encoded_patterns[-1])] = '8'

    def decode_0_6_9_and_3_2_5():
        len_6 = [encoded_patterns[-2], encoded_patterns[-3], encoded_patterns[-4]]
        six = next(filter(lambda p: not encoded_patterns[0].issubset(p), len_6))
        len_6.remove(six)
        t[to_key(six)] = '6'

        zero = next(filter(lambda p: not encoded_patterns[2].issubset(p), len_6))
        len_6.remove(zero)
        t[to_key(zero)] = '0'

        nine = len_6.pop()
        t[to_key(nine)] = '9'

        len_5 = [encoded_patterns[3], encoded_patterns[4], encoded_patterns[5]]
        three = next(filter(lambda p: encoded_patterns[0].issubset(p), len_5))
        len_5.remove(three)
        t[to_key(three)] = '3'

        upper = encoded_patterns[0].difference(six).pop()
        two = next(filter(lambda p: upper in p, len_5))
        t[to_key(two)] = '2'

        five = next(filter(lambda p: upper not in p, len_5))
        t[to_key(five)] = '5'



    decode_1_7_4_8()
    decode_0_6_9_and_3_2_5()
    return t


def decode_p1(patterns, outputs):
    sum = 0
    for out in outputs:
        if int(patterns.get(out, 0)) in (1, 4, 8, 7):
            sum += 1
    return sum


def decode_p2(patterns, outputs):
    return int(''.join([patterns.get(o, '1') for o in outputs]))


input = list(utils.parse_and_map('i1', parse_line))

sum_p1 = 0
sum_p2 = 0
for i in input:
    patterns = decode_patterns(i[0])
    sum_p1 += decode_p1(patterns, i[1])
    sum_p2 += decode_p2(patterns, i[1])

print(sum_p1)

# part2
print('-----------')

print(sum_p2)
