import sys
import os
import re
import ngram
import time
import tempfile
from collections import defaultdict
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PyTib import Segment
from PyTib.common import write_file, open_file
from PyTib.NGrams import text2ngram


def ngram_minimal_pairs(orig_list, ngram_list):
    matches = {}
    for n_gram in ngram_list:
        matches[''.join(n_gram)] = defaultdict(int)
        ngram_indexes = [a for a in range(len(n_gram))]
        hollowed_ngram_indexes = [(j, [a for a in ngram_indexes if a != j]) for j in ngram_indexes]
        for i in range(len(orig_list)-1):
            for h in hollowed_ngram_indexes:
                hole = h[0]
                if i+hole <= len(orig_list)-1 and orig_list[i+hole] != n_gram[hole]:
                    hollowed_orig_slice = [orig_list[i + j] for j in h[1] if i + j <= len(orig_list) - 1]
                    hollowed_ngram_list = [n_gram[j] for j in h[1]]
                    if hollowed_orig_slice == hollowed_ngram_list:
                        matches[''.join(n_gram)][''.join(orig_list[i:i + len(n_gram)])] += 1
    return matches

#raw_string = open_file('/home/drupchen/PycharmProjects/nalanda_corpus/gyu_raw/རྒྱུད། པུ།.txt').replace('\n', '')
#syls = Segment().segment(raw_string.replace('༌', '་'), ant_segment=1, unknown=0, space_at_punct=True)
#write_file('syls_seperated.txt', ''.join(syls))

original = open_file('./syls_seperated.txt').split(' ')
ngrams = [a.split(' ')[:-1] for a in open_file('./reduced_algo3.txt').split('\n')]
A = time.time()
write_file('test.txt', ngram_minimal_pairs(original, ngrams))
B = time.time()
print(B-A)

orig_list = list('abcdefgabaacaba')
ngram_list = [list('abc'), list('bad')]
test = ngram_minimal_pairs(orig_list, ngram_list)
for t in test:
    print(t)
    for occ in test[t]:
        print('\t', occ, test[t][occ])