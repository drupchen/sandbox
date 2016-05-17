import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

from TibProcessing import getSylComponents, Agreement, Segment
print(getSylComponents().get_mingzhi('ཤིས'))
print(getSylComponents().get_info('ཤིའི'))
print(Agreement().part_agreement('ཁྲི', 'གི'))

truc = Segment().segment('བཀྲ་ཤིས་བདེ་ལེགས༎ ༎', ant_segment=0, unknown=1)
print(truc)
