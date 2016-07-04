import sys
import os
import re
import ngram
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PyTib import Segment
from PyTib.NGrams import NGrams
from PyTib.common import write_file, open_file


def no_space(string):
    for regex in [r'([་|༌])\s', r'(ང[་|༌])\s', r'\s(ར)', r'\s(ས)', r'\s(འི)', r'\s(འོ)']:
        string = re.sub(regex, r'\1', string)
    return string

import time

raw_string = open_file('files/བསྟོདཚོགས.txt').replace('\n', '')
A = time.time()
syls = Segment().segment(raw_string.replace('༌', '་'), ant_segment=1, unknown=0, space_at_punct=True).split(' ')
B = time.time()
print('segmentation :',B-A)
write_file('segmented.txt', ' '.join(syls))
ng = NGrams().no_substring_ngrams(syls, min=3, max=12, freq=10, raw_output=True)

C = time.time()
print('ngrams :', C-B)

# list in order all the sizes of ngrams that are more frequent than 10
length = sorted(list(set([a[1] for a in ng if a[1] >= 10])))
# create a set of all syllables found in the ngrams
all_syls = set([syl for a in ng for syl in a[0]])

model = ngram.NGram()
for syl in all_syls:
    model.add(syl)

out = []
for i in range(10):#range(len(raw_string)-1):
    for l in length:



D = time.time()
print('fuzzy match :', D-C)
write_file('fuzzy.txt', '\n'.join(out))
