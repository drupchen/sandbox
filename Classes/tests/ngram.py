import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PyTib.common import DefaultOrderedDict, open_file, write_file, PrepareTib


from itertools import tee, islice

def ngram_generator(iterable, n):
    return zip(*((islice(seq, i, None) for i, seq in enumerate(tee(iterable, n)))))


def raw_ngrams(l, min=3, max=12):
    ngrams = DefaultOrderedDict(int)
    for a in range(min, max+1):
        grams = ngram_generator(l, a)
        for g in grams:
            ngrams[g] += 1
    # removing all entries with only one occurence
    return [n for n in ngrams.items() if n[1] != 1]


def ngrams_by_freq(raw, freq=10):
    ngrams = sorted(raw.items(), key=lambda x: x[1], reverse=True)
    return [(n[1], ' '.join(n[0]), len(n[0])) for n in ngrams if n[1] >= freq]


def format_ngrams(l, sep='\t'):
    return '\n'.join([str(n[0])+sep+n[1]+sep+str(n[2]) for n in l])


def ngrams(l, freq=10, min=3, max=12):
    raw = raw_ngrams(l, min, max)
    by_freq = ngrams_by_freq(raw, freq)
    formatted = format_ngrams(by_freq)
    return formatted


import time
A = time.time()
IN = './ngram_input/'

ngram_total = DefaultOrderedDict(int)
for f in os.listdir(IN):
    raw = open_file(IN+f)
    syls = PrepareTib(raw).tsheks_only()
    ngrams = raw_ngrams(syls, min=3, max=12)
    for n in ngrams:
        ngram_total[n[0]] += n[1]
ngram_total = ngrams_by_freq(ngram_total, freq=2)
write_file('test.txt', format_ngrams(ngram_total))

B = time.time()
print(B-A)