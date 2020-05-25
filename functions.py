from texteditor import text_improver
import random
import pickle
from flask import Flask, request
from collections import defaultdict
import pickle
import string


app = Flask(__name__)
app.config["DEBUG"] = True


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


def generate(depth=3, count=50, verbosity=0, output_file=None, probabilities_file='probabilities.txt'):
    with open(probabilities_file, "rb") as read_file:
        data = pickle.load(read_file)
    assert data[0] >= depth, f'You only have {data[0]} depth'

    previous_tokens = []
    main_result = []
    result = []
    answer = []
    editor = text_improver(count)

    for _ in range(count):
        previous_tokens = cut_previous_tokens(data, previous_tokens, depth)
        choose_and_add_word(data, previous_tokens, main_result, result, editor, verbosity)

    if verbosity == 1:
        answer.append("Текст курильщика:\n")
        answer.append(' '.join(word for word in result if word))
        answer.append("\n\nТекст здорового человека:\n")

    answer.append(' '.join(word for word in main_result if word))
    return answer


def get_material(filename, encoding=None):
    words = []
    with open(filename, 'r', encoding=encoding) as book:
        for line in book:
            words += line.split()
    return words


def return_emptiness():
    return defaultdict(int)


def calculate(input_file, depth=3, probabilities_file='probabilities.txt'):
    try:
        words = get_material(input_file, 'utf-8')
    except Exception:
        words = get_material(input_file)

    probabilities = [depth]

    for index in range(depth):
        result = defaultdict(return_emptiness)
        for i in range(index, len(words)):
            if words[i] not in string.punctuation:
                result[tuple(words[i - index: i])][words[i]] += 1
        for substring in result.keys():
            amount = sum(result[substring].values())
            for new_word in result[substring].keys():
                result[substring][new_word] /= amount
        probabilities.append(result)

    with open(probabilities_file, "wb") as write_file:
        pickle.dump(probabilities, write_file)
