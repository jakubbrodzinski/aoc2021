import utils

def parse_line(line):
    (command,change) = line.split()
    change = int(change)
    if command == 'forward':
        return lambda p: (p[0] + change, p[1])
    elif command == 'up':
        return lambda p: (p[0], p[1] - change)
    elif command == 'down':
        return lambda p: (p[0], p[1] + change)


pos = (0,0)
for change_pos in utils.parse_and_map('i1', parse_line):
    pos = change_pos(pos)
print(pos)
print(pos[0]*pos[1])

# part2
print('--------------------')

def parse_line_with_aim(line):
    (command,change) = line.split()
    change = int(change)
    if command == 'forward':
        return lambda p: (p[0] + change, p[1] + p[2] * change, p[2])
    elif command == 'up':
        return lambda p: (p[0], p[1], p[2] - change)
    elif command == 'down':
        return lambda p: (p[0], p[1], p[2] + change)

pos = (0,0,0)
for change_pos in utils.parse_and_map('i1', parse_line_with_aim):
    pos = change_pos(pos)
print(pos)
print(pos[0]*pos[1])