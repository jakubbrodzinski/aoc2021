EAST = '>'
SOUTH = 'v'
EMPTY = '.'


def load(path):
    with open(path) as reader:
        return list(map(lambda row: [c for c in row], reader.read().split('\n')))


def move_east(row):
    add_to_left_edge = row[-1] == EAST and row[0] == EMPTY
    east_move = False
    ic = 0
    while ic < len(row) - 1:
        if row[ic] == EAST and row[ic + 1] == EMPTY:
            row[ic + 1] = EAST
            row[ic] = EMPTY
            east_move = True
            ic += 2
        else:
            ic += 1

    if add_to_left_edge:
        row[-1] = EMPTY
        row[0] = EAST
        east_move = True

    return east_move, row


assert move_east(['>', '.'])[1] == ['.', '>']
assert move_east(['.', '>'])[1] == ['>', '.']
assert move_east(['>', '>', '.'])[1] == ['>', '.', '>']
assert move_east(['>', '.', '>'])[1] == ['.', '>', '>']
assert move_east(['v', '.', '>'])[1] == ['v', '.', '>']
assert move_east(['.', 'v', '>'])[1] == ['>', 'v', '.']
assert move_east(['>', '.', '.'])[1] == ['.', '>', '.']


def move_south(board, ic):
    add_to_top_edge = board[-1][ic] == SOUTH and board[0][ic] == EMPTY
    south_move = False
    ir = 0
    while ir < len(board) - 1:
        if board[ir][ic] == SOUTH and board[ir + 1][ic] == EMPTY:
            board[ir + 1][ic] = SOUTH
            board[ir][ic] = EMPTY
            south_move = True
            ir += 2
        else:
            ir += 1

    if add_to_top_edge:
        board[-1][ic] = EMPTY
        board[0][ic] = SOUTH
        south_move = True

    return south_move, board


assert move_south([['v', '.'], ['.', '.']], 0)[1] == [['.', '.'], ['v', '.']]
assert move_south([['v', '.'], ['.', 'v']], 1)[1] == [['v', 'v'], ['.', '.']]
assert move_south([['v', '>'], ['.', 'v']], 1)[1] == [['v', '>'], ['.', 'v']]
assert move_south([['v', '.'], ['.', 'v'], ['.', 'v']], 1)[1] == [['v', 'v'], ['.', 'v'], ['.', '.']]
assert move_south([['v', 'v'], ['.', 'v'], ['.', '.']], 1)[1] == [['v', 'v'], ['.', '.'], ['.', 'v']]
assert move_south([['v', 'v'], ['.', '>'], ['v', 'v']], 0)[1] == [['.', 'v'], ['v', '>'], ['v', 'v']]
assert move_south([['v', 'v'], ['.', '>'], ['.', 'v']], 0)[1] == [['.', 'v'], ['v', '>'], ['.', 'v']]


def print_board(board):
    print('\n'.join([''.join(row) for row in board]))


def count_turns(board):
    def do_turn(board):
        move_occured = False
        for row in board:
            if move_east(row)[0]:
                move_occured = True
        for ic in range(0, len(board[0])):
            if move_south(board, ic)[0]:
                move_occured = True

        return move_occured

    turns = 0
    # print_board(board)
    while do_turn(board):
        turns += 1
        # print('turn:', turns)
        # print_board(board)
        # print('-------------')
    return turns + 1

assert len(load('t1')) == 9
assert count_turns(load('t1')) == 58

print(count_turns(load('i1')))
