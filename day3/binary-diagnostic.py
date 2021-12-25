import utils

numbers = list(utils.parse_and_map('i1', lambda l: l[:-1]))
LENGTH = len(numbers[0])


def power_consumption(numbers):
    MASK = (1 << (LENGTH)) - 1

    def most_common_bits():
        mcbs = [0] * LENGTH
        for n in numbers:
            for i in range(0, LENGTH):
                temp = mcbs[i]
                mcbs[i] = temp + 1 if n[i] == '1' else temp - 1
        return ['1' if mcb > 0 else '0' for mcb in mcbs]

    gamma_rate_bits = ''.join(most_common_bits())

    gamma_rate = int(gamma_rate_bits, 2)
    power_consumption = gamma_rate * (~gamma_rate & MASK)
    return power_consumption


print(power_consumption(numbers))

# part2
print('--------------')


def common_bits_by_decider(numbers, decider):
    def common_bits(numbers, bit):
        one = []
        zero = []
        counter = 0
        for n in numbers:
            if n[bit] == '0':
                counter -= 1
                zero.append(n)
            else:
                counter += 1
                one.append(n)
        return decider(counter, zero, one)

    bit = 0
    while len(numbers) != 1:
        numbers = common_bits(numbers, bit)
        bit += 1
    return numbers[0]


def oxygen_rating(numbers):
    decider = lambda counter, zeros, ones: zeros if counter < 0 else ones
    return int(common_bits_by_decider(numbers, decider), 2)


def co2_rating(numbers):
    decider = lambda counter, zeros, ones: ones if counter < 0 else zeros
    return int(common_bits_by_decider(numbers, decider), 2)


print(oxygen_rating(numbers) * co2_rating(numbers))