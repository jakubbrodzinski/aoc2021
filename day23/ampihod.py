import heapq

HALLWAY_SIZE = 11

COSTS = {0: 1, 1: 10, 2: 100, 3: 1000}


def treplace(t, i, e):
    return t[:i] + (e,) + t[i + 1:]



# room numbers: 2,4,6,8
def possible_hallways_moves(hallway, room_index):
    jd = [True] * HALLWAY_SIZE
    for i in range(room_index - 1, -1, -1):
        jd[i] = jd[i + 1] and hallway[i] == -1

    for i in range(room_index + 1, HALLWAY_SIZE):
        jd[i] = jd[i - 1] and hallway[i] == -1
    jd[2] = False
    jd[4] = False
    jd[6] = False
    jd[8] = False
    return jd


def possible_room_moves(hallway, room_index, elt):
    room_moves = []
    for i in range(room_index, -1, -1):
        if hallway[i] != -1:
            if hallway[i] == elt:
                room_moves.append(i)
            break
    for i in range(room_index + 1, HALLWAY_SIZE):
        if hallway[i] != -1:
            if hallway[i] == elt:
                room_moves.append(i)
            break
    return room_moves


def get_all_possible_moves(rooms, hallway):
    def find_top(room_number):
        for i, r in enumerate(rooms):
            if r[room_number] != -1:
                return i

    moves = []

    def into_hallway_moves():
        def is_valid_room(room_number):
            for r in rooms:
                if r[room_number] != -1 and r[room_number] != room_number:
                    return False
            return True

        for room_number in range(0, 4):
            if is_valid_room(room_number):
                continue

            top = find_top(room_number)
            if top is None:
                continue

            top_elt = rooms[top][room_number]
            room_index = 2 + 2 * room_number
            for ihn, hn in enumerate(possible_hallways_moves(hallway, room_index)):
                if hn:
                    nrs = treplace(rooms, top, treplace(rooms[top], room_number, -1))
                    nhs = treplace(hallway, ihn, top_elt)
                    nc = (abs(room_index - ihn) + top + 1) * COSTS[top_elt]
                    moves.append((nc, nrs, nhs))

    def get_valid_rooms():
        valid_rooms = [None] * 4
        for ir, r in enumerate(rooms):
            for i in range(0, 4):
                if r[i] == -1:
                    valid_rooms[i] = ir
                elif r[i] != i:
                    valid_rooms[i] = None
        return valid_rooms

    def into_room_moves():
        for room_number, room_top in enumerate(get_valid_rooms()):
            if room_top is not None:
                room_index = 2 + 2 * room_number
                for ih in possible_room_moves(hallway, room_index, room_number):
                    nrs = treplace(rooms, room_top, treplace(rooms[room_top], room_number, room_number))
                    nhs = treplace(hallway, ih, -1)
                    nc = (abs(room_index - ih) + room_top + 1) * COSTS[room_number]
                    moves.append((nc, nrs, nhs))

    into_hallway_moves()
    into_room_moves()

    return moves


def dijkstra(rooms, hallway, end):
    priorities = {(rooms, hallway): 0}
    queue = []
    heapq.heappush(queue, (0, rooms, hallway))
    while len(queue) != 0:
        cost, crooms, challway = heapq.heappop(queue)
        cost = priorities[crooms, challway]

        if crooms == end:
            break

        for nc, nr, nh in get_all_possible_moves(crooms, challway):
            alt = cost + nc
            if (nr, nh) not in priorities or alt < priorities[nr, nh]:
                priorities[nr, nh] = alt
                heapq.heappush(queue, (alt, nr, nh))

    return priorities[end, hallway]


assert possible_hallways_moves([-1, 'A', -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 2) == [False,
                                                                                         False,
                                                                                         False,
                                                                                         True,
                                                                                         False,
                                                                                         True,
                                                                                         False,
                                                                                         True,
                                                                                         False,
                                                                                         True,
                                                                                         True]
assert possible_hallways_moves([-1, 'A', -1, 'B', -1, -1, -1, -1, -1, -1, -1, -1], 2) == [False,
                                                                                          False,
                                                                                          False,
                                                                                          False,
                                                                                          False,
                                                                                          False,
                                                                                          False,
                                                                                          False,
                                                                                          False,
                                                                                          False,
                                                                                          False]
assert possible_hallways_moves([-1, 'A', -1, -1, -1, -1, -1, 'B', -1, -1, -1, -1], 4) == [False,
                                                                                          False,
                                                                                          False,
                                                                                          True,
                                                                                          False,
                                                                                          True,
                                                                                          False,
                                                                                          False,
                                                                                          False,
                                                                                          False,
                                                                                          False]

ROOM_HEIGHT = 2
END = ((0, 1, 2, 3), (0, 1, 2, 3))
END2 = ((0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
INIT_HALLWAY = tuple([-1] * HALLWAY_SIZE)

assert dijkstra(((1, 2, 1, 3), (0, 3, 2, 0)), INIT_HALLWAY, END) == 12521
assert dijkstra(((1, 2, 1, 3), (3, 2, 1, 0), (3, 1, 0, 2), (0, 3, 2, 0)), INIT_HALLWAY, END2) == 44169

print(dijkstra(((1, 2, 0, 3), (1, 2, 3, 0)), INIT_HALLWAY, END))
print(dijkstra(((1, 2, 0, 3), (3, 2, 1, 0), (3, 1, 0, 2), (1, 2, 3, 0)), INIT_HALLWAY, END2))
