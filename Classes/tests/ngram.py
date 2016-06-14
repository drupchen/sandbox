import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PyTib.common import DefaultOrderedDict, open_file, filewrite, PrepareTib



def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])


def ngrams_by_freq(l, freq=10, min=3, max=12):
    if min == max:
        max +=1

    ngrams = DefaultOrderedDict(int)
    for a in range(min, max):
        grams = find_ngrams(l, a)
        for g in grams:
            ngrams[g] += 1

    ngrams = sorted(ngrams.items(), key=lambda x: x[1], reverse=True)
    return [(' '.join(n[0]), n[1], len(n[0])) for n in ngrams if n[1] >= freq]



import time
A = time.time()

raw = open_file('/home/drupchen/PycharmProjects/sandbox/Classes/new_lexicon/segmented.txt')
syls = PrepareTib(raw).tsheks_only()
ngrams = ngrams_by_freq(syls, freq=2, min=20, max=20)

B = time.time()
print(B-A)

print(len(ngrams), ngrams[:100])