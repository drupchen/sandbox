import PyTib
from PyTib.common import write_file, open_file
import yaml
import os
import re
from collections import defaultdict

particles = ["གི", "ཀྱི", "གྱི", "ཡི", "གིས", "ཀྱིས", "གྱིས", "ཡིས", "སུ", "ཏུ", "དུ", "རུ", "སྟེ", "ཏེ", "དེ", "ཀྱང", "ཡང", "འང", "གམ", "ངམ", "དམ", "ནམ", "བམ", "མམ", "འམ", "རམ", "ལམ", "སམ", "ཏམ", "གོ", "ངོ", "དོ", "ནོ", "མོ", "འོ", "རོ", "ལོ", "སོ", "ཏོ", "ཅིང", "ཅེས", "ཅེའོ", "ཅེ་ན", "ཅིག", "ཞིང", "ཞེས", "ཞེའོ", "ཞེ་ན", "ཞིག", "ཤིང", "ཤེའོ", "ཤེ་ན", "ཤིག", "ལ", "ན", "ནས", "ལས", "ནི", "དང", "གང", "ཅི", "ཇི", "གིན", "གྱིན", "ཀྱིན", "ཡིན", "པ", "བ", "པོ", "བོ"]


def segment_in_words(notes_conc, left, right):
    sg = PyTib.Segment()
    ed_names = [n for n in notes_conc[0]]
    errors = []
    for conc in notes_conc:
        eds = {}
        mistake = False
        for ed in ed_names:
            segmented = sg.segment(conc[ed])
            seg_syls = sg.segment(conc[ed], syl_segmented=1).split()
            note = ''.join(seg_syls[left:len(seg_syls)-right-1])
            # add all cases where particles are in the notes
            for part in particles:
                if part in note:
                    mistake = True
            if '#' in note:
                mistake = True
            eds[ed] = segmented
        if mistake:
            errors.append(eds)
    wrong_spell = []
    for e in errors:
        error = ''
        for v in e:
            error += v+'༽ '+e[v]+'\n'
        #error += '\n'
        wrong_spell.append(error)
    return wrong_spell


def find_page_num(mistake, text):
    derge_chunk = [a for a in mistake.split('\n') if a.startswith('སྡེ')][0].replace('སྡེ་༽', '').replace(' ', '').replace('_', ' ').replace('#', '')
    page_num = None
    for page in text:
        if derge_chunk in page:
            page_num = re.search(r'[0-9]+\.', page)
            if page_num:
                page_num = page_num.group(0)
    if page_num:
        return page_num
    else:
        return None

path = './output/conc_yaml/'
mistakes_with_pages = defaultdict(list)
for f in os.listdir(path):
    print(f)
    name = f.replace('_conc.yaml', '')

    # open the raw text containing the page numbers
    raw_text = open_file('./output/derge_with_pages/{}.txt'.format(name)).split('\n')

    # open the yaml file
    dump = [a for a in yaml.load_all(open_file(path+f))]

    # find all the mistakes and the particles
    mistakes = segment_in_words(dump, left=5, right=5)

    # add the page number to the each mistake
    for num, mistake in enumerate(mistakes):
        p_n = find_page_num(mistake, raw_text)
        if p_n:
            mistakes[num] = '{}\n{}'.format(p_n, mistake)
            mistakes_with_pages[name+p_n].append(mistake)

    write_file('./output/mistakes/{}.txt'.format(name), str(len(mistakes)) + '\n' + '\n'.join(mistakes))

ordered_mistakes = sorted(mistakes_with_pages, key=lambda x: len(mistakes_with_pages[x]), reverse=True)

out = ''
for m in ordered_mistakes:
    out += '\n{}\n{}'.format(m, mistakes_with_pages[m])
write_file('ordered_mistakes.txt', out)