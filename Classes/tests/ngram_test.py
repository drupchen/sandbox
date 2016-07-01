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

raw_string = open_file('/home/drupchen/PycharmProjects/sandbox/Classes/tests/files/བསྟོད་ཚོགས། ཀ.txt').replace('\n', '')
A = time.time()
syls = Segment().segment(raw_string.replace('༌', '་'), ant_segment=1, unknown=0).split(' ')
B = time.time()
print('segmentation :',B-A)
ng = NGrams().no_substring_ngrams(syls, min=3, max=12, freq=10)
#write_file('filtered.txt', ng)
C = time.time()
print('ngrams :', C-B)

# importing the ngrams for reference
model = ngram.NGram()
length = []
for line in ng.split('\n'):
    parts = line.split('\t')
    freq = int(parts[0])
    string = parts[1]
    if freq >= 10:
        model.add(string)
        if len(string) not in length:
            length.append(len(string))

out = []
for i in range(len(raw_string)-1):
    if raw_string[i-1] in ['་', ' ', '།', '༈', '༄', '༅']:
        for l in sorted(length):
            str_slice = raw_string[i:i + l]
            result = model.search(str_slice, threshold=0.4)
            if result != [] and result[0][1] < 1:
                out.append(str_slice+'\t'+str(result[0]))
D = time.time()
print('fuzzy match :', D-C)
write_file('fuzzy.txt', '\n'.join(out))
