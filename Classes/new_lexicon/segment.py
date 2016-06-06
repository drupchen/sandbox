import sys
import os
import re
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PyTib import Segment, common

punct_regex = r'([༄༅༆༇༈།༎༏༐༑༔\s]+)'

# open file
with open('unsegmented.txt', 'r', -1, 'utf-8-sig') as f:
    content = f.read()

# segment on the punctuation
paragraphs = re.split(punct_regex, content)
common.strip_list(paragraphs)

# segment the texts
out = []
for par in paragraphs:
    if not re.match(punct_regex, par):
        out.append(Segment().segment(par, ant_segment=0, unknown=0))
    else:
        out.append(par)

# write new file
with open('segmented.txt', 'w', -1, 'utf-8-sig') as f:
    f.write(re.sub(r'(།? ?།)([^།])', r'\1\n\2', ''.join(out)))