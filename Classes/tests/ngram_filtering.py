import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PyTib.common import pre_process, open_file, write_file

#content = open_file('/home/drupchen/Documents/TibTAL/ngram/merged_ekangyur.txt')
#write_file('/home/drupchen/Documents/TibTAL/ngram/merged_ekangyur_pre-processed.txt', pre_process(content, 'syls'))

# firt run the following command
# ./extractngram -n11 -f70 -i corpus > ./kangyur_results_raw/11-grams_raw.txt

file_num = 11
in_file = str(file_num)+'-grams_raw.txt'
in_path = '/home/drupchen/Documents/TibTAL/ngram/kangyur_results_raw/'
kangyur_ngrams = open_file(in_path+in_file).split('\n')
out = [' '.join(b) for b in sorted([a.split(' ') for a in kangyur_ngrams if a != ''], key=lambda x: int(x[-1]), reverse=True)]
filtered = []
agreement = []
for o in out:
    first = o.split(' ')[0]
    last = o.split(' ')[-2]
    if '_' not in o and '།' not in o and '༄' not in o:
        if first not in ['དང་', 'ནི་', 'པར་', 'བར་', 'པའི་', 'བའི་', 'པ་', 'བ་', 'པོ་', 'ཅེས་', 'ཅིང་', 'ཞེས་', 'སུ་', 'ཏེ་', 'ཀྱི་', 'གྱི་', 'ཀྱིས་', 'གྱིས་', 'ཏུ་', 'པོས་', 'པས་', 'རྣམས་']:
            if last not in ['དང་', 'ལ་', 'ཡང་', 'གང་', 'ནི་']:
                if last.endswith('འི་') or last.endswith('འི') or last.endswith('འོ་') or last.endswith('འོ') or last.endswith('འམ་') or last.endswith('འམ') or last in ['གི', 'ཀྱི', 'གྱི', 'ཡི', 'གིས', 'ཀྱིས', 'གྱིས', 'ཡིས', 'སུ', 'ཏུ', 'དུ', 'རུ', 'སྟེ', 'ཏེ', 'དེ', 'ཀྱང', 'འང', 'གམ', 'ངམ', 'དམ', 'ནམ', 'བམ', 'མམ', 'འམ', 'རམ', 'ལམ', 'སམ', 'ཏམ', 'གོ', 'ངོ', 'དོ', 'ནོ', 'མོ', 'འོ', 'རོ', 'ལོ', 'སོ', 'ཏོ', 'ཅིང', 'ཅེས', 'ཅེའོ', 'ཅེ', 'ཅིག', 'ཞིང', 'ཞེས', 'ཞེའོ', 'ཞེ', 'ཞིག', 'ཤིང', 'ཤེའོ', 'ཤེ', 'ཤིག', 'པར', 'བར', 'པའི', 'བའི', 'པོར', 'གི་', 'ཀྱི་', 'གྱི་', 'ཡི་', 'གིས་', 'ཀྱིས་', 'གྱིས་', 'ཡིས་', 'སུ་', 'ཏུ་', 'དུ་', 'རུ་', 'སྟེ་', 'ཏེ་', 'དེ་', 'ཀྱང་', 'འང་', 'གམ་', 'ངམ་', 'དམ་', 'ནམ་', 'བམ་', 'མམ་', 'འམ་', 'རམ་', 'ལམ་', 'སམ་', 'ཏམ་', 'གོ་', 'ངོ་', 'དོ་', 'ནོ་', 'མོ་', 'འོ་', 'རོ་', 'ལོ་', 'སོ་', 'ཏོ་', 'ཅིང་', 'ཅེས་', 'ཅེའོ་', 'ཅེ་', 'ཅིག་', 'ཞིང་', 'ཞེས་', 'ཞེའོ་', 'ཞེ་', 'ཞིག་', 'ཤིང་', 'ཤེའོ་', 'ཤེ་', 'ཤིག་', 'པར་', 'བར་', 'པའི་', 'བའི་', 'པོར་']:
                    agreement.append(o)
                else:
                    filtered.append(o)
write_file(in_path.replace('_raw', '')+in_file.replace('_raw', ''), '\n'.join(filtered))
write_file(in_path.replace('_raw', '')+in_file.replace('_raw', '_agreement'), '\n'.join(agreement))