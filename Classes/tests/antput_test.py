import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

from TibTK import AntPut

with open('../tests/files/AntPut/Level 1 - 1000 words.txt', 'r', -1, 'utf-8-sig') as f:
    content = f.read()

output = AntPut().words(content)
with open('../tests/files/words_uni.txt', 'w', -1, 'utf-8-sig') as f:
    f.write(output)