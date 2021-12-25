import re


def parse(input):
    groups = re.match(r'[a-z :]+(x=(-?\d+)..(-?\d+)), (y=(-?\d+)..(-?\d+))', input).groups()
    return int(groups[1]), int(groups[2]), int(groups[4]), int(groups[5])


def simulate(dx, dy, restrictions):
    xmin, xmax, ymin, ymax = restrictions
    x, y = 0, 0
    while y + dy >= ymin and x + dx <= xmax:
        if dx > 0:
            x += dx
            dx -= 1

        y += dy
        dy -= 1

    if y <= ymax and x >= xmin:
        return True
    else:
        return False


def highest_point(input):
    def calculate_heighest_point(dy):
        return sum(range(dy, 0, -1))

    def find_optimal_x(xmax):
        xstart = 0
        distance = 0
        while distance + xstart + 1 <= xmax:
            xstart += 1
            distance += xstart

        return xstart

    restrictions = parse(input)
    xmin, xmax, ymin, ymax = restrictions

    xstart = find_optimal_x(xmax)
    max_height_details = (0, 0, 0)

    for ystart in range(ymin, -ymin):
        if simulate(xstart, ystart, restrictions):
            hp = calculate_heighest_point(ystart)
            if hp > max_height_details[2]:
                max_height_details = (xstart, ystart, hp)

        ystart += 1

    return max_height_details


assert highest_point('target area: x=20..30, y=-10..-5') == (7, 9, 45)
print(highest_point('target area: x=88..125, y=-157..-103')[2])


def possible_shots(input):
    restrictions = parse(input)
    xmin, xmax, ymin, ymax = restrictions

    shots = []
    for xstart in range(0, xmax+1):
        for ystart in range(ymin, -ymin):
            if simulate(xstart, ystart, restrictions):
                shots.append((xstart, ystart))

    return len(shots)


assert possible_shots('target area: x=20..30, y=-10..-5') == 112
print(possible_shots('target area: x=88..125, y=-157..-103'))
