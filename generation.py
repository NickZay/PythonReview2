from texteditor import TextImprover
import random
import pickle


def choose_and_add_word(data, previous_tokens, main_result, result, editor, verbosity):
    rand = random.random()
    sum_of_prob = 0.0
    for word, prob in data[len(previous_tokens) + 1][tuple(previous_tokens)].items():
        sum_of_prob += prob
        if sum_of_prob > rand:
            previous_tokens.append(word)
            if verbosity == 1:
                result.append(word)
            word = editor(word)
            main_result.append(word)
            break


def cut_previous_tokens(data, previous_tokens, depth):
    while previous_tokens and (len(previous_tokens) >= depth - 1) or \
            (not (tuple(previous_tokens) in data[len(previous_tokens) + 1])):
        previous_tokens = previous_tokens[1:]
    return previous_tokens


def generate(depth=3, count=50, verbosity=0, probabilities_file='probabilities.txt'):
    with open(probabilities_file, "rb") as read_file:
        data = pickle.load(read_file)
    assert data[0] >= depth, f'You only have {data[0]} depth'

    previous_tokens = []
    main_result = []
    result = []
    answer = []
    editor = TextImprover(count)

    for _ in range(count):
        previous_tokens = cut_previous_tokens(data, previous_tokens, depth)
        choose_and_add_word(data, previous_tokens, main_result, result, editor, verbosity)

    if verbosity == 1:
        answer.append("Smoker's text:\n")
        answer.append(' '.join(word for word in result if word))
        answer.append("\n\nHealthy person's text:\n")

    answer.append(' '.join(word for word in main_result if word))
    return answer

