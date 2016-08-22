# coding: utf-8

from bisect import bisect_left
from collections import OrderedDict, Callable
from tempfile import NamedTemporaryFile
from icu import RuleBasedCollator


def tib_sort(l):
    """
    sorts a list according to the Tibetan order
    code from https://github.com/eroux/tibetan-collation
    :param l: list to sort
    :return: sorted list
    """
    rules = '# Rules for Sanskrit ordering\n# From Bod rgya tshig mdzod chen mo pages 9, 11, 347, 1153, 1615, 1619, 1711, 1827, 1833, 2055, 2061, 2332, 2840, 2920, 2922, 2934, 3136 and 3137\n# Example: ཀར་ལུགས།  < ཀརྐ་ཊ།\n&ཀར=ཀར\n&ཀལ=ཀལ\n&ཀས=ཀས\n&གཉྫ=གཉྫ\n&ཐར=ཐར\n&པུས=པུས\n&ཕལ=ཕལ\n&བིལ=བིལ\n&མཉྫ=མཉྫ\n&མར=མར\n&ཤས=ཤས\n&སར=སར\n&ཨར=ཨར\n&ཨས=ཨས\n&ངྒྷ=ངྒྷ\n&ང༌ག=ངྒ\n&ད༌ད=དྡ\n&ན༌དེ=ནྡེ\n&མ༌བ=མྦ\n&ར༌པ=རྤ\n# Marks (seconadry different, with low equal primary weight after Lao)\n&ໆ<།<<༎<<༏<<༐<<༑<<༔<<༴<་=༌\n&ཀ<<ྈྐ<དཀ<བཀ<རྐ<ལྐ<སྐ<བརྐ<བསྐ\n&ཁ<<ྈྑ<མཁ<འཁ\n&ག<དགག<དགང<དགད<དགན<དགབ<དགཝ<དགའ<དགར<དགལ<དགས<དགི<དགུ<དགེ<དགོ<དགྭ<དགྱ<དགྲ<བགག<བགང<བགད<བགབ<བགམ<<<བགཾ<བགཝ<བགའ\n		<བགར<བགལ<བག⁠ས<བགི<བགུ<བགེ<བགོ<བགྭ<བགྱ<བགྲ<བགླ<མགག<མགང<མགད<མགབ<མགའ<མགར<མགལ<མག⁠ས<མགི<མགུ<མགེ<མགོ<མགྭ<མགྱ<མགྲ<འགག<འགང<འགད<འགན<འགབ<འགམ<<<འགཾ\n		<འགའ<འགར<འགལ<འགས<འགི<འགུ<འགེ<འགོ<འགྭ<འགྱ<འགྲ<རྒ<ལྒ<སྒ<བརྒ<བསྒ\n&ང<<<ྂ<<<ྃ<དངག<དངང<དངད<དངན<དངབ<དངའ<དངར<དངལ<དང⁠ས<དངི<དངུ<དངེ<དངོ<དངྭ<མངག<མངང<མངད<མངན<མངབ<མངའ<མངར<མངལ<མང⁠ས<མངི<མངུ<མངེ<མངོ<མངྭ<རྔ<ལྔ<སྔ<བརྔ<བསྔ\n&ཅ<གཅ<བཅ<ལྕ<བལྕ\n&ཆ<མཆ<འཆ\n&ཇ<མཇ<འཇ<རྗ<ལྗ<བརྗ\n&ཉ<<ྋྙ<གཉ<མཉ<རྙ<<<ཪྙ<སྙ<བརྙ<<<བཪྙ<བསྙ\n&ཏ<<<ཊ<གཏ<བཏ<རྟ<ལྟ<སྟ<བརྟ<བལྟ<བསྟ\n&ཐ<<<ཋ<མཐ<འཐ\n&ད<<<ཌ<གདག<གདང<གདད<གདན<གདབ<གདམ<<<གདཾ<གདའ<གདར<གདལ<གདས<གདི<གདུ<གདེ<གདོ<གདྭ<བདག<བདང<བདད<བདབ<བདམ<<<བདཾ<བདའ\n		<བདར<བདལ<བདས<བདི<བདུ<བདེ<བདོ<བདྭ<མདག<མདང<མདད<མདན<མདབ<མདའ<མདར<མདལ<མདས<མདི<མདུ<མདེ<མདོ<མདྭ<འདག<འདང<འདད<འདན<འདབ<འདམ<<<འདཾ\n		<འདའ<འདར<འདལ<འདས<འདི<འདུ<འདེ<འདོ<འདྭ<འདྲ<རྡ<ལྡ<སྡ<བརྡ<བལྡ<བསྡ\n&ན<<<ཎ<གནག<གནང<གནད<གནན<གནབ<གནམ<<<གནཾ<གནའ<གནར<གནལ<གནས<གནི<གནུ<གནེ<གནོ<གནྭ<མནག<མནང<མནད<མནན<མནབ<མནམ<<<མནཾ<མནའ\n		<མནར<མནལ<མནས<མནི<མནུ<མནེ<མནོ<མནྭ<རྣ<སྣ<བརྣ<བསྣ\n&པ<<ྉྤ<དཔག<དཔང<དཔད<དཔབ<དཔའ<དཔར<དཔལ<དཔས<དཔི<དཔུ<དཔེ<དཔོ<དཔྱ<དཔྲ<ལྤ<སྤ\n&ཕ<<ྉྥ<འཕ\n&བ<དབག<དབང<དབད<དབན<དབབ<དབའ<དབར<དབལ<དབས<དབི<དབུ<དབེ<དབོ<དབྭ<དབྱ<དབྲ<འབག<འབང<འབད<འབན<འབབ<འབམ\n	<<<འབཾ<འབའ<འབར<འབལ<འབས<འབི<འབུ<འབེ<འབོ<འབྭ<འབྱ<འབྲ<རྦ<ལྦ<སྦ\n&མ<<<ཾ<དམག<དམང<དམད<དམན<དམབ<དམཝ<དམའ<དམར<དམལ<དམས<དམི<དམུ<དམེ<དམོ<དམྭ<དམྱ<དམྲ<རྨ<སྨ\n&ཙ<གཙ<བཙ<རྩ<སྩ<བརྩ<བསྩ\n&ཚ<མཚ<འཚ\n&ཛ<མཛ<འཛ<རྫ<བརྫ\n# &ཝ\n&ཞ<གཞ<བཞ\n&ཟ<གཟ<བཟ\n# &འ\n&ཡ<གཡ\n&ར<<<ཪ<བརླ<<<བཪླ\n# &ལ\n&ཤ<<<ཥ<གཤ<བཤ\n&ས<གསག<གསང<གསད<གསན<གསབ<གསའ<གསར<གསལ<གསས<གསི<གསུ<གསེ<གསོ<གསྭ<བསག<བསང<བསད<བསབ<བསམ<<<བསཾ<བསའ<བསར\n		<བསལ<བསས<བསི<བསུ<བསེ<བསོ<བསྭ<བསྲ<བསླ\n&ཧ<ལྷ\n# &ཨ\n# Explicit vowels\n<ཱ<ི<ཱི<ྀ<ཱྀ<ུ<ཱུ<ེ<ཻ=ེེ<ོ<ཽ=ོོ\n# Post-radicals\n	<ྐ<ྑ<ྒ<ྔ<ྕ<ྖ<ྗ<ྙ<ྟ<<<ྚ<ྠ<<<ྛ<ྡ<<<ྜ<ྣ<<<ྞ<ྤ<ྥ<ྦ<ྨ<ྩ<ྪ<ྫ<ྭ<<<ྺ<ྮ<ྯ<ྰ<ྱ<<<ྻ<ྲ<<<ྼ<ླ<ྴ\n	<<<ྵ<ྶ<ྷ<ྸ\n# Combining marks and signs (secondary weight)\n&༹<<྄<<ཿ<<྅<<ྈ<<ྉ<<ྊ<<ྋ<<ྌ<<ྍ<<ྎ<<ྏ\n# Treatༀ,  ཷand ,ཹ as decomposed\n&ཨོཾ=ༀ\n&ྲཱྀ=ཷ\n&ླཱྀ=ཹ\n# Shorthands for ག,ས\n&དགགས<<<དགཊ<<<དགཌ\n&བགགས<<<བགཊ<<<བགཌ\n&འགགས<<<འགཊ<<<འགཌ\n&དངགས<<<དངཊ<<<དངཌ\n&མངགས<<<མངཊ<<<མངཌ\n&གདགས<<<གདཊ<<<གདཌ\n&བདགས<<<བདཊ<<<བདཌ\n&མདགས<<<མདཊ<<<མདཌ\n&འདགས<<<འདཊ<<<འདཌ\n&གནགས<<<གནཊ<<<གནཌ\n&མནགས<<<མནཊ<<<མནཌ\n&དཔགས<<<དཔཊ<<<དཔཌ\n&དབགས<<<དབཊ<<<དབཌ\n&འབགས<<<འབཊ<<<འབཌ\n&དམགས<<<དམཊ<<<དམཌ\n&གསགས<<<གསཊ<<<གསཌ\n&བསགས<<<བསཊ<<<བསཌ'
    collator = RuleBasedCollator('[normalization on]\n' + rules)
    return sorted(l, key=collator.getSortKey)


def write_file(file_path, content):
    with open(file_path, 'w', -1, 'utf8') as f:
        f.write(content)


def open_file(file_path):
    with open(file_path, 'r', -1, 'utf-8-sig') as f:
        return f.read()


def temp_object(content):
    temp = NamedTemporaryFile(delete=True)
    temp.write(str.encode(content))
    return temp


def pre_process(raw_string, mode='words'):
    """
    Splits a raw Tibetan orig_list by the punctuation and syllables or words
    :param raw_string:
    :param mode: words for splitting on words, syls for splitting in syllables. Default value is words
    :return: a list with the elements separated from the punctuation
    """
    import re

    def is_punct(string):
        # put in common
        if '༄' in string or '༅' in string or '༆' in string or '༇' in string or '༈' in string or \
            '།' in string or '༎' in string or '༏' in string or '༐' in string or '༑' in string or \
            '༔' in string or ';' in string or ':' in string:
            return True
        else:
            return False

    def trim_punct(l):
        i = 0
        while i < len(l) - 1:
            if is_punct(l[i]) and is_punct(l[i + 1]):
                del l[i + 1]
            i += 1

    yigo = r'((༄༅+|༆|༇|༈)།?༎? ?།?༎?)'
    text_punct = r'(( *། *| *༎ *| *༏ *| *༐ *| *༑ *| *༔ *)+)'
    splitted = []
    # replace unbreakable tsek and tabs
    raw_string = raw_string.replace('༌', '་').replace('   ', ' ')
    # split the raw orig_list by the yigos,
    for text in re.split(yigo, raw_string):
        # add the yigos to the list
        if re.match(yigo, text):
            splitted.append(text.replace(' ', '_'))
        elif text != '':
            # split the orig_list between yigos by the text pre_process
            for par in re.split(text_punct, text):
                # add the pre_process to the list
                if is_punct(par):
                    splitted.append(par.replace(' ', '_'))
                elif par != '':
                    # add the segmented text split on words
                    if mode == 'words':
                        splitted.extend(par.split(' '))
                    # add the non-segmented text by splitting it on syllables.
                    elif mode == 'syls':
                        temp = []
                        for chunk in par.split(' '):
                            if '་' in chunk:
                                word = ''
                                for c in chunk:
                                    if c == '་':
                                        word += c
                                        temp.append(word)
                                        word = ''
                                    else:
                                        word += c
                                # adding the last word in temp[]
                                if word != '':
                                    temp.append(word)
                            else:
                                temp.append(chunk)
                        splitted.extend(temp)
                    else:
                        print('non-valid splitting mode. choose either "words" or "syls".')
                        break
    # trim the extra pre_process
    trim_punct(splitted)
    return splitted


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
    :param sub_l: sub-list
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
    :return: list of non-tibetan non-tibetan-pre_process characters found within a orig_list
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

    def __deepcopy__(self):
        import copy
        return type(self)(self.default_factory, copy.deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory, OrderedDict.__repr__(self))
