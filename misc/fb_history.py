from PyTib.common import open_file, write_file
import re
path = '/home/drupchen/Bureau/fb-archive/'
raw = open_file(path+'fb.txt').replace('Drupchen Dorje', 'Moi ').replace('Ngawang Trinley', 'NT ').replace('+01','').replace('+02', '')
raw = re.sub(r'\n\n(.*)\n', r'\n\1\n\n', raw)
messages = raw.split('\n\n')
out = '\n'.join([messages[a].replace('\n', ' ').replace('UTC', '\t').strip() for a in sorted(range(0, len(messages)-1), reverse=True) if 'juillet 2016' in messages[a]])
write_file(path+'fb_good.txt', out)
