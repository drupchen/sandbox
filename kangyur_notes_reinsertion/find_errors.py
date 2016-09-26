import PyTib
from PyTib.common import write_file, open_file
import yaml
import os
import re
from collections import defaultdict
path = 'output/mistakes/'
for f in os.listdir(path):
    if f == 'i-6-1 བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ།.txt':
        raw_mistakes = open_file(path+f).split('\n\n')
        for mistake in raw_mistakes:
            parts = mistake.split('\n')
            derge = [p.replace('སྡེ་༽', '') for p in parts if 'སྡེ་༽' in p][0]
            cone = [p.replace('ཅོ་༽', '') for p in parts if 'ཅོ་༽' in p][0]
            if derge != cone:
                print(mistake)
                print()
