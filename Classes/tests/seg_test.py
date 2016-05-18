import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

from TibProcessing import getSylComponents, Agreement, Segment, AntTib

print(getSylComponents().get_mingzhi('ཤིས'))

print(getSylComponents().get_info('ཤིའི'))

print(Agreement().part_agreement('ཁྲིས', 'གི'))


print(Segment().segment('བཀྲ་ཤིས་བདེ་ལེགས་ཕུན་སུམ་ཚོགས་པར་ཤོག', ant_segment=0, unknown=0))

truc = Segment().segment('བཀྲ་ཤིས་བདེ་ལེགས་ཕུན་སུམ་ཚོགས་པར་ཤོག', ant_segment=1, unknown=0)
print(truc)

truca = AntTib().to_ant_text(truc)
print(truca)

trucb = AntTib().from_ant_text(truca)
print(trucb)