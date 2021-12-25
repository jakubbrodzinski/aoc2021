import utils


def find_low_points(board):
    low_points = []
    for r in range(1, len(board) - 1):
        left, elt, right = 10, 10, board[r][1]
        for c in range(1, len(board[r]) - 1):
            left = elt
            elt = right
            right = board[r][c + 1]
            top, down = board[r - 1][c], board[r + 1][c]
            if elt < left and elt < right and elt < top and elt < down:
                low_points.append((r, c))

    return low_points


def count_risk_levels(board, low_points):
    risk_levels = []
    for lp in low_points:
        risk_levels.append(board[lp[0]][lp[1]] + 1)
    return risk_levels


board = list(utils.parse_and_map('t1', lambda line: [10] + [int(i) for i in line[:-1]] + [10]))
width = len(board[0])
board = [[10] * width] + board + [[10] * width]

low_points = find_low_points(board)
risk_levels = count_risk_levels(board, low_points)

sum = 0
for rl in risk_levels:
    sum += rl
print(sum)


def measure_basin(board, low_point):
    def basin(row, column, value):
        if value == 9 or value == 10:
            return 0

        board[row][column] = 10

        size = 1
        top = board[row - 1][column]
        if value < top:
            size += basin(row - 1, column, top)

        right = board[row][column + 1]
        if value < right:
            size += basin(row, column + 1, right)

        down = board[row + 1][column]
        if value < down:
            size += basin(row + 1, column, down)

        left = board[row][column - 1]
        if value < left:
            size += basin(row, column - 1, left)

        return size

    r, c = low_point
    return basin(r, c, board[r][c])


# part2
print('----------------')

sum = 0
basin_sizes = sorted([measure_basin(board, lp) for lp in low_points])
print(basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3])
