import string


def make_dict_of_signs():
    result = dict()
    for open_sign, close_sign in zip(TextImprover.OPEN_SIGNS, TextImprover.CLOSE_SIGNS):
        result[open_sign] = close_sign
        result[close_sign] = open_sign
    return result


def remove_bad_signs(word):
    word = word.replace('—', '-')
    word = word.replace("_", "")
    return word


def make_capital(word):
    index = 0
    for index, letter in enumerate(word):
        if letter in string.ascii_letters or letter in TextImprover.RUSSIAN:
            break
    word = word[:index] + word[index].capitalize() + word[index + 1:]
    return word


def end_on_bad(word):
    bad = ["’s", "’t", "’ve", "’re", "’m", "’d"]
    is_word_bad = False
    for item in bad:
        if word.endswith(item):
            is_word_bad = True
    return is_word_bad


def add_one_more_point(word):
    k = -1
    while k > -len(word) and word[k] not in string.ascii_letters and \
            word[k] not in TextImprover.RUSSIAN:
        k -= 1
    else:
        if k != -1:
            word = word[:k + 1] + '.'
        else:
            word += '.'
    return word


class TextImprover:
    OPEN_SIGNS = ('(', '[', '{', '“', '"', '«', '‘', '')
    CLOSE_SIGNS = (')', ']', '}', '”', '"', '»', '’', '')
    PUNCTUATION_SIGNS = ('.', '?', '!')
    RUSSIAN = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"

    def __init__(self, number_of_words):
        self.has_quote = False
        self.counter = 0
        self.num_of_words = number_of_words
        self.is_start_sentence = True
        self.what_quote = 0
        self.last_dot = False
        self.last_comma = False
        self.stack_of_signs = []
        self.pairs_of_signs = make_dict_of_signs()

    def fflush(self, new_word, symbol=''):
        opposite_symbol = self.pairs_of_signs[symbol]
        if symbol == '' or opposite_symbol in self.stack_of_signs:
            while self.stack_of_signs and opposite_symbol != self.stack_of_signs[-1]:
                new_word += self.pairs_of_signs[self.stack_of_signs[-1]]
                self.stack_of_signs.pop(-1)
            else:
                if symbol != '' and self.stack_of_signs:
                    self.stack_of_signs.pop(-1)
                    new_word += symbol
        return new_word

    def change_stack(self, word):
        new_word = ''
        is_it_end = False
        for letter in word:
            if letter in string.ascii_letters or letter in TextImprover.RUSSIAN:
                is_it_end = True
            if letter in TextImprover.OPEN_SIGNS and not (letter == '"' and letter in self.stack_of_signs):
                if not is_it_end:
                    self.stack_of_signs.append(letter)
                    new_word += letter
            elif letter in TextImprover.PUNCTUATION_SIGNS:
                new_word += letter
                if '...' not in word and 'www' not in word:
                    new_word = self.fflush(new_word)
                self.is_start_sentence = True
            elif letter in TextImprover.CLOSE_SIGNS and \
                    not (letter == '’' and end_on_bad(word)):
                if is_it_end:
                    new_word = self.fflush(new_word, letter)
            else:
                new_word += letter
        return new_word

    def remove_double_dots_and_commas(self, word):
        new_word = ''
        for i in range(len(word)):
            need_to_add = True
            if word[i] == ',':
                if self.last_comma or self.last_dot:
                    need_to_add = False
                else:
                    self.last_comma = True
                    self.last_dot = False
            else:
                self.last_comma = False

            if word[i] == '.' and '...' not in word:
                if self.last_dot or self.last_comma:
                    need_to_add = False
                else:
                    self.last_dot = True
            else:
                self.last_dot = False

            if need_to_add:
                new_word += word[i]

        return new_word

    def __call__(self, word):
        assert type(word) == str, 'Something went wrong'
        self.counter += 1

        if self.is_start_sentence:
            interesting_words = ('screamed', 'said', 'cried', 'muttered')
            if word not in interesting_words:
                word = make_capital(word)
            self.is_start_sentence = False

        word = remove_bad_signs(word)

        if self.counter == self.num_of_words:
            word = add_one_more_point(word)

        word = self.change_stack(word)
        word = self.remove_double_dots_and_commas(word)
        return word
