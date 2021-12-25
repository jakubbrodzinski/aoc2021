from functools import reduce


def compile(input):
    encoded_program = []
    with open(input) as reader:
        lines = reader.read().split('\n')
        for i in range(0, 14):
            div = int(lines[18 * i + 4].split()[2])
            arg1 = int(lines[18 * i + 5].split()[2])
            arg2 = int(lines[18 * i + 15].split()[2])
            encoded_program.append((arg1, arg2, div))
    return encoded_program


def run(z0, w, encoded_params):
    arg1, arg2, div = encoded_params
    if (z0 % 26) + arg1 != w:
        return (z0 // div) * 26 + w + arg2
    else:
        return z0 // div


assert reduce(lambda z0, params: run(z0, 1, params), compile('i1'), 0) == 158714800


# when the div is 26, then it's the only case when (z % 26) + arg1 != w can be False,
# since in every other line the arg >= 10
# when |z//div| >= |(z // div) * 26 + w + arg2| then z == 0
def generate_numbers():
    steps = compile('i1')
    valid_numbers = []

    def generate(z0, depth, acc):
        if depth == 14:
            if z0 == 0:
                valid_numbers.append(acc)
            return

        step = steps[depth]
        if step[2] == 26:
            next_num = z0 % 26 + step[0]
            if 0 < next_num < 10:
                generate(run(z0, next_num, step), depth + 1, acc + str(next_num))
        else:
            for next_num in range(9, 0, -1):
                generate(run(z0, next_num, step), depth + 1, acc + str(next_num))

    generate(0, 0, '')
    return list(map(lambda s: int(s),valid_numbers))

valid_serial_numbers = generate_numbers()
print(max(valid_serial_numbers))
print(min(valid_serial_numbers))
