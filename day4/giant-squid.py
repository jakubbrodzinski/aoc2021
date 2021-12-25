def read_file(file_name):
    def parse_board_line(line):
        return [int(line[0:2]), int(line[3:5]), int(line[6:8]), int(line[9:11]), int(line[12:14])]

    with open(file_name) as reader:
        lines = reader.readlines()

        turnes = list(map(lambda n: int(n), lines[0].split(',')))
        boards = []
        new_board = []
        for line in lines[2:]:
            line = line[:-1]
            if line == '':
                boards.append(new_board)
                new_board = []
            else:
                new_board.append(parse_board_line(line))
        if len(new_board) != 0:
            boards.append(new_board)

        return turnes, boards


def boards_to_dictionary(boards):
    b_dictionary = {}
    for b in range(0, len(boards)):
        for row in range(0, len(boards[0])):
            for column in range(0, len(boards[0])):
                v = boards[b][row][column]
                if not v in b_dictionary:
                    b_dictionary[v] = []
                b_dictionary[v].append((b, row, column))
    return b_dictionary


def is_lucky(b, r, c):
    is_lucky = True
    for i in range(0, len(b)):
        if b[r][i] != -1:
            is_lucky = False
            break
    if not is_lucky:
        for i in range(0, len(b)):
            if b[i][c] != -1:
                return False
        return True
    else:
        return True


def find_lucky_board(turnes, boards):
    bd = boards_to_dictionary(boards)
    for t in turnes:
        for match in bd[t]:
            boards[match[0]][match[1]][match[2]] = -1
            if is_lucky(boards[0], match[1], match[2]):
                return t, boards[match[0]]


input = read_file('i1')
lucky_turn, lucky_board = find_lucky_board(*input)

final_score = 0
for row in lucky_board:
    for v in row:
        if v != -1:
            final_score += v
final_score *= lucky_turn
print(final_score)

# part2
print('-----------')


def find_unlucky_board(turnes, boards):
    unlucky_boards = set(range(0, len(boards)))
    bd = boards_to_dictionary(boards)
    for t in turnes:
        for match in bd[t]:
            if match[0] in unlucky_boards:
                current_board = boards[match[0]]
                current_board[match[1]][match[2]] = -1
                if is_lucky(current_board, match[1], match[2]):
                    unlucky_boards.remove(match[0])
                    if len(unlucky_boards) == 0:
                        return t, current_board


input = read_file('i1')
last_turn, unlucky_board = find_unlucky_board(*input)

final_score = 0
for row in unlucky_board:
    for v in row:
        if v != -1:
            final_score += v
final_score *= last_turn
print(final_score)
