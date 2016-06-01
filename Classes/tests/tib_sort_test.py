import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PYTib import common


with open('../PYTib/data/uncompound_lexicon.txt', 'r', -1, 'utf-8-sig') as f:
    content = [line.strip() for line in f.readlines()]

with open('./files/lexicon.txt', 'w', -1, 'utf-8-sig') as f:
    f.write('\n'.join(common.tib_sort(content)))