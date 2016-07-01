from subprocess import Popen, PIPE, check_output
import re
import tempfile


def no_space(string):
    regexes = [r'([་|༌])\s', r'(ང[་|༌])\s', r'\s(ར)', r'\s(ས)', r'\s(འི)', r'\s(འོ)']
    for regex in regexes:
        string = re.sub(regex, r'\1', string)
    return string

with open('/home/drupchen/PycharmProjects/sandbox/ཤེར་ཕྱིན། ཕ། -.txt', 'r', -1, 'utf-8-') as f:
    seg = f.read().replace('\n', '')


raw = no_space(seg)
#with open('/home/drupchen/PycharmProjects/sandbox/data_structure/raw.txt', 'w', -1, 'utf-8-') as f:
#    for r in raw:
#        f.write(r+'\n')
#with open('/home/drupchen/PycharmProjects/sandbox/data_structure/seg.txt', 'w', -1, 'utf-8-') as f:
#    for s in seg:
#        f.write(s+'\n')

temp_A = tempfile.NamedTemporaryFile(delete=True)
temp_B = tempfile.NamedTemporaryFile(delete=True)
temp_A.write(str.encode('\n'.join([r for r in raw])))
temp_B.write(str.encode('\n'.join([s for s in seg])))
temp_A.flush()
temp_B.flush()

diff = Popen(['diff', temp_A.name, temp_B.name], stdout=PIPE, stdin=PIPE, shell=False)
out = bytes.decode(diff.communicate()[0])
layer = {}
index = ''
operation = ''
string = ''
for line in out:
    if line[0] != '>' or line[0] != '>' or line[0] != '-':
        # add the finished operation to the layer

        # find the index and the operation
        if 'a' in line:
            index = line.split('a')[0]
            operation = 'a'
        elif 'c' in line:
            index = line.split('c')[0]
            operation = 'c'
        elif 'd' in line:
            index = line.split('d')[0]
            operation = 'd'
    

