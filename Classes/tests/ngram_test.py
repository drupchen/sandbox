import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
import time
import Levenshtein
from collections import defaultdict
from PyTib import Segment
from PyTib.common import write_file, open_file, tib_sort
from PyTib.NGrams import text2ngram


def no_trailing_tsek(string):
    if string.endswith('་'):
        return string[:-1]
    else:
        return string

def no_punct(string):
    punct = ['༄', '༅', '།', '་', '༌', '༑', '༎', '༏', '༐', '༔', '_']
    for p in punct:
        string = string.replace(p, '')
    return string

def ngram_minimal_pairs(orig_list, ngram_list, similarity=72):
    matches = {}
    for n_gram in ngram_list:
        orig_ngram = n_gram[-1]+' '+''.join(n_gram[:-1])
        print(orig_ngram)
        matches[orig_ngram] = defaultdict(int)
        ngram_indexes = [a for a in range(len(n_gram)-1)]
        hollowed_ngram_indexes = [(j, [a for a in ngram_indexes if a != j]) for j in ngram_indexes]
        for i in range(len(orig_list)-1):
            for h in hollowed_ngram_indexes:
                hole = h[0]
                if i + hole <= len(orig_list) - 1:
                    hole_syl_orig = no_trailing_tsek(orig_list[i + hole])
                    hole_syl_ngram = no_trailing_tsek(n_gram[hole])
                    lev_index = Levenshtein.jaro_winkler(hole_syl_orig, hole_syl_ngram)*100
                    if lev_index < 100 and lev_index >= similarity and no_punct(hole_syl_ngram) != no_punct(hole_syl_orig):
                        hollowed_orig_slice = ''.join([orig_list[i + j] for j in h[1] if i + j <= len(orig_list) - 1])
                        hollowed_ngram_list = ''.join([n_gram[j] for j in h[1]])
                        if no_trailing_tsek(hollowed_orig_slice) == no_trailing_tsek(hollowed_ngram_list):
                            matches[orig_ngram][''.join(orig_list[i:i + len(n_gram)-1])] += 1
    # formatting
    output = ''
    for t in sorted(matches, reverse=True):
        if matches[t]:
            output += t + '\n'
            for occ in tib_sort(matches[t]):
                output += '\t'+occ+'\t'+str(matches[t][occ])+'\n'
            output += '\n'
    return output

#raw_string = open_file('/home/drupchen/PycharmProjects/nalanda_corpus/gyu_raw/རྒྱུད། པུ།.txt').replace('\n', '')
#syls = Segment().segment(raw_string.replace('༌', '་'), ant_segment=1, unknown=0, space_at_punct=True)
#write_file('syls_seperated.txt', ''.join(syls))

original = open_file('./syls_seperated.txt').split(' ')
ngrams = [a.split(' ') for a in open_file('./reduced_algo3.txt').split('\n')]
ngrams = sorted(ngrams, key=lambda x: x[-1], reverse=True)[:100]
A = time.time()
write_file('test.txt', ngram_minimal_pairs(original, ngrams, similarity=72).replace('_', ' '))
B = time.time()
print(B-A)
