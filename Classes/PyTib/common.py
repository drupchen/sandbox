# coding: utf-8

from bisect import bisect_left

from PyTib.icu import RuleBasedCollator


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

