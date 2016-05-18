import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

from TibProcessing import AntPut

#with open('../tests/files/lamrim-chenmo-word-list.txt', 'r', -1, 'utf-8-sig') as f:
#    content = f.read()

#output = AntPut().keyword_list(content)
#with open('../tests/files/lamrim-word-list_uni.txt', 'w', -1, 'utf-8-sig') as f:
#    f.write(output)