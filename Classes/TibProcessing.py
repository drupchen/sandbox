# coding: utf-8

import re

mark = '*'  # marker of unknown syllables. Can’t be a letter. Only 1 char allowed. Can’t be left empty.


def strip_list(l):
    """
    :param l: list to strip
    :return: the list without 1rst and last element if they were empty elements
    """
    if l[0] == '':
        del l[0]
    if l[len(l) - 1] == '':
        del l[len(l) - 1]


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


class SylComponents:
    """
    Provides information about a syllable
    """

    def __init__(self):
        # check for possible dadrag https://github.com/eroux/tibetan-spellchecker/blob/master/doc/second-suffix-da.md
        self.dadrag = ['ཀུན', 'ཤིན', 'འོན']
        # roots is an import from root + rareC and wazurC and suffixes is the 'AB' entry from  suffixes.json
        self.roots = {
            'ཀ': 'A', 'ཀྱ': 'A', 'ཀྲ': 'A', 'ཀླ': 'A', 'དཀ': 'NB', 'དཀྱ': 'A', 'དཀྲ': 'A', 'དཀླ': 'A', 'བཀ': 'NB',
            'བཀྱ': 'A', 'བཀྲ': 'A', 'བཀླ': 'A', 'རྐ': 'A', 'རྐྱ': 'A', 'ལྐ': 'A', 'སྐ': 'A', 'སྐྱ': 'A', 'སྐྲ': 'A',
            'བརྐ': 'A', 'བརྐྱ': 'A', 'བསྐ': 'A', 'བསྐྱ': 'A', 'བསྐྲ': 'A', 'ཀའུ': 'C', 'ཀིའུ': 'C', 'ཀེའུ': 'C',
            'ཀོའུ': 'C', 'ཀྲུའུ': 'C', 'ཀྭའི': 'C', 'ཀྭ': 'C', 'ཀརྨ': 'C',
            'ཁ': 'A', 'ཁྱ': 'A', 'ཁྲ': 'A', 'མཁ': 'NB', 'མཁྱ': 'A', 'མཁྲ': 'A', 'འཁ': 'NB', 'འཁྱ': 'A', 'འཁྲ': 'A',
            'ཁེའུ': 'C', 'ཁྱིའུ': 'C', 'ཁྱེའུ': 'C', 'ཁྲིའུ': 'C', 'ཁྲུའུ': 'C', 'ཁྲེའུ': 'C', 'ཁྭ': 'C',
            'ག': 'A', 'གྱ': 'A', 'གྲ': 'A', 'གླ': 'A', 'དག': 'NB', 'དགྱ': 'A', 'དགྲ': 'A', 'བག': 'NB', 'བགྱ': 'A',
            'བགྲ': 'A', 'མག': 'NB', 'མགྱ': 'A', 'མགྲ': 'A', 'འག': 'NB', 'འགྱ': 'A', 'འགྲ': 'A', 'རྒ': 'A', 'རྒྱ': 'A',
            'ལྒ': 'A', 'སྒ': 'A', 'སྒྱ': 'A', 'སྒྲ': 'A', 'བརྒ': 'A', 'བརྒྱ': 'A', 'བསྒ': 'A', 'བསྒྱ': 'A', 'བསྒྲ': 'A',
            'གའུ': 'C', 'གྲིའུ': 'C', 'གྲེའུ': 'C', 'གླེའུ': 'C', 'འགིའུ': 'C', 'འགོའུ': 'C', 'རྒེའུ': 'C', 'སྒའུ': 'C',
            'སྒེའུ': 'C', 'སྒྱེའུ': 'C', 'སྒྲེའུ': 'C', 'གྭ': 'C', 'གྲྭ': 'C',
            'ང': 'A', 'དང': 'NB', 'མང': 'NB', 'རྔ': 'A', 'ལྔ': 'A', 'སྔ': 'A', 'བརྔ': 'A', 'བསྔ': 'A', 'རྔེའུ': 'C',
            'སྔེའུ': 'C',
            'ཅ': 'A', 'གཅ': 'NB', 'བཅ': 'NB', 'ལྕ': 'A', 'གཅིའུ': 'C', 'གཅེའུ': 'C', 'ལྕེའུ': 'C',
            'ཆ': 'A', 'མཆ': 'NB', 'འཆ': 'NB',
            'ཇ': 'A', 'མཇ': 'NB', 'འཇ': 'NB', 'རྗ': 'A', 'ལྗ': 'A', 'བརྗ': 'A', 'རྗེའུ': 'C',
            'ཉ': 'A', 'གཉ': 'NB', 'མཉ': 'NB', 'རྙ': 'A', 'སྙ': 'A', 'བརྙ': 'A', 'བསྙ': 'A', 'ཉེའུ': 'C', 'སྙེའུ': 'C',
            'ཉྭ': 'C',
            'ཏ': 'A', 'ཏྲ': 'A', 'གཏ': 'NB', 'གཏྲ': 'A', 'བཏ': 'NB', 'བཏྲ': 'A', 'རྟ': 'A', 'ལྟ': 'A', 'སྟ': 'A',
            'བརྟ': 'A', 'བལྟ': 'A', 'བསྟ': 'A', 'ཏེའུ': 'C', 'གཏེའུ': 'C', 'རྟའུ': 'C', 'རྟེའུ': 'C', 'སྟེའུ': 'C',
            'སྟྭ': 'C',
            'ཐ': 'A', 'ཐྲ': 'A', 'མཐ': 'NB', 'འཐ': 'NB', 'ཐིའུ': 'C', 'ཐུའུ': 'C', 'ཐེའུ': 'C', 'ཐོའུ': 'C',
            'མཐེའུ': 'C',
            'ད': 'A', 'དྲ': 'A', 'གད': 'NB', 'བད': 'NB', 'མད': 'NB', 'འད': 'NB', 'འདྲ': 'A', 'རྡ': 'A', 'ལྡ': 'A',
            'སྡ': 'A', 'བརྡ': 'A', 'བལྡ': 'A', 'བསྡ': 'A', 'དུའུ': 'C', 'དེའུ': 'C', 'དྲེའུ': 'C', 'མདེའུ': 'C',
            'རྡེའུ': 'C', 'སྡེའུ': 'C', 'དྲྭ': 'C', 'དྭ': 'C', 'དྭོ': 'C',
            'ན': 'A', 'གན': 'NB', 'མན': 'NB', 'རྣ': 'A', 'སྣ': 'A', 'སྣྲ': 'A', 'བརྣ': 'A', 'བསྣ': 'A', 'ནའུ': 'C',
            'ནེའུ': 'C', 'ནོའུ': 'C', 'སྣེའུ': 'C',
            'པ': 'A', 'པྱ': 'A', 'པྲ': 'A', 'དཔ': 'NB', 'དཔྱ': 'A', 'དཔྲ': 'A', 'ལྤ': 'A', 'སྤ': 'A', 'སྤྱ': 'A',
            'སྤྲ': 'A', 'དཔེའུ': 'C', 'སྤའུ': 'C', 'སྤེའུ': 'C', 'སྤྱིའུ': 'C', 'སྤྲེའུ': 'C', 'པདྨ': 'C',
            'ཕ': 'A', 'ཕྱ': 'A', 'ཕྲ': 'A', 'འཕ': 'NB', 'འཕྱ': 'A', 'འཕྲ': 'A', 'ཕེའུ': 'C', 'ཕྲའུ': 'C', 'ཕྲེའུ': 'C',
            'འཕེའུ': 'C', 'ཕྱྭ': 'C',
            'བ': 'A', 'བྱ': 'A', 'བྲ': 'A', 'བླ': 'A', 'དབ': 'NB', 'དབྱ': 'A', 'དབྲ': 'A', 'འབ': 'NB', 'འབྱ': 'A',
            'འབྲ': 'A', 'རྦ': 'A', 'ལྦ': 'A', 'སྦ': 'A', 'སྦྱ': 'A', 'སྦྲ': 'A', 'བེའུ': 'C', 'བྱའུ': 'C', 'བྱིའུ': 'C',
            'བྱེའུ': 'C', 'བྲའུ': 'C', 'བྲའོ': 'C', 'བྲེའུ': 'C', 'བྲོའུ': 'C', 'འབེའུ': 'C', 'སྦྲེའུ': 'C',
            'མ': 'A', 'མྱ': 'A', 'མྲ': 'A', 'དམ': 'NB', 'དམྱ': 'A', 'དམྲ': 'A', 'རྨ': 'A', 'རྨྱ': 'A', 'སྨ': 'A',
            'སྨྱ': 'A', 'སྨྲ': 'A', 'མིའུ': 'C', 'མུའུ': 'C', 'མོའུ': 'C', 'མྱིའུ': 'C', 'རྨེའུ': 'C', 'སྨེའུ': 'C',
            'ཙ': 'A', 'གཙ': 'NB', 'བཙ': 'NB', 'རྩ': 'A', 'སྩ': 'A', 'བརྩ': 'A', 'བསྩ': 'A', 'ཙིའུ': 'C', 'ཙེའུ': 'C',
            'གཙེའུ': 'C', 'རྩེའུ': 'C', 'རྩྭ': 'C',
            'ཚ': 'A', 'མཚ': 'NB', 'འཚ': 'NB', 'ཚའུ': 'C', 'ཚུའུ': 'C', 'ཚེའུ': 'C', 'མཚེའུ': 'C', 'ཚྭ': 'C',
            'ཛ': 'A', 'མཛ': 'NB', 'འཛ': 'NB', 'རྫ': 'A', 'བརྫ': 'A', 'རྫིའུ': 'C', 'རྫེའུ': 'C', 'གཞུའུ': 'C',
            'ཝ': 'A',
            'ཞ': 'A', 'གཞ': 'NB', 'བཞ': 'NB', 'ཞྭ': 'C',
            'ཟ': 'A', 'ཟླ': 'A', 'གཟ': 'NB', 'བཟ': 'NB', 'བཟླ': 'A', 'ཟེའུ': 'C', 'ཟྭ': 'C',
            'འ': 'A',
            'ཡ': 'A', 'གཡ': 'NB', 'ཡེའུ': 'C', 'གཡིའུ': 'C',
            'ར': 'A', 'རླ': 'A', 'བརླ': 'A', 'རེའུ': 'C', 'རྭ': 'C',
            'ལ': 'A', 'ལའུ': 'C', 'ལིའུ': 'C', 'ལེའུ': 'C', 'ལོའུ': 'C', 'ལྭ': 'C',
            'ཤ': 'A', 'གཤ': 'NB', 'བཤ': 'NB', 'ཤའུ': 'C', 'ཤེའུ': 'C', 'ཤྭ': 'C',
            'ས': 'A', 'སྲ': 'A', 'སླ': 'A', 'གས': 'NB', 'བས': 'NB', 'བསྲ': 'A', 'བསླ': 'A', 'སིའུ': 'C', 'སེའུ': 'C',
            'སྲིའུ': 'C', 'སླེའུ': 'C', 'བསེའུ': 'C', 'སླེའོ': 'C', 'བསྭོ': 'C', 'སྭ': 'C', 'བསྭ': 'C',
            'ཧ': 'A', 'ཧྲ': 'A', 'ལྷ': 'A', 'ཧུའུ': 'C', 'ཧེའུ': 'C', 'ཧྲུའུ': 'C', 'ཧྭ': 'C',
            'ཨ': 'A'
        }
        self.suffixes = ["འ", "ག", "གས", "ང", "ངས", "ད", "ན", "བ", "བས", "མ", "མས", "ལ", "འི", "འོ", "འང", "འམ", "ར",
                         "ས",
                         "ི", "ིག", "ིགས", "ིང", "ིངས", "ིད", "ིན", "ིབ", "ིབས", "ིམ", "ིམས", "ིལ", "ིའི", "ིའོ", "ིའང",
                         "ིའམ", "ིར", "ིས",
                         "ུ", "ུག", "ུགས", "ུང", "ུངས", "ུད", "ུན", "ུབ", "ུབས", "ུམ", "ུམས", "ུལ", "ུའི", "ུའོ", "ུའང",
                         "ུའམ", "ུར", "ུས",
                         "ེ", "ེག", "ེགས", "ེང", "ེངས", "ེད", "ེན", "ེབ", "ེབས", "ེམ", "ེམས", "ེལ", "ེའི", "ེའོ", "ེའང",
                         "ེའམ", "ེར", "ེས",
                         "ོ", "ོག", "ོགས", "ོང", "ོངས", "ོད", "ོན", "ོབ", "ོབས", "ོམ", "ོམས", "ོལ", "ོའི", "ོའོ", "ོའང",
                         "ོའམ", "ོར", "ོས"]
        self.Csuffixes = ["འི", "འོ", "འང", "འམ", "ར", "ས"]

        # all dicts from https://github.com/eroux/tibetan-spellchecker/tree/master/syllables
        self.special = ['བགླ', 'མདྲོན', 'བརྡའ', 'བརྟའ']
        self.wazurs = ['ཧྭག', 'ཀྭས', 'ཁྭངས', 'ཧྭང', 'ཀྭན', 'དྭགས', 'ཧྭགས', 'དྭངས', 'ཏྭོན']
        self.exceptions = self.special + self.wazurs
        self.ambiguous = {'མངས': ('མ', 'ངས'), 'མགས': ('མ', 'གས'), 'དབས': ('ད', 'བས'), 'དངས': ('ད', 'ངས'),
                          'དགས': ('དག', 'ས'), 'དམས': ('དམ', 'ས'), 'བགས': ('བ', 'གས'), 'འབས': ('འབ', 'ས'),
                          'འགས': ('འག', 'ས')}

        self.m_roots = {'ཀ': 'ཀ', 'ཀྱ': 'ཀ', 'ཀྲ': 'ཀ', 'ཀླ': 'ལ', 'དཀ': 'ཀ', 'དཀྱ': 'ཀ', 'དཀྲ': 'ཀ', 'དཀླ': 'ལ',
                        'བཀ': 'ཀ', 'བཀྱ': 'ཀ', 'བཀྲ': 'ཀ', 'བཀླ': 'ླ', 'རྐ': 'ྐ', 'རྐྱ': 'ྐ', 'ལྐ': 'ྐ', 'སྐ': 'ྐ',
                        'སྐྱ': 'ྐ', 'སྐྲ': 'ྐ', 'བརྐ': 'ྐ', 'བརྐྱ': 'ྐ', 'བསྐ': 'ྐ', 'བསྐྱ': 'ྐ', 'བསྐྲ': 'ྐ', 'ཁ': 'ཁ',
                        'ཁྱ': 'ཁ', 'ཁྲ': 'ཁ', 'མཁ': 'ཁ', 'མཁྱ': 'ཁ', 'མཁྲ': 'ཁ', 'འཁ': 'ཁ', 'འཁྱ': 'ཁ', 'འཁྲ': 'ཁ',
                        'ག': 'ག', 'གྱ': 'ག', 'གྲ': 'ག', 'གླ': 'ླ', 'དག': 'ག', 'དགྱ': 'ག', 'དགྲ': 'ག', 'བག': 'ག',
                        'བགྱ': 'ག', 'བགྲ': 'ག', 'མག': 'ག', 'མགྱ': 'ག', 'མགྲ': 'ག', 'འག': 'ག', 'འགྱ': 'ག', 'འགྲ': 'ག',
                        'རྒ': 'ྒ', 'རྒྱ': 'ྒ', 'ལྒ': 'ྒ', 'སྒ': 'ྒ', 'སྒྱ': 'ྒ', 'སྒྲ': 'ྒ', 'བརྒ': 'ྒ', 'བརྒྱ': 'ྒ',
                        'བསྒ': 'ྒ', 'བསྒྱ': 'ྒ', 'བསྒྲ': 'ྒ', 'ང': 'ང', 'དང': 'ང', 'མང': 'ང', 'རྔ': 'ྔ', 'ལྔ': 'ྔ',
                        'སྔ': 'ྔ', 'བརྔ': 'ྔ', 'བསྔ': 'ྔ', 'ཅ': 'ཅ', 'གཅ': 'ཅ', 'བཅ': 'ཅ', 'ལྕ': 'ྕ', 'ཆ': 'ཆ',
                        'མཆ': 'ཆ', 'འཆ': 'ཆ', 'ཇ': 'ཇ', 'མཇ': 'ཇ', 'འཇ': 'ཇ', 'རྗ': 'ྗ', 'ལྗ': 'ྗ', 'བརྗ': 'ྗ',
                        'ཉ': 'ཉ', 'གཉ': 'ཉ', 'མཉ': 'ཉ', 'རྙ': 'ྙ', 'སྙ': 'ྙ', 'བརྙ': 'ྙ', 'བསྙ': 'ྙ', 'ཏ': 'ཏ',
                        'ཏྲ': 'ཏ', 'གཏ': 'ཏ', 'གཏྲ': 'ཏ', 'བཏ': 'ཏ', 'བཏྲ': 'ཏ', 'རྟ': 'ྟ', 'ལྟ': 'ྟ', 'སྟ': 'ྟ',
                        'བརྟ': 'ྟ', 'བལྟ': 'ྟ', 'བསྟ': 'ྟ', 'ཐ': 'ཐ', 'ཐྲ': 'ཐ', 'མཐ': 'ཐ', 'འཐ': 'ཐ', 'ད': 'ད',
                        'དྲ': 'ད', 'གད': 'ད', 'བད': 'ད', 'མད': 'ད', 'འད': 'ད', 'འདྲ': 'ད', 'རྡ': 'ྡ', 'ལྡ': 'ྡ',
                        'སྡ': 'ྡ', 'བརྡ': 'ྡ', 'བལྡ': 'ྡ', 'བསྡ': 'ྡ', 'ན': 'ན', 'གན': 'ན', 'མན': 'ན', 'རྣ': 'ྣ',
                        'སྣ': 'ྣ', 'སྣྲ': 'ྣ', 'བརྣ': 'ྣ', 'བསྣ': 'ྣ', 'པ': 'པ', 'པྱ': 'པ', 'པྲ': 'པ', 'དཔ': 'པ',
                        'དཔྱ': 'པ', 'དཔྲ': 'པ', 'ལྤ': 'ྤ', 'སྤ': 'ྤ', 'སྤྱ': 'ྤ', 'སྤྲ': 'ྤ', 'ཕ': 'ཕ', 'ཕྱ': 'ཕ',
                        'ཕྲ': 'ཕ', 'འཕ': 'ཕ', 'འཕྱ': 'ཕ', 'འཕྲ': 'ཕ', 'བ': 'བ', 'བྱ': 'བ', 'བྲ': 'བ', 'བླ': 'ླ',
                        'དབ': 'བ', 'དབྱ': 'བ', 'དབྲ': 'བ', 'འབ': 'བ', 'འབྱ': 'བ', 'འབྲ': 'བ', 'རྦ': 'ྦ', 'ལྦ': 'ྦ',
                        'སྦ': 'ྦ', 'སྦྱ': 'ྦ', 'སྦྲ': 'ྦ', 'མ': 'མ', 'མྱ': 'མ', 'མྲ': 'མ', 'དམ': 'མ', 'དམྱ': 'མ',
                        'དམྲ': 'མ', 'རྨ': 'ྨ', 'རྨྱ': 'ྨ', 'སྨ': 'ྨ', 'སྨྱ': 'ྨ', 'སྨྲ': 'ྨ', 'ཙ': 'ཙ', 'གཙ': 'ཙ',
                        'བཙ': 'ཙ', 'རྩ': 'ྩ', 'སྩ': 'ྩ', 'བརྩ': 'ྩ', 'བསྩ': 'ྩ', 'ཚ': 'ཚ', 'མཚ': 'ཚ', 'འཚ': 'ཚ',
                        'ཛ': 'ཛ', 'མཛ': 'ཛ', 'འཛ': 'ཛ', 'རྫ': 'ྫ', 'བརྫ': 'ྫ', 'ཝ': 'ཝ', 'ཞ': 'ཞ', 'གཞ': 'ཞ', 'བཞ': 'ཞ',
                        'ཟ': 'ཟ', 'ཟླ': 'ླ', 'གཟ': 'ཟ', 'བཟ': 'ཟ', 'བཟླ': 'ླ', 'འ': 'འ', 'ཡ': 'ཡ', 'གཡ': 'ཡ', 'ར': 'ར',
                        'རླ': 'ླ', 'བརླ': 'ླ', 'ལ': 'ལ', 'ཤ': 'ཤ', 'གཤ': 'ཤ', 'བཤ': 'ཤ', 'ས': 'ས', 'སྲ': 'ས', 'སླ': 'ླ',
                        'གས': 'ས', 'བས': 'ས', 'བསྲ': 'ས', 'བསླ': 'ླ', 'ཧ': 'ཧ', 'ཧྲ': 'ཧ', 'ལྷ': 'ྷ', 'ཨ': 'ཨ',
                        'ཀའུ': 'འ', 'ཀིའུ': 'འ', 'ཀེའུ': 'འ', 'ཀོའུ': 'འ', 'ཀྲུའུ': 'འ', 'ཁེའུ': 'འ', 'ཁྱིའུ': 'འ',
                        'ཁྱེའུ': 'འ', 'ཁྲིའུ': 'འ', 'ཁྲུའུ': 'འ', 'ཁྲེའུ': 'འ', 'གའུ': 'འ', 'གྲིའུ': 'འ', 'གྲེའུ': 'འ',
                        'གླེའུ': 'འ', 'འགིའུ': 'འ', 'འགོའུ': 'འ', 'རྒེའུ': 'འ', 'སྒའུ': 'འ', 'སྒེའུ': 'འ',
                        'སྒྱེའུ': 'འ', 'སྒྲེའུ': 'འ', 'རྔེའུ': 'འ', 'སྔེའུ': 'འ', 'གཅིའུ': 'འ', 'གཅེའུ': 'འ',
                        'ལྕེའུ': 'འ', 'རྗེའུ': 'འ', 'ཉེའུ': 'འ', 'སྙེའུ': 'འ', 'ཏེའུ': 'འ', 'གཏེའུ': 'འ', 'རྟའུ': 'འ',
                        'རྟེའུ': 'འ', 'སྟེའུ': 'འ', 'ཐིའུ': 'འ', 'ཐུའུ': 'འ', 'ཐེའུ': 'འ', 'ཐོའུ': 'འ', 'མཐེའུ': 'འ',
                        'དུའུ': 'འ', 'དེའུ': 'འ', 'དྲེའུ': 'འ', 'མདེའུ': 'འ', 'རྡེའུ': 'འ', 'སྡེའུ': 'འ', 'ནའུ': 'འ',
                        'ནེའུ': 'འ', 'ནོའུ': 'འ', 'སྣེའུ': 'འ', 'དཔེའུ': 'འ', 'སྤའུ': 'འ', 'སྤེའུ': 'འ', 'སྤྱིའུ': 'འ',
                        'སྤྲེའུ': 'འ', 'ཕེའུ': 'འ', 'ཕྲའུ': 'འ', 'ཕྲེའུ': 'འ', 'འཕེའུ': 'འ', 'བེའུ': 'འ', 'བྱའུ': 'འ',
                        'བྱིའུ': 'འ', 'བྱེའུ': 'འ', 'བྲའུ': 'འ', 'བྲའོ': 'འ', 'བྲེའུ': 'འ', 'བྲོའུ': 'འ', 'འབེའུ': 'འ',
                        'སྦྲེའུ': 'འ', 'མིའུ': 'འ', 'མུའུ': 'འ', 'མོའུ': 'འ', 'མྱིའུ': 'འ', 'རྨེའུ': 'འ', 'སྨེའུ': 'འ',
                        'ཙིའུ': 'འ', 'ཙེའུ': 'འ', 'གཙེའུ': 'འ', 'རྩེའུ': 'འ', 'ཚའུ': 'འ', 'ཚུའུ': 'འ', 'ཚེའུ': 'འ',
                        'མཚེའུ': 'འ', 'རྫིའུ': 'འ', 'རྫེའུ': 'འ', 'གཞུའུ': 'འ', 'ཟེའུ': 'འ', 'ཡེའུ': 'འ', 'གཡིའུ': 'འ',
                        'རེའུ': 'འ', 'ལའུ': 'འ', 'ལིའུ': 'འ', 'ལེའུ': 'འ', 'ལོའུ': 'འ', 'ཤའུ': 'འ', 'ཤེའུ': 'འ',
                        'སིའུ': 'འ', 'སེའུ': 'འ', 'སྲིའུ': 'འ', 'སླེའུ': 'འ', 'བསེའུ': 'འ', 'སླེའོ': 'འ', 'ཧུའུ': 'འ',
                        'ཧེའུ': 'འ', 'ཧྲུའུ': 'འ', 'སྟྭ': 'ྟ', 'གྭ': 'ག', 'ཞྭ': 'ཞ', 'ཁྭ': 'ཁ', 'དྲྭ': 'ད', 'ཀྭའི': 'ཀ',
                        'བསྭོ': 'ས', 'དྭ': 'ད', 'རྭ': 'ར', 'སྭ': 'ས', 'ཤྭ': 'ཤ', 'ཧྭ': 'ཧ', 'ལྭ': 'ལ', 'ཕྱྭ': 'ཕ',
                        'ཟྭ': 'ཟ', 'ཀྭ': 'ཀ', 'དྭོ': 'ད', 'ཉྭ': 'ཉ', 'ཚྭ': 'ཚ', 'རྩྭ': 'ྩ', 'བསྭ': 'ས', 'གྲྭ': 'ག',
                        'ཧྭག': 'ཧ', 'ཀྭས': 'ཀ', 'ཁྭངས': 'ཁ', 'ཧྭང': 'ཧ', 'ཀྭན': 'ཀ', 'དྭགས': 'ད', 'ཧྭགས': 'ཧ',
                        'དྭངས': 'ད', 'ཏྭོན': 'ཏ', 'ཧྤ': 'ྤ', 'ཀརྨ': 'ྨ', 'པདྨ': 'ྨ'}
        self.m_exceptions = {'བགླ': 'ླ', 'མདྲོན': 'ད', 'བརྡའ': 'ྡ', 'བརྟའ': 'ྟ'}
        self.m_wazurs = {'ཧྭག': 'ཧ', 'ཀྭས': 'ཀ', 'ཁྭངས': 'ཁ', 'ཧྭང': 'ཧ', 'ཀྭན': 'ཀ', 'དྭགས': 'ད', 'ཧྭགས': 'ཧ',
                         'དྭངས': 'ད', 'ཏྭོན': 'ཏ'}
        self.mingzhis = {**self.m_roots, **self.m_exceptions, **self.m_wazurs}

    def get_parts(self, syl):
        """

        :param syl: takes a syllable as input
        :return: a tuple:
                        - (prefix+main-stack, vowel+suffixes)
                        - (exceptions, x)
                        - a list of solutions if there is more than one
                        - None if the syllable is not wellformed
        """
        if syl not in self.exceptions and syl not in self.ambiguous:
            l_s = len(syl)
            # find all possible roots
            root = []
            if len(syl) > 5 and syl[:6] in self.roots:
                root.append(syl[:6])
            if len(syl) > 4 and syl[:5] in self.roots:
                root.append(syl[:5])
            if len(syl) > 3 and syl[:4] in self.roots:
                root.append(syl[:4])
            if len(syl) > 2 and syl[:3] in self.roots:
                root.append(syl[:3])
            if len(syl) > 1 and syl[:2] in self.roots:
                root.append(syl[:2])
            if len(syl) > 0 and syl[:1] in self.roots:
                root.append(syl[:1])
            # find all possible suffixes
            suffix = []
            if l_s > 1:
                if syl[l_s - 1:] in self.suffixes:
                    suffix.append(syl[l_s - 1:])
                if syl[l_s - 2:] in self.suffixes:
                    suffix.append(syl[l_s - 2:])
                if syl[l_s - 3:] in self.suffixes:
                    suffix.append(syl[l_s - 3:])

            # deal with all the C roots
            # print(self.syl, root)
            if root != [] and self.roots[root[0]] == 'C':
                if root[0] == syl:
                    return root[0], ''
                else:
                    for s in suffix:
                        if s in self.Csuffixes and root[0] + s == syl:
                            return root[0], s

            # find all possible matches
            solutions = []
            if suffix != [] and root != []:
                # dealing with all other cases
                for r in root:
                    for s in suffix:
                        # unexpected འ་
                        if self.roots[r] == 'A' and s == 'འ' and r + s == syl:
                            # print(r, roots[r])
                            return None
                        else:
                            # if root+suffix make the syllable + avoids duplicates
                            if r + s == syl and (r, s) not in solutions:
                                solutions.append((r, s))
                if solutions != []:
                    if len(solutions) > 1:
                        return solutions
                    else:
                        return solutions[0]
                # root + suffix don’t make syl
                else:
                    # print(solutions)
                    return None
            elif root != []:
                # print('k')
                for r in root:
                    if r in self.roots and r == syl:
                        # if syllable is valid without suffix + without aa
                        if self.roots[r] != 'NB' and (r, '') not in solutions:
                            solutions.append((r, ''))
                if solutions != []:
                    if len(solutions) > 1:
                        return solutions
                    else:
                        return solutions[0]
                # non-valid syl
                else:
                    return None
            # non-valid syl
            else:
                return None
        elif syl in self.ambiguous:
            return self.ambiguous[syl]
        else:
            return syl, 'x'

    def get_mingzhi(self, syl):
        """

        :param syl: syllable
        :return:    the mingzhi that will serve for the particle agreement. for example, ཁྱེའུར will return འ
                    None if more than one solution from get_parts()
        """
        components = self.get_parts(syl)
        if type(components) == 'list' or not components:
            return None
        else:
            return self.mingzhis[components[0]]

    def get_info(self, syl):
        """

        :param syl: syllable
        :return: required info to part_agreement:
                - dadrag
                - thame
                - the syllable
        """
        mingzhi = self.get_mingzhi(syl)
        if not mingzhi:
            return None
        else:
            if syl in self.dadrag:
                return 'dadrag'
            elif re.findall(mingzhi + '[ིེོུྱྲླྷྭ]*$', syl) != []:
                return 'thame'
            else:
                return syl


def part_agreement(previous, particle):
    """
    proposes the right particle according to the previous syllable.
        In case of an invalid previous syllable, returns the particle preceded by *
        limitation : particle needs to be a separate syllabes. (the problems with wrong merged agreement will be flagged by get_mingzhi )
        input : previous syllable, particle
    :param previous: preceding syllable
    :param particle: particle at hand
    :return: the correct agreement for the preceding syllable
    """
    previous = SylComponents().get_info(previous)
    final = ''
    if previous == 'dadrag':
        final = 'ད་དྲག'
    elif previous == 'thame':
        final = 'མཐའ་མེད'
    else:
        final = previous[-1]
        if final not in ['ག', 'ང', 'ད', 'ན', 'བ', 'མ', 'འ', 'ར', 'ལ', 'ས']:
            final = None

    if final:
        # added the ད་དྲག་ for all and the མཐའ་མེད་ for all in provision of all cases
        # where an extra syllable is needed in verses
        # dadrag added according to Élie’s rules.
        dreldra = {'ད': 'ཀྱི', 'བ': 'ཀྱི', 'ས': 'ཀྱི', 'ག': 'གི', 'ང': 'གི', 'ན': 'གྱི', 'མ': 'གྱི', 'ར': 'གྱི',
                   'ལ': 'གྱི', 'འ': 'ཡི', 'མཐའ་མེད': 'ཡི', 'ད་དྲག': 'གྱི'}
        jedra = {'ད': 'ཀྱིས', 'བ': 'ཀྱིས', 'ས': 'ཀྱིས', 'ག': 'གིས', 'ང': 'གིས', 'ན': 'གྱིས', 'མ': 'གྱིས', 'ར': 'གྱིས',
                 'ལ': 'གྱིས', 'འ': 'ཡིས', 'མཐའ་མེད': 'ཡིས', 'ད་དྲག': 'གྱིས'}
        ladon = {'ག': 'ཏུ', 'བ': 'ཏུ', 'ང': 'དུ', 'ད': 'དུ', 'ན': 'དུ', 'མ': 'དུ', 'ར': 'དུ', 'ལ': 'དུ', 'འ': 'རུ',
                 'ས': 'སུ', 'མཐའ་མེད': 'རུ', 'ད་དྲག': 'ཏུ'}
        lhakce = {'ན': 'ཏེ', 'ར': 'ཏེ', 'ལ': 'ཏེ', 'ས': 'ཏེ', 'ད': 'དེ', 'ག': 'སྟེ', 'ང': 'སྟེ', 'བ': 'སྟེ', 'མ': 'སྟེ',
                  'འ': 'སྟེ', 'མཐའ་མེད': 'སྟེ', 'ད་དྲག': 'ཏེ'}
        gyendu = {'ག': 'ཀྱང', 'ད': 'ཀྱང', 'བ': 'ཀྱང', 'ས': 'ཀྱང', 'འ': 'ཡང', 'ང': 'ཡང', 'ན': 'ཡང', 'མ': 'ཡང',
                  'ར': 'ཡང', 'ལ': 'ཡང', 'མཐའ་མེད': 'ཡང', 'ད་དྲག': 'ཀྱང'}
        jedu = {'ག': 'གམ', 'ང': 'ངམ', 'ད་དྲག': 'ཏམ', 'ད': 'དམ', 'ན': 'ནམ', 'བ': 'བམ', 'མ': 'མམ', 'འ': 'འམ', 'ར': 'རམ',
                'ལ': 'ལམ', 'ས': 'སམ', 'མཐའ་མེད': 'འམ'}
        dagdra_pa = {'ག': 'པ', 'ད': 'པ', 'བ': 'པ', 'ས': 'པ', 'ན': 'པ', 'མ': 'པ', 'ང': 'བ', 'འ': 'བ', 'ར': 'བ', 'ལ': 'བ',
                     'མཐའ་མེད': 'བ', 'ད་དྲག': 'པ'}
        dagdra_po = {'ག': 'པོ', 'ད': 'པོ', 'བ': 'པོ', 'ས': 'པོ', 'ན': 'པོ', 'མ': 'པོ', 'ང': 'བོ', 'འ': 'བོ', 'ར': 'བོ',
                     'ལ': 'བོ', 'མཐའ་མེད': 'བོ', 'ད་དྲག': 'པོ'}
        lardu = {'ག': 'གོ', 'ང': 'ངོ', 'ད': 'དོ', 'ན': 'ནོ', 'བ': 'བོ', 'མ': 'མོ', 'འ': 'འོ', 'ར': 'རོ', 'ལ': 'ལོ',
                 'ས': 'སོ', 'མཐའ་མེད': 'འོ', 'ད་དྲག': 'ཏོ'}
        cing = {'ག': 'ཅིང', 'ད': 'ཅིང', 'བ': 'ཅིང', 'ང': 'ཞིང', 'ན': 'ཞིང', 'མ': 'ཞིང', 'འ': 'ཞིང', 'ར': 'ཞིང',
                'ལ': 'ཞིང', 'ས': 'ཤིང', 'མཐའ་མེད': 'ཞིང', 'ད་དྲག': 'ཅིང'}
        ces = {'ག': 'ཅེས', 'ད': 'ཅེས', 'བ': 'ཅེས', 'ང': 'ཞེས', 'ན': 'ཞེས', 'མ': 'ཞེས', 'འ': 'ཞེས', 'ར': 'ཞེས',
               'ལ': 'ཞེས', 'ས': 'ཞེས', 'མཐའ་མེད': 'ཞེས', 'ད་དྲག': 'ཅེས'}
        ceo = {'ག': 'ཅེའོ', 'ད': 'ཅེའོ', 'བ': 'ཅེའོ', 'ང': 'ཞེའོ', 'ན': 'ཞེའོ', 'མ': 'ཞེའོ', 'འ': 'ཞེའོ', 'ར': 'ཞེའོ',
               'ལ': 'ཞེའོ', 'ས': 'ཤེའོ', 'མཐའ་མེད': 'ཞེའོ', 'ད་དྲག': 'ཅེའོ',}
        cena = {'ག': 'ཅེ་ན', 'ད': 'ཅེ་ན', 'བ': 'ཅེ་ན', 'ང': 'ཞེ་ན', 'ན': 'ཞེ་ན', 'མ': 'ཞེ་ན', 'འ': 'ཞེ་ན', 'ར': 'ཞེ་ན',
                'ལ': 'ཞེ་ན', 'ས': 'ཤེ་ན', 'མཐའ་མེད': 'ཞེ་ན', 'ད་དྲག': 'ཅེ་ན'}
        cig = {'ག': 'ཅིག', 'ད': 'ཅིག', 'བ': 'ཅིག', 'ང': 'ཞིག', 'ན': 'ཞིག', 'མ': 'ཞིག', 'འ': 'ཞིག', 'ར': 'ཞིག',
               'ལ': 'ཞིག', 'ས': 'ཤིག', 'མཐའ་མེད': 'ཞིག', 'ད་དྲག': 'ཅིག',}
        # mostly for modern spoken Tibetan. in accord with Esukhia’s decision to make the agreement for this "new" particle
        gin = {'ད': 'ཀྱིན', 'བ': 'ཀྱིན', 'ས': 'ཀྱིན', 'ག': 'གིན', 'ང': 'གིན', 'ན': 'གྱིན', 'མ': 'གྱིན', 'ར': 'གྱིན',
               'ལ': 'གྱིན', 'ད་དྲག': 'ཀྱིན'}
        cases = [(["གི", "ཀྱི", "གྱི", "ཡི"], dreldra), (["གིས", "ཀྱིས", "གྱིས", "ཡིས"], jedra),
                 (["སུ", "ཏུ", "དུ", "རུ"], ladon), (["སྟེ", "ཏེ", "དེ"], lhakce), (["ཀྱང", "ཡང", "འང"], gyendu),
                 (["གམ", "ངམ", "དམ", "ནམ", "བམ", "མམ", "འམ", "རམ", "ལམ", "སམ", "ཏམ"], jedu), (["པ", "བ"], dagdra_pa),
                 (["པོ", "བོ"], dagdra_po), (["གོ", "ངོ", "དོ", "ནོ", "བོ", "མོ", "འོ", "རོ", "ལོ", "སོ", "ཏོ"], lardu),
                 (["ཅིང", "ཤིང", "ཞིང"], cing), (["ཅེས", "ཞེས"], ces), (["ཅེའོ", "ཤེའོ", "ཞེའོ"], ceo),
                 (["ཅེ་ན", "ཤེ་ན", "ཞེ་ན"], cena), (["ཅིག", "ཤིག", "ཞིག"], cig), (['ཀྱིན', 'གིན', 'གྱིན'], gin)]
        correction = ''
        for case in cases:
            if particle in case[0]:
                correction = case[1][final]
        return correction
    else:
        return '*' + particle

class AntTib:
    """
    Pseudo-Wylie created for use in AntConc.
    The output only contains letters for the syllables, :; for the punctuation.
    All yigos are deleted
    """

    def __init__(self):
        self.punct_beginning = ["༄", "༅", "࿓", "࿔", "༇", "༆", "༈"]
        self.punct_separators = [" ", "།", "༎", "༏", "༐", "༑", "༔"]
        self.punct_other = ["༼", "༽", "༒", "༓"]
        self.syl_punct = ["་", "༌", "ཿ"]
        self.punct_all = self.punct_beginning + self.punct_separators + self.punct_other + self.syl_punct

        # 1rst part of the syllable
        self.roots = {'ཀ': 'k', 'ཀྱ': 'ky', 'ཀྲ': 'kr', 'ཀླ': 'kl', 'ཁ': 'kh', 'ཁྱ': 'khy', 'ཁྲ': 'khr', 'ག': 'g',
                      'གཅ': 'gc', 'གཉ': 'gny', 'གཏ': 'gt', 'གཏྲ': 'gtr', 'གད': 'gd', 'གན': 'gn', 'གཙ': 'gts',
                      'གཞ': 'gzh', 'གཟ': 'gz', 'གཡ': 'gqy', 'གཤ': 'gsh', 'གས': 'gs', 'གྱ': 'gy', 'གྲ': 'gr', 'གླ': 'gl',
                      'ང': 'ng', 'ཅ': 'c', 'ཆ': 'ch', 'ཇ': 'j', 'ཉ': 'ny', 'ཏ': 't', 'ཏྲ': 'tr', 'ཐ': 'th', 'ཐྲ': 'thr',
                      'ད': 'd', 'དཀ': 'dk', 'དཀྱ': 'dky', 'དཀྲ': 'dkr', 'དཀླ': 'dkl', 'དག': 'dg', 'དགྱ': 'dgy',
                      'དགྲ': 'dgr', 'དང': 'dng', 'དཔ': 'dp', 'དཔྱ': 'dpy', 'དཔྲ': 'dpr', 'དབ': 'db', 'དབྱ': 'dby',
                      'དབྲ': 'dbr', 'དམ': 'dm', 'དམྱ': 'dmy', 'དམྲ': 'dmr', 'དྲ': 'dr', 'ན': 'n', 'པ': 'p', 'པྱ': 'py',
                      'པྲ': 'pr', 'ཕ': 'ph', 'ཕྱ': 'phy', 'ཕྲ': 'phr', 'བ': 'b', 'བཀ': 'bk', 'བཀྱ': 'bky', 'བཀྲ': 'bkr',
                      'བཀླ': 'bkl', 'བག': 'bg', 'བགྱ': 'bgy', 'བགྲ': 'bgr', 'བཅ': 'bc', 'བཏ': 'bt', 'བཏྲ': 'btr',
                      'བད': 'bd', 'བཙ': 'bts', 'བཞ': 'bzh', 'བཟ': 'bz', 'བཟླ': 'bzl', 'བརྐ': 'brk', 'བརྐྱ': 'brky',
                      'བརྒ': 'brg', 'བརྒྱ': 'brgy', 'བརྔ': 'brng', 'བརྗ': 'brj', 'བརྙ': 'brny', 'བརྟ': 'brt',
                      'བརྡ': 'brd', 'བརྣ': 'brn', 'བརྩ': 'brts', 'བརྫ': 'brdz', 'བརླ': 'brl', 'བལྟ': 'blt',
                      'བལྡ': 'bld', 'བཤ': 'bsh', 'བས': 'bs', 'བསྐ': 'bsk', 'བསྐྱ': 'bsky', 'བསྐྲ': 'bskr', 'བསྒ': 'bsg',
                      'བསྒྱ': 'bsgy', 'བསྒྲ': 'bsgr', 'བསྔ': 'bsng', 'བསྙ': 'bsny', 'བསྟ': 'bst', 'བསྡ': 'bsd',
                      'བསྣ': 'bsn', 'བསྩ': 'bsts', 'བསྲ': 'bsr', 'བསླ': 'bsl', 'བྱ': 'by', 'བྲ': 'br', 'བླ': 'bl',
                      'མ': 'm', 'མཁ': 'mkh', 'མཁྱ': 'mkhy', 'མཁྲ': 'mkhr', 'མག': 'mg', 'མགྱ': 'mgy', 'མགྲ': 'mgr',
                      'མང': 'mng', 'མཆ': 'mch', 'མཇ': 'mj', 'མཉ': 'mny', 'མཐ': 'mth', 'མད': 'md', 'མན': 'mn',
                      'མཚ': 'mtsh', 'མཛ': 'mdz', 'མྱ': 'my', 'མྲ': 'mr', 'ཙ': 'ts', 'ཚ': 'tsh', 'ཛ': 'dz', 'ཝ': 'w',
                      'ཞ': 'zh', 'ཟ': 'z', 'ཟླ': 'zl', 'འ': 'v', 'འཁ': 'vkh', 'འཁྱ': 'vkhy', 'འཁྲ': 'vkhr', 'འག': 'vg',
                      'འགྱ': 'vgy', 'འགྲ': 'vgr', 'འཆ': 'vch', 'འཇ': 'vj', 'འཐ': 'vth', 'འད': 'vd', 'འདྲ': 'vdr',
                      'འཕ': 'vph', 'འཕྱ': 'vphy', 'འཕྲ': 'vphr', 'འབ': 'vb', 'འབྱ': 'vby', 'འབྲ': 'vbr', 'འཚ': 'vtsh',
                      'འཛ': 'vdz', 'ཡ': 'y', 'ར': 'r', 'རྐ': 'rk', 'རྐྱ': 'rky', 'རྒ': 'rg', 'རྒྱ': 'rgy', 'རྔ': 'rng',
                      'རྗ': 'rj', 'རྙ': 'rny', 'རྟ': 'rt', 'རྡ': 'rd', 'རྣ': 'rn', 'རྦ': 'rb', 'རྨ': 'rm', 'རྨྱ': 'rmy',
                      'རྩ': 'rts', 'རྫ': 'rdz', 'རླ': 'rl', 'ལ': 'l', 'ལྐ': 'lk', 'ལྒ': 'lg', 'ལྔ': 'lng', 'ལྕ': 'lc',
                      'ལྗ': 'lj', 'ལྟ': 'lt', 'ལྡ': 'ld', 'ལྤ': 'lp', 'ལྦ': 'lb', 'ལྷ': 'lh', 'ཤ': 'sh', 'ས': 's',
                      'སྐ': 'sk', 'སྐྱ': 'sky', 'སྐྲ': 'skr', 'སྒ': 'sg', 'སྒྱ': 'sgy', 'སྒྲ': 'sgr', 'སྔ': 'sng',
                      'སྙ': 'sny', 'སྟ': 'st', 'སྡ': 'sd', 'སྣ': 'sn', 'སྣྲ': 'snr', 'སྤ': 'sp', 'སྤྱ': 'spy',
                      'སྤྲ': 'spr', 'སྦ': 'sb', 'སྦྱ': 'sby', 'སྦྲ': 'sbr', 'སྨ': 'sm', 'སྨྱ': 'smy', 'སྨྲ': 'smr',
                      'སྩ': 'sts', 'སྲ': 'sr', 'སླ': 'sl', 'ཧ': 'h', 'ཧྲ': 'hr', 'ཨ': 'A'}
        self.rareC = {'བེའུ': 'bevu', 'ཧུའུ': 'huvu', 'ཀིའུ': 'kivu', 'བྲའོ': 'bravo', 'སླེའུ': 'slevu',
                      'འགོའུ': 'vgovu', 'ཁྱེའུ': 'khyevu', 'མདེའུ': 'mdevu', 'རྔེའུ': 'rngevu', 'ཚུའུ': 'tshuvu',
                      'གཅེའུ': 'gcevu', 'རྟའུ': 'rtavu', 'ཁྱིའུ': 'khyivu', 'ཐེའུ': 'thevu', 'སྟེའུ': 'stevu',
                      'རྩེའུ': 'rtsevu', 'སླེའོ': 'slevo', 'ཤའུ': 'shavu', 'ཉེའུ': 'nyevu', 'སྨེའུ': 'smevu',
                      'རྟེའུ': 'rtevu', 'ཚའུ': 'tshavu', 'ཙེའུ': 'tsevu', 'གཡིའུ': 'g.yivu', 'སྤྲེའུ': 'sprevu',
                      'ལོའུ': 'lovu', 'གྲིའུ': 'grivu', 'སྤྱིའུ': 'spyivu', 'འབེའུ': 'bevu', 'གླེའུ': 'glevu',
                      'ལའུ': 'lavu', 'སྙེའུ': 'snyevu', 'ཕེའུ': 'phevu', 'རྡེའུ': 'rdevu', 'ཀྲུའུ': 'kruvu',
                      'ཁྲིའུ': 'khrivu', 'བྲེའུ': 'brevu', 'རྨེའུ': 'rmevu', 'གཏེའུ': 'gtevu', 'སྣེའུ': 'snevu',
                      'ཕྲའུ': 'phravu', 'དྲེའུ': 'drevu', 'སྡེའུ': 'sdevu', 'ནོའུ': 'novu', 'ཟེའུ': 'zevu',
                      'མིའུ': 'mivu', 'ཁེའུ': 'khevu', 'རྫེའུ': 'rdzevu', 'གཙེའུ': 'gtsevu', 'མཐེའུ': 'mthevu',
                      'མོའུ': 'movu', 'ཀེའུ': 'kevu', 'སྤའུ': 'spavu', 'དེའུ': 'devu', 'ཧེའུ': 'hevu',
                      'ཕྲེའུ': 'phrevu', 'ཚེའུ': 'tshevu', 'རྒེའུ': 'rgevu', 'བྲོའུ': 'brovu', 'བྱའུ': 'byavu',
                      'ཏེའུ': 'tevu', 'ཀོའུ': 'kovu', 'རེའུ': 'revu', 'ལིའུ': 'livu', 'ཡེའུ': 'yevu', 'མུའུ': 'muvu',
                      'སྒྲེའུ': 'sgrevu', 'ཁྲུའུ': 'khruvu', 'ལེའུ': 'levu', 'བྱེའུ': 'byevu', 'བྱིའུ': 'byivu',
                      'བྲའུ': 'bravu', 'འཕེའུ': 'phevu', 'གཅིའུ': 'gcivu', 'མཚེའུ': 'mtshevu', 'སྦྲེའུ': 'sbrevu',
                      'འགིའུ': 'givu', 'སྔེའུ': 'sngevu', 'ནེའུ': 'nevu', 'རྫིའུ': 'rdzivu', 'རྗེའུ': 'rjevu',
                      'སེའུ': 'sevu', 'ཐིའུ': 'thivu', 'སྒའུ': 'sgavu', 'སིའུ': 'sivu', 'མྱིའུ': 'myivu',
                      'ཙིའུ': 'tsivu', 'སྲིའུ': 'srivu', 'ནའུ': 'navu', 'བསེའུ': 'bsevu', 'གའུ': 'gavu',
                      'སྒེའུ': 'sgevu', 'ཀའུ': 'kavu', 'གྲེའུ': 'grevu', 'ཁྲེའུ': 'khrevu', 'སྤེའུ': 'spevu',
                      'སྒྱེའུ': 'sgyevu', 'དཔེའུ': 'dpevu', 'ཧྲུའུ': 'hruvu', 'ཐོའུ': 'thovu', 'ཤེའུ': 'shevu',
                      'ཐུའུ': 'thuvu', 'གཞུའུ': 'gzhuvu', 'དུའུ': 'duvu', 'ལྕེའུ': 'lcevu'}
        self.wazurC = {'སྟྭ': 'stw', 'གྭ': 'gw', 'ཞྭ': 'zhw', 'ཁྭ': 'khw', 'དྲྭ': 'drw', 'ཀྭའི': 'kwavi',
                       'བསྭོ': 'bswo', 'དྭ': 'dw', 'རྭ': 'rw', 'སྭ': 'sw', 'ཤྭ': 'shw', 'ཧྭ': 'hw', 'ལྭ': 'lw',
                       'ཕྱྭ': 'phyw', 'ཟྭ': 'zw', 'ཀྭ': 'kw', 'དྭོ': 'dwo', 'ཉྭ': 'nyw', 'ཚྭ': 'tshw', 'རྩྭ': 'rtsw',
                       'བསྭ': 'bsw', 'གྲྭ': 'grw'}
        self.A = {**self.roots, **self.rareC, **self.wazurC}
        # second part of the syllable
        self.NB = {'ག': 'ag', 'གས': 'ags', 'ང': 'ang', 'ངས': 'angs', 'ད': 'ad', 'ན': 'an', 'བ': 'ab', 'བས': 'abs',
                   'མ': 'am', 'མས': 'ams', 'འ': 'av', 'འང': 'avang', 'འམ': 'avam', 'འི': 'avi', 'འོ': 'avo', 'ར': 'ar',
                   'ལ': 'al', 'ས': 'as', 'ི': 'i', 'ིག': 'ig', 'ིགས': 'igs', 'ིང': 'ing', 'ིངས': 'ings', 'ིད': 'id',
                   'ིན': 'in', 'ིབ': 'ib', 'ིབས': 'ibs', 'ིམ': 'im', 'ིམས': 'ims', 'ིའང': 'ivang', 'ིའམ': 'ivam',
                   'ིའི': 'ivi', 'ིའོ': 'ivo', 'ིར': 'ir', 'ིལ': 'il', 'ིས': 'is', 'ུ': 'u', 'ུག': 'ug', 'ུགས': 'ugs',
                   'ུང': 'ung', 'ུངས': 'ungs', 'ུད': 'ud', 'ུན': 'un', 'ུབ': 'ub', 'ུབས': 'ubs', 'ུམ': 'um',
                   'ུམས': 'ums', 'ུའང': 'uvang', 'ུའམ': 'uvam', 'ུའི': 'uvi', 'ུའོ': 'uvo', 'ུར': 'ur', 'ུལ': 'ul',
                   'ུས': 'us', 'ེ': 'e', 'ེག': 'eg', 'ེགས': 'egs', 'ེང': 'eng', 'ེངས': 'engs', 'ེད': 'ed', 'ེན': 'en',
                   'ེབ': 'eb', 'ེབས': 'ebs', 'ེམ': 'em', 'ེམས': 'ems', 'ེའང': 'evang', 'ེའམ': 'evam', 'ེའི': 'evi',
                   'ེའོ': 'evo', 'ེར': 'er', 'ེལ': 'el', 'ེས': 'es', 'ོ': 'o', 'ོག': 'og', 'ོགས': 'ogs', 'ོང': 'ong',
                   'ོངས': 'ongs', 'ོད': 'od', 'ོན': 'on', 'ོབ': 'ob', 'ོབས': 'obs', 'ོམ': 'om', 'ོམས': 'oms',
                   'ོའང': 'ovang', 'ོའམ': 'ovam', 'ོའི': 'ovi', 'ོའོ': 'ovo', 'ོར': 'or', 'ོལ': 'ol', 'ོས': 'os'}
        # exceptions
        self.special = {'བགླ': 'bgla', 'མདྲོན': 'mdron', 'བརྡའ': 'brdav', 'བརྟའ': 'brtav'}
        self.wazur = {'ཧྭག': 'hwag', 'ཀྭས': 'kwas', 'ཁྭངས': 'khwangs', 'ཧྭང': 'hwang', 'ཀྭན': 'kwan', 'དྭགས': 'dwags',
                      'ཧྭགས': 'hwags', 'དྭངས': 'dwangs', 'ཏྭོན': 'twon'}
        self.exceptions = {**self.special, **self.wazur}
        # inversed lists
        self.C = {v: k for k, v in self.A.items()}
        self.D = {v: k for k, v in self.NB.items()}
        self.E = {v: k for k, v in self.exceptions.items()}

    def to_ant_syl(self, components):
        """

        :param components: the tuple outputed by SylComponents().get_parts(<syl>)
        :return: the AntTib of that syllable
        """
        if type(components) == 'list' or not components:
            return '***'
        else:
            part1 = components[0]
            part2 = components[1]
            if part1 not in self.A and part1 not in self.exceptions:
                return '***'
            else:
                # first part of the syllable
                if part1 in self.exceptions:
                    a = self.exceptions[part1]
                else:
                    a = self.A[part1]
                # second part of the syllable
                b = ''
                if part2 == '':
                    b = 'a'
                elif part2 != 'x':
                    b = self.NB[part2]
                return a + b

    def from_ant_syl(self, syl):
        """

        :param syl: takes as input a AntTib syllable
        :return: its Tibetan unicode counterpart
        """
        if syl == '***':
            return '***'
        else:
            a = ''
            if syl in self.E:
                return self.E[syl]
            elif syl in self.C:
                return self.C[syl]
            else:
                i = len(syl) - 1
                while i >= 0:
                    if syl[:i] in self.C:
                        a = syl[:i]
                        break
                    i -= 1
            b = syl[len(a):]
            if b.startswith('v') or b.startswith('r') or b.startswith('l') or b.startswith('s'):
                b = 'a' + b
            if b == 'a':
                return self.C[a]
            else:
                return self.C[a] + self.D[b]

    def __is_punct(self, string):
        if '།' in string or '༎' in string or '༏' in string or '༐' in string or '༑' in string or '༔' in string or ';' in string or ':' in string:
            return True
        else:
            return False

    def __trim_punct(self, l):
        """
        :param l:    a list splitted on the punctuation with re.split() where the regex was
                        something like ((<punct>|<punct>)+)
        :return: the same list, only keeping one of the two punctuation elements re.split() gave
        """
        i = 0
        while i < len(l) - 1:
            if self.__is_punct(l[i]) and self.__is_punct(l[i + 1]):
                del l[i + 1]
            i = i + 1

    def to_ant_text(self, string):
        """

        :param string: a Tibetan text string
        :return: its counterpart in AntTib with the punctuation diminished to shads(;) and tershe(:)
        """
        # Todo : make a new class to deal with the punctuation instead of doing it here
        # Prepare the string : delete all extra punctuations
        # replace the tabs by normal spaces
        string = string.replace('   ', ' ')
        # replace all non-breaking tsek by a normal tsek
        string = string.replace('༌', '་')
        # delete all yigos
        string = re.sub('(༄༅+|༆|༇|༈)།?༎? ?།?༎?', '', string)
        # split on the punctuation. here, a paragraph is just a chunk of text separated by shads.

        # split on remaining punctuation
        paragraphs = re.split(r'(( *། *| *༎ *| *༏ *| *༐ *| *༑ *| *༔ *)+)', string)
        # trim the extra punctuation
        self.__trim_punct(paragraphs)
        strip_list(paragraphs)  # delete empty elements beginning or ending the list

        # replace all shads by a ';' and the tershe by a ':'
        for num, element in enumerate(paragraphs):
            if '།' in element or '༏' in element or '༐' in element or '༑' in element:
                paragraphs[num] = element.replace('།', ';').replace('༎', ';').replace('༏', ';').replace('༐',
                                                                                                        ';').replace(
                        '༑', ';')
            elif '༎' in element:
                paragraphs[num] = element.replace('༎', ';;')
            elif '༔' in element:
                paragraphs[num] = element.replace('༔', ':')

        # translate the syllables into pseudo-wylie
        parts = SylComponents()  # instantiate object
        ant_text = []
        for par in paragraphs:
            if ';' not in par and ':' not in par:
                par = re.sub(r'([^་]) ', r'\1-',
                             par)  # adds a - everywhere a space is not preceded by a tsek to find the merged particles
                par = re.sub(r'་$', '', par.replace('་ ', ' '))  # delete all tsek at the end of words
                ant_par = []
                words = par.split(' ')
                for word in words:
                    syls = word.split('་')
                    ant_word = []
                    for syl in syls:
                        # deals with the fusioned particles like མཐར་ that have become མཐའ ར་. we want to see 'mthav r'
                        # it is a bit of a hack because I already add a space instead of doing it with ' '.join()
                        if '-' in syl:
                            if syl.startswith(mark):
                                psyl = syl[1:].split('-')
                                ant_word.append(
                                        mark + self.to_ant_syl(parts.get_parts(psyl[0])) + ' ' + self.to_ant_syl(
                                                parts.get_parts(psyl[1])).replace('a', ''))
                            else:
                                psyl = syl.split('-')
                                ant_word.append(self.to_ant_syl(parts.get_parts(psyl[0])) + ' ' + self.to_ant_syl(
                                        parts.get_parts(psyl[1])).replace('a', ''))
                        else:
                            if syl.startswith(mark):
                                ant_word.append(mark + self.to_ant_syl(parts.get_parts(syl[1:])))
                            else:
                                ant_word.append(self.to_ant_syl(parts.get_parts(syl)))
                    ant_par.append('x'.join(ant_word))
                ant_text.append(' '.join(ant_par))
            else:
                ant_text.append(par)
        return ''.join(ant_text)

    def from_ant_text(self, string):
        """

        :param string: an AntTib string
        :return: its counterpart in Tibetan unicode
        """
        paragraphs = re.split(r'(( *; *| *: *)+)', string)
        # delete the last element of the list if it is an empty string
        strip_list(paragraphs)
        # trim the extra punctuation (see comment in to_pw_text)
        self.__trim_punct(paragraphs)
        ant_text = []
        for par in paragraphs:
            if ';' not in par and ':' not in par:
                ant_par = []
                par = re.sub(r' (r|s|vi|vo) ', r'-\1 ', par)
                words = par.split(' ')
                for word in words:
                    syls = word.split('x')
                    ant_word = []
                    for syl in syls:
                        # deals with the fusioned particles
                        # is a similar hack as for the previous function
                        if '-' in syl:
                            if syl.startswith(mark):
                                psyl = syl[1:].split('-')
                                ant_word.append(mark + self.from_ant_syl(psyl[0]) + ' ' + self.from_ant_syl(psyl[1]))
                            else:
                                psyl = syl.split('-')
                                ant_word.append(self.from_ant_syl(psyl[0]) + ' ' + self.from_ant_syl(psyl[1]))
                        else:
                            if syl.startswith(mark):
                                ant_word.append(mark + self.from_ant_syl(syl[1:]))
                            else:
                                ant_word.append(self.from_ant_syl(syl))
                    ant_par.append('་'.join(ant_word) + '་')
                ant_text.append(' '.join(ant_par))
            else:
                ant_text.append(par.replace(';', '།').replace(':', '༔'))
        ant_text = ''.join(ant_text)
        ant_text = re.sub(r'([^ང])་([༔།])', r'\1\2', ant_text)
        return ant_text

    def no_space(self, string):
        """

        :param string: a segmented Tibetan unicode string
        :return: the same string without the spaces between syllables (keeps all spaces at punctuation)
        """
        regexes = [r'([་|༌])\s',  # spaces preceded by a tsek
                   r'(ང[་|༌])\s',  # ང་ plus space
                   r'\s(ར)',  #
                   r'\s(ས)',
                   r'\s(འི)',
                   r'\s(འོ)']
        for regex in regexes:
            string = re.sub(regex, r'\1', string)
        return string
