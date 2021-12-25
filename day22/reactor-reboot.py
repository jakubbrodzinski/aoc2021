from collections import Counter


def parse_and_map(path: str, mapper):
    with open(path) as reader:
        return map(mapper, reader.readlines())


def parse_cuboid(line):
    switch, cuboid = line.split(' ')
    cuboid = tuple(int(d) for edge in cuboid.split(',') for d in edge[2:].split('..'))
    return cuboid, 1 if switch == 'on' else 0


def part1_filter(cuboid):
    for c in cuboid[0]:
        if c < -50 or c > 50:
            return False
    return True


def intersect(c1, c2):
    x0, x1 = max(c1[0], c2[0]), min(c1[1], c2[1])
    y0, y1 = max(c1[2], c2[2]), min(c1[3], c2[3])
    z0, z1 = max(c1[4], c2[4]), min(c1[5], c2[5])

    if x1 < x0 or y1 < y0 or z1 < z0:
        return None
    else:
        return x0, x1, y0, y1, z0, z1


def reboot_steps(cuboids):
    def count_on(on, off):
        on_count = 0
        for (x0, x1, y0, y1, z0, z1), score in on.items():
            on_count += (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1) * score
        for (x0, x1, y0, y1, z0, z1), score in off.items():
            on_count -= (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1) * score
        return on_count

    turned_on = Counter()
    turned_off = Counter()

    for c, switch in cuboids:
        double_off = Counter()
        for off, score in turned_off.items():
            i = intersect(c, off)
            if i is not None:
                double_off[i] += score

        double_on = Counter()
        for on, score in turned_on.items():
            i = intersect(c, on)
            if i is not None:
                double_on[i] += score

        turned_off.update(double_on)
        turned_on.update(double_off)
        if switch == 1:
            turned_on[c] += 1

    return count_on(turned_on, turned_off)


assert reboot_steps(filter(part1_filter, parse_and_map('t1', parse_cuboid))) == 39
assert reboot_steps(filter(part1_filter, parse_and_map('t2', parse_cuboid))) == 590784
print(reboot_steps(filter(part1_filter, parse_and_map('i1', parse_cuboid))))

assert reboot_steps(parse_and_map('t3', parse_cuboid)) == 2758514936282235
print(reboot_steps(parse_and_map('i1', parse_cuboid)))
