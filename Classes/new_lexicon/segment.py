import os
import re
from PyTib import Segment, common, Concordance

punct_regex = r'([༄༅༆༇༈།༎༏༐༑༔\[\]\(\)\s]+)'

# open file
with open('ཤེར་ཕྱིན། ཀ.txt', 'r', -1, 'utf-8-sig') as f:
    content = f.read().replace('༌', '་')  # replace non-breaking tsek

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
            if '#' in syl:
                if syl.endswith('་'):
                    syl = syl[:-1]
                stars.append(syl)
    f.write('\n'.join(sorted(list(set(stars)))))

# write new file
with open('segmented.txt', 'w', -1, 'utf-8-sig') as f:
    for o in out:
        if re.match(r'([༄༅༆༇༈།༎༏༐༑༔\s]+)', o):
            f.write(o+'\n')
        else:
            f.write(o)

with open('conc.txt', 'w', -1, 'utf-8-sig') as f:
    with open('/home/drupchen/PycharmProjects/sandbox/Classes/new_lexicon/segmented.txt', 'r', -1, 'utf-8-sig') as g:
        f.write(Concordance.no_tab_lexicon_concs(g.read()))