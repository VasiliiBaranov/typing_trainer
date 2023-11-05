import random
from english_words import english_words_set

list_of_words = list(english_words_set)

# list_of_words = ['мама', 'папа']
length_of_dict = len(list_of_words)
lst_of_words = []

for i in list_of_words:
    lst_of_words.append(i.lower())

cap_list_w = []
for i in list_of_words:
    cap_list_w.append(i.capitalize())
    cap_list_w.append(i)
'''
object with generated text
'''


class Text(object):

    def __init__(self, min_length, max_length, capital_e, digits_e, other_e):
        self.length = random.randint(min_length, max_length)
        self.data = []

        self._digits_col = 0
        self._other_col = 0
        self.number_of_symbols = 0

        if digits_e:
            self._digits_col = random.randint(1, int(self.length / 10 + 10))

        if other_e:
            self._other_col = random.randint(0, int(self.length / 15))

        # add words in list
        self.tmp_list = lst_of_words
        if capital_e:
            self.tmp_list = cap_list_w

        if self._digits_col:
            for _ in range(self._digits_col):
                self.data.append(str(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])))

        if self._other_col:
            for _ in range(self._other_col):
                self.data.append(random.choice(
                    ["!", "@", "#", "$", "%", "^", "*", "(", ")", "_", "+", "{", "}", "[", "]", ":", "\"", ";", "'",
                     "<",
                     ">", ",", ".", ">", "?"]))

        for _ in range(self.length - self._digits_col - self._other_col):
            self.data.append(random.choice(self.tmp_list))

        # Make string from data
        random.shuffle(self.data)
        self.string = " ".join(self.data)
        self.number_of_symbols = len(self.string)

    def __str__(self):
        return self.string

    def __len__(self):
        return self.length

# t = Text(3, 15, False, False, False)
# print(t)
# print(t.number_of_symbols)
