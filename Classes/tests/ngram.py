import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PyTib.common import DefaultOrderedDict


with open('/home/drupchen/PycharmProjects/sandbox/Classes/new_lexicon/segmented.txt', 'r', -1, 'utf-8-sig') as f:
    seg = f.read().replace('\n', '').split()


# class TibNgram:


def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])


def ngrams_by_freq(l, freq=10, min=3, max=12):
    ngrams = DefaultOrderedDict(int)
    for a in range(min, max):
        grams = find_ngrams(l, a)
        for g in grams:
            ngrams[' '.join(g)] += 1

    ngrams = sorted(ngrams.items(), key=lambda x: x[1], reverse=True)
    return [n for n in ngrams if n[1] >= freq]


import time
A = time.time()
ngrams = ngrams_by_freq(seg)
B = time.time()
print(B-A)

print(ngrams[:100])