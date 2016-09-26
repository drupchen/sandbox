from subprocess import Popen, PIPE, call, check_output
import re
import tempfile


def no_space(string):
    regexes = [r'([་|༌])\s', r'(ང[་|༌])\s', r'\s(ར)', r'\s(ས)', r'\s(འི)', r'\s(འོ)']
    for regex in regexes:
        string = re.sub(regex, r'\1', string)
    return string

with open('/home/drupchen/PycharmProjects/sandbox/Classes/tests/files/བསྟོདཚོགས.txt', 'r', -1, 'utf-8-') as f:
    seg = f.read().replace('\n', '')
raw = no_space(seg)


def temp_object(content):
    temp = tempfile.NamedTemporaryFile(delete=True)
    temp.write(str.encode(content))
    return temp


def unix_diff(string_a, string_b, windows=False):
    # insert \n after every character and create a temp file
    temp_A = temp_object('\n'.join(list(string_a)) + '\n')
    temp_B = temp_object('\n'.join(list(string_b)) + '\n')
    # support for windows
    diff_command = 'diff'
    if windows:
        diff_command = 'third_parties/diff_exe/diff.exe'
    # diff call
    raw_diff = Popen([diff_command, '-H', temp_A.name, temp_B.name], shell=False, stdout=PIPE)
    return bytes.decode(raw_diff.communicate()[0])

diff = unix_diff('abc', 'abci')
diff_list = re.split(r'\n?([^\n]+[acd][^\n]+)\n?', diff)[1:]

layer = {}
while len(diff_list) >= 2:
    idx, op = re.split(r'([acd])', diff_list.pop(0))[:2]
    modifs = diff_list.pop(0).split('\n')
    print(modifs)


