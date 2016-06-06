import sys
import os
import re
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PyTib import Segment, common

punct_regex = r'([༄༅༆༇༈།༎༏༐༑༔\[\]\(\)\s]+)'

# open file
with open('ཤེར་ཕྱིན། ཀ.txt', 'r', -1, 'utf-8-sig') as f:
    content = f.read().replace('༌', '་')

# segment on the punctuation
paragraphs = re.split(punct_regex, content)
common.strip_list(paragraphs)

# segment the texts
out = []
for par in paragraphs:
    if not re.match(punct_regex, par):
        out.append(Segment().segment(par, ant_segment=0, unknown=1))
    else:
        out.append(par)

with open('stars.txt', 'w', -1, 'utf-8-sig') as f:
    stars = []
    for line in out:
        syls = line.split(' ')
        for syl in syls:
            if '*' in syl:
                stars.append(syl)
    f.write('\n'.join(sorted(list(set(stars)))))

# write new file
with open('segmented.txt', 'w', -1, 'utf-8-sig') as f:
    for o in out:
        if re.match(r'([༄༅༆༇༈།༎༏༐༑༔\s]+)', o):
            f.write(o+'\n')
        else:
            f.write(o)