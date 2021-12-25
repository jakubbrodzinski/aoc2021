import utils


def parse_input(file):
    dots = set()
    lines = utils.read_lines(file)
    i = 0
    while i < len(lines):
        if lines[i] == '\n':
            break

        x, y = lines[i][:-1].split(',')
        dots.add((int(x), int(y)))
        i += 1

    i += 1

    folds = []
    while i < len(lines):
        f = lines[i].split('=')
        folds.append((f[0][-1], int(f[1])))
        i += 1

    return dots, folds


def x_fold(dots, fx):
    def page_width():
        max_x = 0
        for x, _ in dots:
            max_x = max(max_x, x)
        return max_x

    folded = set()
    diff = max(0, page_width() - 2 * fx)
    for x, y in dots:
        if x < fx:
            folded.add((x + diff, y))
        else:
            folded_x = fx - (x - fx)
            folded.add((folded_x, y))

    return folded


def y_fold(dots, fy):
    def page_height():
        max_y = 0
        for _, y in dots:
            max_y = max(max_y, y)
        return max_y

    folded = set()
    diff = max(0, page_height() - 2 * fy)
    for x, y in dots:
        if y < fy:
            folded.add((x, y + diff))
        else:
            folded_y = fy - (y - fy)
            folded.add((x, folded_y))

    return folded


dots, folds = parse_input('i1')

if folds[0][0] == 'x':
    print(len(x_fold(dots,folds[0][1])))
else:
    print(len(y_fold(dots, folds[0][1])))
#-----
print('part2')

def print_dots(dots):
    def page_sizes():
        max_x, max_y = 0, 0
        for x, y in dots:
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return max_x+1, max_y+1

    width, height = page_sizes()
    board = []
    for i in range(0,height):
        board.append([0]*width)
    for x, y in dots:
        board[y][x] = 1
    for row in board:
        for cell in row:
            if cell == 0 :
                print('.', end='')
            else:
                print('#', end='')
        print()

for fold in folds:
    if fold[0] == 'x':
        dots = x_fold(dots, fold[1])
    else:
        dots = y_fold(dots, fold[1])

print_dots(dots)