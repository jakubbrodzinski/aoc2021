import utils

# when we compute pixels that are "part of ifnite image" but not the part of "input". Either 0 or 511.
def inf_pixel_val(algorithm, round):
    if not algorithm[0]:
        return 0

    if not algorithm[-1]:
        return (round-1) % 2
    else:
        return 1


def parse_input(lines):
    algorithm = list(map(lambda c: True if c == '#' else False, lines[0][:-1]))

    dimensions = (len(lines) - 2, len(lines[2]) - 1)

    ligh_pixels = set()
    dark_pixels = set()
    for row in range(2, len(lines)):
        for column in range(0, len(lines[row]) - 1):
            if lines[row][column] == '#':
                ligh_pixels.add((row - 2, column))
            else:
                dark_pixels.add((row - 2, column))

    return algorithm, ligh_pixels, dark_pixels, dimensions


def enchance_image(algorithm, light_pixels, dark_pixels, dims, default_pixel):
    def get_pixel(row, column):
        if (row, column) in light_pixels:
            return 1
        elif (row, column) in dark_pixels:
            return 0
        else:
            return default_pixel

    def enchance_pixel(row, column):
        bin_number = 0
        for p in [(row - 1, column - 1), (row - 1, column), (row - 1, column + 1), (row, column - 1), (row, column),
                  (row, column + 1), (row + 1, column - 1), (row + 1, column), (row + 1, column + 1)]:
            tmp = get_pixel(*p)
            bin_number = bin_number << 1
            bin_number += tmp

        return algorithm[bin_number]

    enchanced_light_pixels = set()
    enchanced_dark_pixels = set()

    for row in range(0, dims[0] + 2):
        for column in range(0, dims[1] + 2):
            if enchance_pixel(row - 1, column - 1):
                enchanced_light_pixels.add((row, column))
            else:
                enchanced_dark_pixels.add((row, column))

    return enchanced_light_pixels, enchanced_dark_pixels, (dims[0] + 2, dims[1] + 2)


algorithm, light_pixels, dark_pixels, dims = parse_input(utils.read_lines('t1'))
light_pixels, dark_pixels, dims = enchance_image(algorithm, light_pixels, dark_pixels, dims,
                                                 inf_pixel_val(algorithm, 1))
light_pixels, dark_pixels, dims = enchance_image(algorithm, light_pixels, dark_pixels, dims,
                                                 inf_pixel_val(algorithm, 2))
assert len(light_pixels) == 35

for i in range(0, 48):
    def_pixel = inf_pixel_val(algorithm, i + 3)
    light_pixels, dark_pixels, dims = enchance_image(algorithm, light_pixels, dark_pixels, dims, def_pixel)
assert len(light_pixels) == 3351

algorithm, light_pixels, dark_pixels, dims = parse_input(utils.read_lines('i1'))

light_pixels, dark_pixels, dims = enchance_image(algorithm, light_pixels, dark_pixels, dims,
                                                 inf_pixel_val(algorithm, 1))
light_pixels, dark_pixels, dims = enchance_image(algorithm, light_pixels, dark_pixels, dims,
                                                 inf_pixel_val(algorithm, 2))
print(len(light_pixels))

# part2 uses comp results from part1
print('------')

for i in range(0, 48):
    def_pixel = inf_pixel_val(algorithm, i + 3)
    light_pixels, dark_pixels, dims = enchance_image(algorithm, light_pixels, dark_pixels, dims, def_pixel)

print(len(light_pixels))


def print_image(lp):
    d = 11
    for i in range(0, d):
        for j in range(0, d):
            if (i, j) in lp:
                print('#', end='')
            else:
                print('.', end='')
        print()
