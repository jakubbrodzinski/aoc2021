import utils


def parse(line):
    return list(map(lambda i: [int(c) for c in i.split(',')], line.split(' -> ')))


def create_simulation_board(ventures):
    def calculate_simulation_board_size():
        max_x, max_y = 0, 0
        for v in ventures:
            max_x = max(max_x, max(v[0][0], v[1][0]))
            max_y = max(max_y, max(v[0][1], v[1][1]))
        return max_x + 1, max_y + 1

    width, height = calculate_simulation_board_size()
    board = []
    for i in range(0, height):
        board.append([0] * width)
    return board


def apply_horizontal_and_vertical_ventures(board, ventures):
    def is_horizontal_venture(venture):
        return venture[0][1] == venture[1][1]

    def is_vertical_venture(venture):
        return venture[0][0] == venture[1][0]

    for venture in ventures:
        if is_horizontal_venture(venture):
            if venture[1][0] < venture[0][0]:
                venture[0], venture[1] = venture[1], venture[0]
            row = venture[0][1]
            for i in range(venture[0][0], venture[1][0] + 1):
                board[row][i] += 1
        elif is_vertical_venture(venture):
            if venture[1][1] < venture[0][1]:
                venture[0], venture[1] = venture[1], venture[0]
            column = venture[0][0]
            for i in range(venture[0][1], venture[1][1] + 1):
                board[i][column] += 1


def apply_diagonal_ventures(board, ventures):
    def is_diagonal_venture(venture):
        return venture[0][1] != venture[1][1] and venture[0][0] != venture[1][0]

    for venture in ventures:
        if is_diagonal_venture(venture):
            if venture[1][0] < venture[0][0]:  # we go always from left to right
                venture[0], venture[1] = venture[1], venture[0]

            if venture[1][1] < venture[0][1]:  # from up to down
                x,y = venture[0]
                times = venture[1][0]-venture[0][0] + 1
                for i in range(0,times):
                    board[y][x] += 1
                    x,y = x+1,y-1
            else:  # from down to up
                x, y = venture[0]
                times = venture[1][0] - venture[0][0] + 1
                for i in range(0, times):
                    board[y][x] += 1
                    x, y = x + 1, y + 1


def print_board(board):
    for r in board:
        print(list(map(lambda e: str(e) if e != 0 else '.', r)))


def count_dangerous_spots(board):
    sum = 0
    for r in board:
        for e in r:
            if e > 1:
                sum += 1
    return sum


ventures = list(utils.parse_and_map('i1', parse))
board = create_simulation_board(ventures)
apply_horizontal_and_vertical_ventures(board, ventures)
# print_board(board)
print(count_dangerous_spots(board))

# part2
print('-----------------------------------')

apply_diagonal_ventures(board,ventures)
# print_board(board)
print(count_dangerous_spots(board))