import heapq
import math

import utils


def dijkstra(graph):
    height, width = len(graph), len(graph[0])
    dist = [[math.inf] * len(row) for row in graph]
    dist[0][0] = 0
    pqueue = []
    heapq.heappush(pqueue, (0, 0, 0))
    while len(pqueue) != 0:
        cost, x, y = heapq.heappop(pqueue)
        cost = dist[y][x]
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue
            alt = cost + graph[ny][nx]
            if alt < dist[ny][nx]:
                dist[ny][nx] = alt
                heapq.heappush(pqueue, (alt, nx, ny))
    return dist[-1][-1]


def parse_expanded_board(path):
    with open(path) as reader:
        lines = reader.readlines()
        return [
            [(int(v) + x + y - 1) % 9 + 1 for x in range(5) for v in line[:-1]]
            for y in range(5)
            for line in lines
        ]


board = list(utils.parse_and_map('i1', mapper=lambda l: [int(i) for i in l.strip()]))
print(dijkstra(board))
# part2
print('--------')

board = parse_expanded_board('i1')
print(dijkstra(board))
