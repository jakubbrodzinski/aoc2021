import utils


def parse(packet):
    version = int(packet[0:3], 2)
    type_id = int(packet[3:6], 2)

    if type_id == 4:
        literal, rest = decode_literal(packet)
        return (version, type_id, literal), rest
    else:
        if packet[6] == '1':
            subpackets, rest = decode_subpackets_by_amount(packet)
            return (version, type_id, subpackets), rest
        else:
            subpackets, rest = decode_subpackets_by_size(packet)
            return (version, type_id, subpackets), rest


def decode_subpackets_by_size(packet):
    subpackets_size = int(packet[7:22], 2)
    rest = packet[22:22 + subpackets_size]
    subpackets = []
    while len(rest) > 6:
        sub, rest = parse(rest)
        subpackets.append(sub)

    return subpackets, packet[22 + subpackets_size:]


def decode_subpackets_by_amount(packet):
    subpackets_amount = int(packet[7:18], 2)
    rest = packet[18:]
    subpackets = []
    for i in range(0, subpackets_amount):
        sub, rest = parse(rest)
        subpackets.append(sub)

    return subpackets, rest


def decode_literal(packet):
    bits_processed = 6
    literal = ''
    while True:
        literal += packet[bits_processed + 1:bits_processed + 5]
        if packet[bits_processed] == '0':
            break
        bits_processed += 5

    bits_processed += 5

    return int(literal, 2), packet[bits_processed:]


def add_versions(parsed_packet):
    version_sum = 0

    version_sum += parsed_packet[0]
    if isinstance(parsed_packet[2], list):
        for sp in parsed_packet[2]:
            version_sum += add_versions(sp)
    return version_sum


def to_bin(input):
    binary_string = bin(int(input, 16))[2:]

    i = 0
    while input[i] == '0':
        binary_string = '0' * 4 + binary_string
        i += 1

    return '0' * ((4 - len(binary_string) % 4) % 4) + binary_string


def solve(parsed_packet):
    def get_op(type_id):
        if parsed_packet[1] == 0:
            return lambda acc, e: acc + e if acc is not None else e
        elif type_id == 1:
            return lambda acc, e: acc * e if acc is not None else e
        elif type_id == 2:
            return lambda acc, e: min(acc, e) if acc is not None else e
        elif type_id == 3:
            return lambda acc, e: max(acc, e) if acc is not None else e
        elif type_id == 5:
            return lambda acc, e: (1 if acc > e else 0) if acc is not None else e
        elif type_id == 6:
            return lambda acc, e: (1 if acc < e else 0) if acc is not None else e
        elif type_id == 7:
            return lambda acc, e: (1 if acc == e else 0) if acc is not None else e

    if parsed_packet[1] == 4:
        return parsed_packet[2]
    else:
        op = get_op(parsed_packet[1])
        result = None
        for sp in parsed_packet[2]:
            result = op(result, solve(sp))
        return result


def part1(input):
    return add_versions(parse(to_bin(input))[0])


assert part1("D2FE28") == 6
assert part1("8A004A801A8002F478") == 16
assert part1("620080001611562C8802118E34") == 12
assert part1("C0015000016115A2E0802F182340") == 23
assert part1("A0016C880162017C3686B18A3D4780") == 31

print(part1(utils.read_lines('i1')[0]))

# part2
print('--------')


def part2(input):
    return solve(parse(to_bin(input))[0])


assert part2("C200B40A82") == 3
assert part2("04005AC33890") == 54
assert part2("880086C3E88112") == 7
assert part2("CE00C43D881120") == 9
assert part2("D8005AC2A8F0") == 1
assert part2("F600BC2D8F") == 0
assert part2("9C005AC2F8F0") == 0
assert part2("9C0141080250320F1802104A08") == 1

print(part2(utils.read_lines('i1')[0]))
