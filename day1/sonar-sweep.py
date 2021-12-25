import utils


def count_depth_increase(depths):
    depth_increase = 0
    for (previous_depth, next_depth) in zip(depths[:-1], depths[1:]):
        if previous_depth < next_depth:
            depth_increase += 1
    return depth_increase


depths = list(utils.parse_and_map('i1', lambda x: int(x)))
print(count_depth_increase(depths))

# p2
depth_windows = []
for i in range(0, (len(depths) - 2)):
    window = depths[i] + depths[i + 1] + depths[i + 2]
    depth_windows.append(window)

# print(depth_windows)
print(count_depth_increase(depth_windows))
