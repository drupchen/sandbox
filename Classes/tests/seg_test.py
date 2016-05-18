import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

from TibProcessing import getSylComponents, Agreement, Segment, AntTib

print(getSylComponents().get_mingzhi('ཤིས'))

print(getSylComponents().get_info('ཤིའི'))

print(Agreement().part_agreement('ཁྲིས', 'གི'))

print("print(Segment().segment('བཀྲ་ཤིས་བདེ་ལེགས༎ ༎', ant_segment=0, unknown=0))")
print(Segment().segment('བཀྲ་ཤིས་བདེ་ལེགས༎ ༎', ant_segment=0, unknown=0))
print("print(Segment().segment('བཀྲ་ཤིས་བདེ་ལེགས༎ ༎', ant_segment=1, unknown=0))")
print(Segment().segment('བཀྲ་ཤིས་བདེ་ལེགས༎ ༎', ant_segment=1, unknown=0))

print("print(AntTib().to_ant_text('*** *མཚོ འང་ཡིན་xxx'))")
print(AntTib().to_ant_text('*** *མཚོ འང་ཡིན་xxx je suis méchant'))

print("print(AntTib().from_ant_text('Je suis méchant.'))")
print(AntTib().from_ant_text('Je suis méchant.'))