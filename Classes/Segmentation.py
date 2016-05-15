# coding: utf-8

from bisect import bisect_left
from TibProcessing import *
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


class Segment:
    def __init__(self):
        # import the lexicon
        with open('../spellcheck/tsikchen.txt', 'r', -1, 'utf-8-sig') as f:
            self.lexicon = [line.strip() for line in f.readlines()]
        # add all the particles
        self.lexicon.extend(
                ['གི', 'ཀྱི', 'གྱི', 'ཡི', 'གིས', 'ཀྱིས', 'གྱིས', 'ཡིས', 'སུ', 'ཏུ', 'དུ', 'རུ', 'སྟེ', 'ཏེ', 'དེ',
                 'ཀྱང', 'ཡང', 'འང', 'གམ', 'ངམ', 'དམ', 'ནམ', 'བམ', 'མམ', 'འམ', 'རམ', 'ལམ', 'སམ', 'ཏམ', 'གོ', 'ངོ', 'དོ',
                 'ནོ', 'མོ', 'འོ', 'རོ', 'ལོ', 'སོ', 'ཏོ', 'ཅིང', 'ཅེས', 'ཅེའོ', 'ཅེ་ན', 'ཅིག', 'ཞིང', 'ཞེས', 'ཞེའོ',
                 'ཞེ་ན', 'ཞིག', 'ཤིང', 'ཤེའོ', 'ཤེ་ན', 'ཤིག', 'ལ', 'ན', 'ནས', 'ལས', 'ནི', 'དང', 'གང', 'ཅི', 'ཇི', 'གིན',
                 'གྱིན', 'ཀྱིན', 'ཡིན', 'པ', 'བ', 'པོ', 'བོ'])
        # add all Monlam verbs
        with open('../spellcheck/monlam1_verbs.txt', 'r', -1, 'utf-8-sig') as f:
            monlam_verbs = [line.strip() for line in f.readlines()]
        for entry in monlam_verbs:
            verb = entry.split(' | ')[0]
            if verb not in self.lexicon:
                self.lexicon.append(verb)

        self.merged_part = r'(ར|ས|འི|འམ|འང|འོ)$'
        self.punct_regex = r'([༄༅༆༇༈།༎༏༐༑༔\s]+)'

        # for bisect
        self.lexicon = sorted(self.lexicon)
        self.len_lexicon = len(self.lexicon)

        self.n = 0  # counter needed between methods segment() and __process()

    def is_word(self, maybe):
        final = False
        if search(self.lexicon, maybe, self.len_lexicon):
            final = True
        elif search(self.lexicon, re.sub(self.merged_part, '', maybe), self.len_lexicon):
            final = True
        else:
            if '་' in maybe:
                last_syl = maybe.split('་')[-1]
                if SylComponents().get_info(last_syl) == 'thame':
                    maybe = re.sub(self.merged_part, '', maybe) + 'འ'
            else:
                if SylComponents().get_info(maybe) == 'thame':
                    maybe = re.sub(self.merged_part, '', maybe) + 'འ'
            if search(self.lexicon, maybe, self.len_lexicon):
                final = True
        return final

    def __process(self, list1, list2, num):
        word = '་'.join(list1[self.n:self.n + num])
        if not search(self.lexicon, word, self.len_lexicon):
            maybe = re.split(self.merged_part, word)
            if not search(self.lexicon, maybe[0], self.len_lexicon):
                if search(self.lexicon, maybe[0] + 'འ', self.len_lexicon):
                    list2.append(maybe[0] + 'འ')
                else:
                    list2.append(maybe[0])
            else:
                list2.append(maybe[0])
            list2.append(maybe[1] + '་')
            # del list1[:num]
            self.n = self.n + num
        else:
            list2.append(word + "་")
            # del list1[:num]
            self.n = self.n + num

    def segment(self, string, ant_segment, unknown):
        """

        :param string: takes a unicode text file as input
        :param ant_segment: 0, segments normally. 1, separates the merged particles from their syllables
        :param unknown: 0, adds nothing. 1, adds character in variable mark to unknown words/syllables
        :return: outputs the segmented text
        """
        paragraphs = re.split(self.punct_regex, string)
        strip_list(paragraphs)

        text = []
        for par in paragraphs:
            words = []
            if not re.match(self.punct_regex, par):
                syls = par.split('་')
                strip_list(syls)

                self.n = 0
                while self.n < len(syls):
                    if len(syls[self.n:self.n + 3]) == 3 and self.is_word('་'.join(syls[self.n:self.n + 3])):
                        self.__process(syls, words, 3)
                    elif len(syls[self.n:self.n + 2]) == 2 and self.is_word('་'.join(syls[self.n:self.n + 2])):
                        self.__process(syls, words, 2)
                    elif len(syls[self.n:self.n + 1]) == 1 and self.is_word('་'.join(syls[self.n:self.n + 1])):
                        self.__process(syls, words, 1)
                    else:
                        if unknown == 0:
                            words.append('་'.join(syls[self.n:self.n + 1]) + '་')
                        elif unknown == 1:
                            words.append(mark + '་'.join(syls[self.n:self.n + 1]) + '་')
                        self.n += 1
                paragraph = ' '.join(words)
                if not paragraph.endswith('ང་'):
                    paragraph = paragraph[:-1]
                #########
                # add spaces at all tseks
                if ant_segment == 1:
                    paragraph = re.sub(r'་([^ ])', r'་ \1', paragraph)
                #
                #########
                text.append(paragraph)
            else:
                text.append(par)
        #
        ######################
        return ''.join(text)


def main():
    import os
    for file in os.listdir("../IN/"):
        with open('../IN/' + file, 'r', -1, 'utf-8-sig') as f:
            current_file = f.read().replace('༌', '་').replace('\r\n', '\n').replace('\r', '\n')
            current_file = current_file.split('\n')

        seg = Segment()
        text = []
        for line in current_file:
            if line == '':
                text.append(line)
            else:
                text.append(seg.segment(line, ant_segment=0, unknown=1))

        ######################
        # Transpose to AntTib
        # text = AntTib().to_ant_text(text)
        #
        ######################

        # write output
        with open('../' + 'anttib_' + file, 'w', -1, 'utf-8-sig') as f:
            f.write('\n'.join(text))

if __name__ == '__main__':
    main()
