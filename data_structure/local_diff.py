from subprocess import Popen, PIPE, call, check_output
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
import time
A = time.time()
temp_A = tempfile.NamedTemporaryFile()
temp_B = tempfile.NamedTemporaryFile()
temp_A.write(str.encode('\n'.join(list(raw))+'\n'))
temp_B.write(str.encode('\n'.join(list(seg))+'\n'))
temp_A.flush()
temp_B.flush()
B = time.time()
diff = Popen(['diff', '-H', temp_B.name, temp_A.name], shell=False, stdout=PIPE)
out = bytes.decode(diff.communicate()[0])
C = time.time()
print('temp creation', B-A)
print('diff', C-B)
out = re.split(r'\n?([^\n]+[acd][^\n]+)\n?', out)
layer = {}
index = ''
operation = ''
string = ''
for line in out:
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
    else:
        if '\n' in line:
            ops = line.split('\n')
