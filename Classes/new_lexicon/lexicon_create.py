import sys
import os
import re
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

from PYTib import getSylComponents, Agreement, Segment, AntTib, common

with open('manual.txt', 'r', -1, 'utf-8-sig') as f:
    content = f.read().replace('\n', ' ')

string = content.replace('   ', ' ')
# replace all non-breaking tsek by a normal tshek
string = string.replace('༌', '་')
# replace multiple tsek by a single one
string = re.sub(r'་+', r'་', string)
# delete all yigos
string = re.sub('(༄༅+|༆|༇|༈)།?༎? ?།?༎?', '', string)
# split on the punctuation. here, a paragraph is just a chunk of text separated by shads.

# split on remaining punctuation
string = re.sub(r'(( *། *| *༎ *| *༏ *| *༐ *| *༑ *| *༔ *)+)', ' ', string)
string = re.sub(' +', ' ', string)

words = string.split()

# delete final tsek
for num, word in enumerate(words):
    if word.endswith('་'):
        words[num] = word[:-1]

long = []
composed = []
for entry in words:
    segmented = ''.join(Segment().segment(entry, 0, 1))
    if '*' in segmented:
        long.append(entry)
    elif ' ' in segmented:
        composed.append(segmented)

for l in set(long):
    print(l)
print()
for c in set(composed):
    print(c)
