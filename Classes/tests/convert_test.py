import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

from TibProcessing import getSylComponents, Agreement, Segment, AntTib
from TibProcessing.common import strip_list
with open('./files/བསྟོད་ཚོགས། ཀ.txt', 'r', -1, 'utf-8-sig') as f:
    content = [line.strip() for line in f.readlines()]

seg = []
for c in content:
    if c != '':
        seg.append(Segment().segment(c, ant_segment=0, unknown=1))
    else:
        seg.append(c)

ant = []
for s in seg:
    if s != '':
        ant.append(AntTib().to_ant_text(s))
    else:
        ant.append(s)

uni = []
for a in ant:
    if a != '':
        uni.append(AntTib().from_ant_text(a))
    else:
        uni.append(a)

with open('./files/uni.txt', 'w', -1, 'utf-8-sig') as f:
    f.write(uni)