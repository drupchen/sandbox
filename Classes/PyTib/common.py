# coding: utf-8

from bisect import bisect_left
from collections import OrderedDict, Callable


def write_file(file_path, content):
    with open(file_path, 'w', -1, 'utf8') as f:
        f.write(content)


def open_file(file_path):
    with open(file_path, 'r', -1, 'utf8') as f:
        return f.read()


def search(l, entry, len_l):
    """
    :param l: list on which to apply bisect
    :param entry: element of this list to find
    :param len_l: lenght of list (needed to return a correct index)
    :return: True or False
    """
    index = bisect_left(l, entry, 0, len_l)
    if index != len_l and l[index] == entry:
        return True
    else:
        return False


def strip_list(l):
    """
    :param l: list to strip
    :return: the list without 1rst and last element if they were empty elements
    """
    while len(l) > 0 and l[0] == '':
        del l[0]
    while len(l) > 0 and l[len(l) - 1] == '':
        del l[len(l) - 1]


def occ_indexes(l, sub_l):
    """
    used for finding the concordances
    :param l: list
    :param seq: sub-list
    :return: indexes (x, y) for all occurrences of the sub-list in the list, an empty list if none found
    """
    return [(i, i+len(sub_l)) for i in range(len(l)) if l[i:i+len(sub_l)] == sub_l]


def merge_list_items(l, char):
    """
    merges the current item and the next in char is in the current item
    :param l: list to process
    :param char: character indicating where to merge
    :return: processed list
    """
    c = 0
    while c <= len(l) - 1:
        while char in l[c]:
            l[c:c + 2] = [''.join(l[c].replace(char, '') + l[c + 1])]
        c += 1
    return l


def split_list_items(l, char):
    """
    splits the current item and the next in char is in the current item
    :param l: list to process
    :param char: character indicating where to splits
    :return: processed list
    """
    c = 0
    while c <= len(l) - 1:
        while char in l[c]:
            l[c:c] = l.pop(c).split(char)
        c += 1
    return l


def is_tibetan_letter(char):
    """
    :param char: caracter to check
    :return: True or False
    """
    if (char >= 'ༀ' and char <= '༃') or (char >= 'ཀ' and char <= 'ྼ'):
        return True
    return False


def non_tib_chars(string):
    """
    :param string:
    :return: list of non-tibetan non-tibetan-punctuation characters found within a string
    """
    punct = ['༄', '༅', '།', '་', '༌', '༑', '༎', '༏', '༐', '༔']
    chars = []
    for character in string:
        if not is_tibetan_letter(character) and character not in chars and character not in punct:
            chars.append(character)
    return chars


class DefaultOrderedDict(OrderedDict):
    # Source: http://stackoverflow.com/a/6190500/562769
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
           not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory,
                          copy.deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory,
                                               OrderedDict.__repr__(self))


class PrepareTib:
    ''' Dealing with the punctuation of Tibetan '''

    def __init__(self, tibstring):
        self.raw = tibstring.replace('\n', '')  # fast hack to get rid of all returns
        self.punct = [" ", "༄", "༅", "࿓", "࿔", "༇", "༆", "༈", "།", "༎", "༏", "༐", "༑", "༔","་", "༌", "༼", "༽", "༒", "༓", "ཿ"]

    def gen_tuples(self):
        syllables = []
        puncts = []
        syl = ''
        for index, char in enumerate(self.raw):
            if index == 0:
                if char in self.punct:
                    puncts.append(char)
                else:
                    syl += char
            else:
                if char not in self.punct and self.raw[index-1] in self.punct:
                    syllables.append((syl, puncts))
                    puncts = []
                    syl = char
                elif char not in self.punct:
                    syl += char
                elif char in self.punct:
                    puncts.append(char)
        # add last syllable + its punctuation
        if syl != '':
            syllables.append((syl, puncts))
        return syllables

    def syl_tuples(self):
        tuples = PrepareTib.gen_tuples(self)
        return [(t[0], ''.join(t[1])) for t in tuples]

    def all_punct(self):
        tuples = PrepareTib.syl_tuples(self)
        return [t[0]+t[1] for t in tuples]

    def syls_only(self):
        tuples = PrepareTib.gen_tuples(self)
        return [t[0] for t in tuples]

    def tsheks_only(self):
        tuples = PrepareTib.syl_tuples(self)
        return [t[0]+'་' for t in tuples]

    def no_tshek(self):
        tuples = PrepareTib.syl_tuples(self)
        no_tshek = []
        for t in tuples:
            if '་' in t[1]:
                no_tshek.append(t[0]+t[1].replace('་', ''))
            else :
                no_tshek.append(t[0]+t[1])
        return no_tshek