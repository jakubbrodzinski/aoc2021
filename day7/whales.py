import utils

ps = list(utils.parse_and_map('i1',
                              lambda line: list(map(lambda n: int(n), line.split(',')))
                              )
          )[0]


def median(ps):
    ps.sort()
    n = len(ps)
    if n % 2 == 0:
        middle = n // 2
        return (ps[middle - 1] + ps[middle]) / 2
    else:
        return ps[n // 2]


med = median(ps)
distance_sum = 0
for p in ps:
    distance_sum += abs(p - med)
print(distance_sum)

# part2
print('--------------------')

def ps_to_freq_dict(ps):
    ps_with_freq = {}
    for p in ps:
        ps_with_freq[p] = ps_with_freq.get(p, 0) + 1
    ps_with_freq = list(ps_with_freq.items())
    return ps_with_freq


def calculate_costs_for_distances(ps):
    fuel_costs = [0]
    min_distance = ps[-1] - ps[0] + 1
    for cost in range(1, min_distance):
        fuel_costs.append(fuel_costs[cost - 1] + cost)
    return fuel_costs

def count_fuel_cost(ps_with_freq,cost_dict, alignment):
    cost = 0
    for p,freq in ps_with_freq:
        cost += cost_dict[abs(p-alignment)]*freq
    return cost

ps.sort()
ps_with_freq = ps_to_freq_dict(ps)
cost_dict = calculate_costs_for_distances(ps)

min_cost = count_fuel_cost(ps_with_freq,cost_dict,ps[0])
for align in range(ps[1],ps[-1]):
    temp = count_fuel_cost(ps_with_freq,cost_dict,align)
    if temp < min_cost:
        min_cost = temp
    else:
        break
print(min_cost)

