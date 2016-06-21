import difflib
import re

def create_layer(base, modified):
    ndiff = difflib.ndiff(base, modified)
    layer = []
    c = 0
    for line in ndiff:
        operation = line[0]+line[2:]
        # turn - followed by + operation into a replace operation(=)
        if layer != [] and '-' in layer[-1] and '+' in line:
            parts = layer[-1].split('\t')
            layer[-1] = parts[0]+'\t'+parts[1][:-2]+'='+operation[-1]
        else:
            # only increment the counter when there is no modification in the current line
            if line.startswith('  '):
                c += 1
            # append the modification found in the current line
            else:
                layer.append(str(c)+'\t'+operation)
                c += 1
    return layer


def no_space(string):
    regexes = [r'([་|༌])\s', r'(ང[་|༌])\s', r'\s(ར)', r'\s(ས)', r'\s(འི)', r'\s(འོ)']
    for regex in regexes:
        string = re.sub(regex, r'\1', string)
    return string

with open('/home/drupchen/PycharmProjects/sandbox/ཤེར་ཕྱིན། ཕ། -.txt', 'r', -1, 'utf-8-') as f:
    seg = f.read()
raw = no_space(seg)
import time
D = time.time()
truc = [a for a in difflib.ndiff(raw, seg)]
#diff = create_layer(raw, seg)
E = time.time()
print(E-D)