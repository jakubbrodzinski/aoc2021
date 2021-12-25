import utils


def parse_graph(lines):
    graph = {}
    for l in lines:
        v1, v2 = l[:-1].split('-')
        if v1 not in graph:
            graph[v1] = set()
        if v2 not in graph:
            graph[v2] = set()
        graph.get(v1).add(v2)
        graph.get(v2).add(v1)

    return graph


def dfs(graph):
    paths = []

    def dfs(path, explored, v):
        if v == 'end':
            paths.append(path.copy())
        else:
            if v.islower():
                explored.add(v)
            for e in graph[v]:
                if e not in explored:
                    path.append(e)
                    dfs(path, explored, e)
                    path.pop()
            explored.discard(v)

    dfs(['start'], set(), 'start')
    return len(paths)


graph = parse_graph(utils.read_lines('i1'))
print(dfs(graph))

# part2
print('--------')


def dfs2(graph):
    paths = []

    def dfs(path, explored, v, second_small_cave):
        if v == 'end':
            # print('!\t', path)
            paths.append(path.copy())
        else:
            if v.islower():
                explored.add(v)
            for e in graph[v]:
                if e not in explored:
                    path.append(e)
                    dfs(path, explored, e, second_small_cave)
                    path.pop()
                elif not second_small_cave and e != 'start':
                    path.append(e)
                    dfs(path, explored, e, e)
                    path.pop()
            if second_small_cave != v:
                explored.discard(v)

    dfs(['start'], set(), 'start', None)

    return len(paths)


print(dfs2(graph))
