import json

import utils


def nested_number(num):
    return isinstance(num, list)


def literal(num):
    return isinstance(num, int)


class ExplosionReducer:
    def __init__(self, num: list):
        self.num = num
        self.exploded = False
        self.add_to_left, self.add_to_right = False, False
        self.exploded_num = [None, None]

    def add(self, num2):
        self.num = [self.num, num2]

    def reduce(self):
        def add_to_left(num):
            if not self.add_to_left:
                return num

            if literal(num):
                self.add_to_left = False
                return num + self.exploded_num[0]

            if nested_number(num[1]):
                num[1] = add_to_left(num[1])
            else:
                self.add_to_left = False
                return [num[0], num[1] + self.exploded_num[0]]

            if nested_number(num[0]):
                num[0] = add_to_left(num[0])
            elif self.add_to_left:
                self.add_to_left = False
                return [num[0] + self.exploded_num[0], num[1]]

            return num

        def add_to_right(num):
            if not self.add_to_right:
                return num

            if literal(num):
                self.add_to_right = False
                return num + self.exploded_num[1]

            if nested_number(num[0]):
                num[0] = add_to_right(num[0])
            else:
                self.add_to_right = False
                return [num[0] + self.exploded_num[1], num[1]]

            if nested_number(num[1]):
                num[1] = add_to_right(num[1])
            elif self.add_to_right:
                self.add_to_right = False
                return [num[0], num[1] + self.exploded_num[1]]

            return num

        def explode(num):
            self.exploded = True
            self.exploded_num = [num[0], num[1]]
            self.add_to_left, self.add_to_right = True, True

        def should_explode(num, depth):
            return type(num[0]) == int and type(num[1]) == int and depth >= 4

        def explore_and_explode(num, depth):
            if nested_number(num[0]):
                if should_explode(num[0], depth + 1):
                    explode(num[0])
                    num[0] = 0
                else:
                    explore_and_explode(num[0], depth + 1)

            if self.exploded:
                num[1] = add_to_right(num[1])
            elif nested_number(num[1]):
                if should_explode(num[1], depth + 1):
                    explode(num[1])
                    num[1] = 0
                else:
                    explore_and_explode(num[1], depth + 1)
                if self.exploded:
                    num[0] = add_to_left(num[0])

        explore_and_explode(self.num, 0)
        return self.exploded, self.num


class SplitReducer:
    def __init__(self, num: list):
        self.num = num
        self.splitted = False

    def reduce(self):
        def split_literal(literal):
            return [literal // 2, (literal + 1) // 2]

        def explore_and_split(num):
            if self.splitted:
                return

            if nested_number(num[0]):
                explore_and_split(num[0])
            elif num[0] >= 10:
                self.splitted = True
                num[0] = split_literal(num[0])

            if nested_number(num[1]):
                explore_and_split(num[1])
            elif num[1] >= 10 and not self.splitted:
                self.splitted = True
                num[1] = split_literal(num[1])

        explore_and_split(self.num)
        return self.splitted, self.num


class Reducer:
    def __init__(self, num: list):
        self.num = num

    def __init__(self, num1: list, num2: list):
        self.num = [num1, num2]

    def reduce(self):
        should_reduce = True
        while should_reduce:
            exploded, self.num = ExplosionReducer(self.num).reduce()
            should_reduce = exploded

            if not exploded:
                splited, self.num = SplitReducer(self.num).reduce()
                should_reduce = splited

        return self.num


def magnitude(num: list):
    if literal(num):
        return num
    else:
        return 3 * magnitude(num[0]) + 2 * magnitude(num[1])


def explosion_assert():
    assert ExplosionReducer([[[[[9, 8], 1], 2], 3], 4]).reduce() == (True, [[[[0, 9], 2], 3], 4])
    assert ExplosionReducer([[[[[9, 8], 1], 2], 3], 4]).reduce() == (True, [[[[0, 9], 2], 3], 4])
    assert ExplosionReducer([7, [6, [5, [4, [3, 2]]]]]).reduce() == (True, [7, [6, [5, [7, 0]]]])
    assert ExplosionReducer([[6, [5, [4, [3, 2]]]], 1]).reduce() == (True, [[6, [5, [7, 0]]], 3])
    assert ExplosionReducer([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]).reduce() == (True, [[3, [2, [8, 0]]],
                                                                                                [9, [5, [4, [3, 2]]]]])
    assert ExplosionReducer([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]).reduce() == (
        True, [[3, [2, [8, 0]]], [9, [5, [7, 0]]]])
    assert ExplosionReducer([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]).reduce() == (True, [
        [[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]])
    assert ExplosionReducer([[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]).reduce() == (True, [[[[0, 7], 4], [15, [0, 13]]],
                                                                                           [1, 1]])
    assert ExplosionReducer([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]).reduce() == (True, [
        [[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])


def split_assert():
    assert SplitReducer([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]).reduce() == (
        True, [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]])
    assert SplitReducer([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]).reduce() == (
        True, [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]],
               [1, 1]])


def reducer_assert():
    assert Reducer([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]).reduce() == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    assert Reducer([[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
                   [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]).reduce() == [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]],
                                                                           [[8, [7, 7]], [[7, 9], [5, 0]]]]
    assert Reducer([[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]],
                   [[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]]).reduce() == [
               [[[6, 7], [6, 7]], [[7, 7], [0, 7]]],
               [[[8, 7], [7, 7]], [[8, 8], [8, 0]]]]
    assert Reducer([[[[6, 7], [6, 7]], [[7, 7], [0, 7]]], [[[8, 7], [7, 7]], [[8, 8], [8, 0]]]],
                   [[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]]).reduce() == [
               [[[7, 0], [7, 7]], [[7, 7], [7, 8]]], [[[7, 7], [8, 8]], [[7, 7], [8, 7]]]]
    assert Reducer([[[[7, 0], [7, 7]], [[7, 7], [7, 8]]], [[[7, 7], [8, 8]], [[7, 7], [8, 7]]]],
                   [7, [5, [[3, 8], [1, 4]]]]).reduce() == [[[[7, 7], [7, 8]], [[9, 5], [8, 7]]],
                                                            [[[6, 8], [0, 8]], [[9, 9], [9, 0]]]]
    assert Reducer([[[[7, 7], [7, 8]], [[9, 5], [8, 7]]], [[[6, 8], [0, 8]], [[9, 9], [9, 0]]]],
                   [[2, [2, 2]], [8, [8, 1]]]).reduce() == [[[[6, 6], [6, 6]], [[6, 0], [6, 7]]],
                                                            [[[7, 7], [8, 9]], [8, [8, 1]]]]
    assert Reducer([[[[6, 6], [6, 6]], [[6, 0], [6, 7]]], [[[7, 7], [8, 9]], [8, [8, 1]]]], [2, 9]).reduce() == [
        [[[6, 6], [7, 7]], [[0, 7], [7, 7]]], [[[5, 5], [5, 6]], 9]]
    assert Reducer([[[[6, 6], [7, 7]], [[0, 7], [7, 7]]], [[[5, 5], [5, 6]], 9]],
                   [1, [[[9, 3], 9], [[9, 0], [0, 7]]]]).reduce() == [[[[7, 8], [6, 7]], [[6, 8], [0, 8]]],
                                                                      [[[7, 7], [5, 0]], [[5, 5], [5, 6]]]]
    assert Reducer([[[[7, 8], [6, 7]], [[6, 8], [0, 8]]], [[[7, 7], [5, 0]], [[5, 5], [5, 6]]]],
                   [[[5, [7, 4]], 7], 1]).reduce() == [[[[7, 7], [7, 7]], [[8, 7], [8, 7]]], [[[7, 0], [7, 7]], 9]]
    assert Reducer([[[[7, 7], [7, 7]], [[8, 7], [8, 7]]], [[[7, 0], [7, 7]], 9]],
                   [[[[4, 2], 2], 6], [8, 7]]).reduce() == [
               [[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]


def magnitude_assert():
    assert magnitude([[1, 2], [[3, 4], 5]]) == 143
    assert magnitude([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]) == 1384
    assert magnitude([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]) == 445
    assert magnitude([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]) == 791
    assert magnitude([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]) == 1137
    assert magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]) == 3488


def test_file_assert(file_name, sum, magn):
    numbers = list(utils.parse_and_map(file_name, json.loads))
    acc = numbers[0]
    for i in range(1, len(numbers)):
        acc = Reducer(acc, numbers[i]).reduce()
    assert acc == sum
    assert magnitude(acc) == magn


explosion_assert()
split_assert()
magnitude_assert()
test_file_assert('t1', [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]], 3488)
test_file_assert('t2', [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]], 4140)

numbers = list(utils.parse_and_map('i1', json.loads))
acc = numbers[0]
for i in range(1, len(numbers)):
    acc = Reducer(acc, numbers[i]).reduce()
print(magnitude(acc))


def max_sum(numbers):
    sums = [Reducer(json.loads(n1), json.loads(n2)).reduce() for n1 in numbers for n2 in numbers if n1 != n2]
    return max([(s, magnitude(s)) for s in sums], key=lambda s: s[1])


numbers = list(utils.read_lines('t2'))
assert max_sum(numbers) == ([[[[7, 8], [6, 6]], [[6, 0], [7, 7]]], [[[7, 8], [8, 8]], [[7, 9], [0, 6]]]], 3993)

numbers = list(utils.read_lines('i1'))
print(max_sum(numbers)[1])