
# coding: utf-8

import re
from bisect import bisect_left
from TibProcessing import *

def search(List, entry, len_List):
    index = bisect_left(List, entry, 0, len_List)
    return(True if index != len_List and List[index] == entry else False)

class Segment:
    def __init__(self):
        # import the lexicon
        with open('../spellcheck/tsikchen.txt', 'r', -1, 'utf-8-sig') as f:
            self.lexicon = [line.strip() for line in f.readlines()]
        # add all the particles
        self.lexicon.extend(['གི', 'ཀྱི', 'གྱི', 'ཡི', 'གིས', 'ཀྱིས', 'གྱིས', 'ཡིས', 'སུ', 'ཏུ', 'དུ', 'རུ', 'སྟེ', 'ཏེ', 'དེ', 'ཀྱང', 'ཡང', 'འང', 'གམ', 'ངམ', 'དམ', 'ནམ', 'བམ', 'མམ', 'འམ', 'རམ', 'ལམ', 'སམ', 'ཏམ', 'གོ', 'ངོ', 'དོ', 'ནོ', 'མོ', 'འོ', 'རོ', 'ལོ', 'སོ', 'ཏོ', 'ཅིང', 'ཅེས', 'ཅེའོ', 'ཅེ་ན', 'ཅིག', 'ཞིང', 'ཞེས', 'ཞེའོ', 'ཞེ་ན', 'ཞིག', 'ཤིང', 'ཤེའོ', 'ཤེ་ན', 'ཤིག', 'ལ', 'ན', 'ནས', 'ལས', 'ནི', 'དང', 'གང', 'ཅི', 'ཇི', 'གིན', 'གྱིན', 'ཀྱིན', 'ཡིན', 'པ', 'བ', 'པོ', 'བོ'])
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

        # mark (1) or not (0) the unknown words/syllables
        self.mark_unknown = 0
        self.mark = '*'  # character used to mark.
        
        self.c = 0  # counter needed between methods segment() and __process()

    def isWord(self, maybe):
        final = False
        if search(self.lexicon, maybe, self.len_lexicon) == True:
            final = True
        elif search(self.lexicon, re.sub(self.merged_part, '', maybe), self.len_lexicon) == True:
            final = True
        else:
            last_syl = ''
            if '་' in maybe:
                last_syl = maybe.split('་')[-1]
                if SylComponents().get_info(last_syl) == 'thame':
                    maybe = re.sub(self.merged_part, '', maybe) + 'འ'
            else:
                if SylComponents().get_info(maybe) == 'thame':
                    maybe = re.sub(self.merged_part, '', maybe) + 'འ'
            if search(self.lexicon, maybe, self.len_lexicon) == True:
                final = True
        return final

    def __process(self, list1, list2, num):
        word = '་'.join(list1[self.c:self.c+num])
        if search(self.lexicon, word, self.len_lexicon) == False:
            maybe = re.split(self.merged_part, word)
            if search(self.lexicon, maybe[0], self.len_lexicon) == False and search(self.lexicon, maybe[0]+'འ', self.len_lexicon):
                list2.append(maybe[0]+'འ')
            else:
                list2.append(maybe[0])
            list2.append(maybe[1]+'་')
            #del list1[:num]
            self.c = self.c + num
        else:
            list2.append(word+"་")
            #del list1[:num]
            self.c = self.c + num

    def __strip_list(self, List):
        '''delete 1st and last element if equal to an empty string''' 
        first_elt = List[0]
        last_elt = List[len(List)-1]
        if first_elt == '':
            del first_elt
        if last_elt == '':
            del last_elt
            
    def segment(self, File, ant_segment):
        """

        :param File: takes a unicode text file as input
        :param ant_segment: 0, segments normally. 1, separates the merged particles from their syllables
        :return: outputs the segmented text
        """

        paragraphs = re.split(self.punct_regex, File)
        self.__strip_list(paragraphs)

        text = []
        for par in paragraphs:
            words = []
            if re.match(self.punct_regex, par) == None:
                syls = par.split('་')
                self.__strip_list(syls)
                
                self.c = 0
                while self.c < len(syls):
                    if len(syls[self.c:self.c+3]) == 3 and self.isWord('་'.join(syls[self.c:self.c+3])): self.__process(syls, words, 3)
                    elif len(syls[self.c:self.c+2]) == 2 and self.isWord('་'.join(syls[self.c:self.c+2])): self.__process(syls, words, 2)
                    elif len(syls[self.c:self.c+1]) == 1 and self.isWord('་'.join(syls[self.c:self.c+1])): self.__process(syls, words, 1)
                    else:
                        if self.mark_unknown == 0: words.append('་'.join(syls[self.c:self.c+1])+'་')
                        elif self.mark_unknown == 1: words.append(mark+'་'.join(syls[self.c:self.c+1])+'་')
                        self.c = self.c + 1
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
        if file.endswith(".txt"):
        #todo - replace \n by \s try: with open('drugs') as temp_file: \n drugs = [line.rstrip('\n') for line in temp_file]
            try:
                with open('../IN/' + file, 'r', -1, 'utf-8-sig') as f:
                    current_file = f.read().replace('\n', '').replace('\r\n', '').replace('༌', '་')

            except:
                print("Save all IN files as UTF-8 and try again.")
                #input()
        else:
            print("\nSave all IN files as text files and try again.")
            #input()

        text = Segment().segment(current_file, ant_segment=1)
        text = ''.join(text)

        ######################
        # Transpose to AntTib
        text = AntTib().to_pw_text(text)
        #
        ######################

        # write output
        with open('../' + 'anttib_' + file, 'w', -1, 'utf-8-sig') as f:
            f.write(text)

if __name__ == '__main__': main()

