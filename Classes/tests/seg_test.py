import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

from TibProcessing import SylComponents
print(SylComponents().get_parts('ཤིས'))

from TibProcessing import Agreement
print(Agreement().part_agreement('ཤིས', 'གི'))

from TibProcessing import Segment
print(dir())
truc = Segment().segment('བཀྲ་ཤིས་བདེ་ལེགས༎ ༎', ant_segment=0, unknown=1)
print(truc)

