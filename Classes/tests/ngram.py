import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PyTib import Segment
from PyTib.NGrams import NGrams
from PyTib.common import pre_process, DefaultOrderedDict, write_file, open_file

import re
def no_space(string):
    for regex in [r'([་|༌])\s', r'(ང[་|༌])\s', r'\s(ར)', r'\s(ས)', r'\s(འི)', r'\s(འོ)']:
        string = re.sub(regex, r'\1', string)
    return string


string = open_file('/home/drupchen/PycharmProjects/sandbox/Classes/tests/files/བསྟོད་ཚོགས། ཀ.txt').replace('\n', '')
string = Segment().segment(string.replace('༌', '་'), ant_segment=1, unknown=0).split(' ')
ng = NGrams().no_substring_ngrams(string, min=3, max=12, freq=2)
write_file('filtered.txt', ng)


import nltk
