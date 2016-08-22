import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PyTib.NGrams import NGrams
from PyTib import Segment
from PyTib.common import write_file, open_file

raw = open_file('raw_text.txt')
# the ngrams have been selected manually
good_ngrams = open_file('ngrams_filtered.txt')

segmented = Segment().segment(raw, ant_segment=True, unknown=False, space_at_punct=True)
ngrams = NGrams().ngrams(segmented.split(' '), freq=5, min=2, max=4)

ngram_text = [a.split('\t')[1] for a in ngrams.split('\n')]
write_file('ngrams_full.txt', ngrams)

replacements = []
for num, a in enumerate(good_ngrams.split('\n')):
    replacements.append((a, str(num+1), a.replace(' ', '')))
good_ngrams = sorted(replacements, key=lambda x: len(x[0]), reverse=True)

joined = segmented
for n in good_ngrams:
    joined = joined.replace(n[0], '+'+n[2]+'+')
print('The syllables in the ngrams have been put together:')
#print(joined)

numbered = segmented
for n in good_ngrams:
    numbered = numbered.replace(n[0], n[1])
print('The ngrams have been replaced by numbers:')
#print(numbered)


numbers = [str(a) for a in range(50)]
num_structure = ['.' if a not in numbers else a for a in numbered.split(' ')]
print('All other syllables have been replaced by a dot:')
#print(' '.join(num_structure))

tib_structure = []
for a in numbered.split(' '):
    if a in numbers:
        for r in replacements:
            if a == r[1]:
                tib_structure.append(a+r[2])
    else:
        tib_structure.append('.')
print('The numbers have been replaced by their corresponding ngrams:')
#print(' '.join(tib_structure))

