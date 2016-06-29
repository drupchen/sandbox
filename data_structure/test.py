from .structure import MLD

layer1 = '0\t=P\n0\t+ད\n0\t+ྱ\n0\t+་\n0\t-\n4\t+G\n3\t-\n'
layer2 = '0\t=V'

test = MLD('བཀྲ་ཤིས་བདེ་ལེགས། ')
test.import_layer('l1', layer1)
test.import_layer('l2', layer2)
test.export_view()
print('layer1')
test.export_view(layers='l1')
print('layer2')
test.export_view(layers='l2')
print('layer2+layer1\n')
print(test.export_view(layers='l2+l1'))
print('\nlayer1+layer2\n')
print(test.export_view(layers='l1+l2'))

#print(MLD('./test.mld'))
