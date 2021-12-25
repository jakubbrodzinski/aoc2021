import utils

board = [[-1] * 12] + list(utils.parse_and_map('i1', lambda l: [-1] + [int(oct) for oct in l[:-1]] + [-1])) + [
    [-1] * 12]
flashes = [[False for i in range(0, 12)] for j in range(0, 12)]


def start_round():
    for r in range(1, 11):
        for c in range(1, 11):
            board[r][c] += 1


def simulate():
    changed = True
    while changed:
        changed = False
        for r in range(1, 11):
            for c in range(1, 11):
                if board[r][c] > 9 and not flashes[r][c]:
                    board[r - 1][c - 1] += 1
                    board[r - 1][c] += 1
                    board[r - 1][c + 1] += 1
                    board[r][c - 1] += 1
                    board[r][c + 1] += 1
                    board[r + 1][c - 1] += 1
                    board[r + 1][c] += 1
                    board[r + 1][c + 1] += 1
                    changed = True
                    flashes[r][c] = True


def reset_and_count_flashes():
    flash_counter = 0
    for r in range(1, 11):
        for c in range(1, 11):
            if board[r][c] > 9:
                board[r][c] = 0
                flashes[r][c] = False
                flash_counter += 1
    return flash_counter


def print_board():
    for r in range(1, 11):
        for c in range(1, 11):
            print(board[r][c], end='')
        print()
    print()


def simulate_for_rounds(rounds):
    sum = 0
    for i in range(0, rounds):
        start_round()
        simulate()
        sum += reset_and_count_flashes()
        # print_board()
        # print("Round " + str(i+1) + ": " + str(f_c))

    return sum


def reset_and_check_sync():
    sync = True
    for r in range(1, 11):
        for c in range(1, 11):
            if board[r][c] > 9:
                board[r][c] = 0
                flashes[r][c] = False
            else:
                sync = False
    return sync


def simulate_until_sync():
    def simulate_round():
        start_round()
        simulate()
        return reset_and_check_sync()

    rounds = 0
    while not simulate_round():
        rounds += 1
    return rounds + 1


# print(simulate_for_rounds(100))

# part2
print('---------')

print(simulate_until_sync())
