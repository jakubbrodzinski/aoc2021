import utils

DAYS = 256


def simulate(fishes):
    saved_results = {}

    def simulate_single_fish(fish, days):
        if (fish, days) in saved_results:
            return saved_results[(fish, days)]

        output = 1

        if fish < days:
            output += 1
            child_days_remaining = days - fish - 1
            while child_days_remaining >= 7:
                output += simulate_single_fish(8, child_days_remaining)
                child_days_remaining -= 7
            saved_results[(fish, days)] = output

        return output

    fish_count = 0
    for f in fishes:
        fish_count += simulate_single_fish(f, DAYS)

    return fish_count


fishes = list(utils.parse_and_map('i1',
                                  lambda line: list(map(lambda n: int(n), line.split(',')))
                                  ))[0]

print(simulate(fishes))
# print(len(simulate(fishes)))
