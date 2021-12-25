import utils

chunk_openings = {'[', '<', '{', '('}
chunk_closings = {'[': ']', '<': '>', '{': '}', '(': ')'}
syntax_error_scores = {']': 57, '>': 25137, '}': 1197, ')': 3}
closings_scores = {']': 2, '>': 4, '}': 3, ')': 1}


def validate_line(line):
    line_stack = []
    for elt in line:
        if elt in chunk_openings:
            line_stack.append(elt)
        elif chunk_closings.get(line_stack.pop()) != elt:
            return elt
    return line_stack


def close_openings(unclosed_openings):
    line_completions = []
    while len(unclosed_openings) != 0:
        closing = chunk_closings.get(unclosed_openings.pop())
        line_completions.append(closing)
    return line_completions


def score_closings(closings):
    score = 0
    for c in closings:
        score = score * 5 + closings_scores.get(c)
    return score


lines = list(utils.parse_and_map('i1', lambda line: line[:-1]))

score_sum = 0
unclosed_openings = []
for line in lines:
    validation_output = validate_line(line)
    if not isinstance(validation_output, list):
        score_sum += syntax_error_scores.get(validation_output)
    else:
        unclosed_openings.append(validation_output)

print(score_sum)

# part2
print('---------------')


def median(sorted_list):
    n = len(sorted_list)
    if n % 2 == 0:
        middle = n // 2
        return (sorted_list[middle - 1] + sorted_list[middle]) / 2
    else:
        return sorted_list[n // 2]


sorted_scored_closings = sorted(map(score_closings, map(close_openings, unclosed_openings)))
print(median(sorted_scored_closings))
