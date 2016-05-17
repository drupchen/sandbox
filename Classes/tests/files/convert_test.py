import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from TibProcessing import getSylComponents, Agreement, Segment

with open('.files/ant_cut_Lamrim.txt', 'r', -1, 'utf-8-sig') as f:
    content = f.readlines()

truc = AntTib