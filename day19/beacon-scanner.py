from collections import Counter
#thanks joshbduncan for providing such simple solution that i was albe to reimplement on my own!
ROTATIONS = [((1, 0, 2), (1, -1, 1)), ((2, 0, 1), (-1, 1, -1)), ((1, 2, 0), (-1, 1, -1)), ((0, 2, 1), (1, 1, -1)),
             ((2, 1, 0), (-1, 1, 1)), ((0, 2, 1), (-1, 1, 1)), ((2, 0, 1), (1, -1, -1)), ((0, 1, 2), (1, 1, 1)),
             ((1, 0, 2), (-1, -1, -1)), ((1, 2, 0), (1, 1, 1)), ((1, 0, 2), (1, 1, -1)), ((1, 2, 0), (-1, -1, 1)),
             ((2, 0, 1), (-1, -1, 1)), ((2, 1, 0), (1, -1, 1)), ((0, 2, 1), (-1, -1, -1)), ((1, 2, 0), (1, -1, -1)),
             ((0, 1, 2), (-1, -1, 1)), ((2, 1, 0), (-1, -1, -1)), ((0, 2, 1), (1, -1, 1)), ((0, 1, 2), (-1, 1, -1)),
             ((2, 0, 1), (1, 1, 1)), ((0, 1, 2), (1, -1, -1)), ((2, 1, 0), (1, 1, -1)), ((1, 0, 2), (-1, 1, 1))]


def parse_input(path):
    scanners = []
    with open(path) as reader:
        for scanner in reader.read().split('\n\n'):
            beacons = []
            for beacon in scanner.split('\n')[1:]:
                beacons.append(tuple([int(b) for b in beacon.split(',')]))

            scanners.append(beacons)
    return scanners


def apply_rotation(p, rotation):
    r, signs = rotation[0], rotation[1]
    return signs[0] * p[r[0]], signs[1] * p[r[1]], signs[2] * p[r[2]]


def add_points(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return x1 + x2, y1 + y2, z1 + z2


def subtract_points(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return x1 - x2, y1 - y2, z1 - z2


def max_offset(offsets):
    max_value = 0
    max_element = None
    for offset, common_scanners in offsets:
        if common_scanners > max_value:
            max_value = common_scanners
            max_element = offset
    return max_element, max_value


def invert(p):
    x, y, z = p
    return -x, -y, -z


def manhattan_distance(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def match_beacons(scanners):
    beacons = set(scanners.pop(0))
    matched_offsets = set()
    while scanners:
        scanner = scanners.pop(0)
        matched = False
        for rotation in ROTATIONS:
            offsets = Counter()
            for beacon in scanner:
                rotated_point = apply_rotation(beacon, rotation)
                for point in beacons:
                    offsets[subtract_points(rotated_point, point)] += 1

            offset, common_scanners = max_offset(offsets.items())
            if common_scanners >= 12:
                offset = invert(offset)
                matched = True
                for beacon in scanner:
                    rotated_point = apply_rotation(beacon, rotation)
                    beacons.add(add_points(rotated_point, offset))
                matched_offsets.add(offset)
                print(offset, common_scanners)
                break

        if not matched:
            scanners.append(scanner)

    return beacons, matched_offsets


assert apply_rotation((5, 10, 15), ((1, 0, 2), (1, -1, 1))) == (10, -5, 15)
test_case = match_beacons(parse_input('t1'))
assert len(test_case[0]) == 79
assert test_case[1] == {(68, -1246, -43), (-20, -1133, 1061), (1105, -1205, 1229),
                        (-92, -2380, -20)}

result = match_beacons(parse_input('i1'))
print(len(result[0]))
print('-------')


def part2(offsets):
    max = 0
    for o1 in offsets:
        for o2 in offsets:
            if o1 != o2:
                distance = manhattan_distance(o1, o2)
                if distance > max:
                    max = distance
    return max


assert part2(test_case[1]) == 3621
print(part2(result[1]))
