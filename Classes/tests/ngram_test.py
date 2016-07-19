import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
import time
import Levenshtein
from collections import defaultdict
from PyTib import Segment
from PyTib.common import write_file, open_file, tib_sort, pre_process
from tqdm import tqdm

def no_trailing_tsek(string):
    if string.endswith('་'):
        return string[:-1]
    else:
        return string

def no_punct(string):
    punct = ['༄', '༅', '།', '་', '༌', '༑', '༎', '༏', '༐', '༔', '_']
    for p in punct:
        string = string.replace(p, '')
    return string

def ngram_minimal_pairs(orig_list, ngram_list, similarity=72):
    matches = {}
    for n_gram in tqdm(ngram_list[:1000]):
        orig_ngram = n_gram[-1]+' '+''.join(n_gram[:-1])
        matches[orig_ngram] = defaultdict(int)
        ngram_indexes = [a for a in range(len(n_gram)-1)]
        hollowed_ngram_indexes = [(j, [a for a in ngram_indexes if a != j]) for j in ngram_indexes]
        for i in range(len(orig_list)-1):
            for h in hollowed_ngram_indexes:
                hole = h[0]
                if i + hole <= len(orig_list) - 1:
                    hole_syl_orig = no_trailing_tsek(orig_list[i + hole])
                    hole_syl_ngram = no_trailing_tsek(n_gram[hole])
                    lev_index = Levenshtein.jaro_winkler(hole_syl_orig, hole_syl_ngram)*100
                    if lev_index < 100 and lev_index >= similarity and no_punct(hole_syl_ngram) != no_punct(hole_syl_orig):
                        hollowed_orig_slice = ''.join([orig_list[i + j] for j in h[1] if i + j <= len(orig_list) - 1])
                        hollowed_ngram_list = ''.join([n_gram[j] for j in h[1]])
                        if no_trailing_tsek(hollowed_orig_slice) == no_trailing_tsek(hollowed_ngram_list):
                            matches[orig_ngram][''.join(orig_list[i:i + len(n_gram)-1])] += 1
    # formatting
    output = ''
    for t in sorted(matches, reverse=True):
        if matches[t]:
            output += t + '\n'
            for occ in tib_sort(matches[t]):
                output += '\t'+occ+'\t'+str(matches[t][occ])+'\n'
            output += '\n'
    return output

def find_wrong_agreement(orig_list, ngram_list, similarity=80):
    matches = {}
    particles = ['འི་', 'འོ་', 'འམ་', 'གི་', 'ཀྱི་', 'གྱི་', 'ཡི་', 'གིས་', 'ཀྱིས་', 'གྱིས་', 'ཡིས་', 'སུ་', 'ཏུ་',
                 'དུ་', 'རུ་', 'སྟེ་', 'ཏེ་', 'དེ་', 'ཀྱང་', 'འང་', 'གམ་', 'ངམ་', 'དམ་', 'ནམ་', 'བམ་', 'མམ་', 'འམ་',
                 'རམ་', 'ལམ་', 'སམ་', 'ཏམ་', 'གོ་', 'ངོ་', 'དོ་', 'ནོ་', 'མོ་', 'འོ་', 'རོ་', 'ལོ་', 'སོ་', 'ཏོ་',
                 'ཅིང་', 'ཅེས་', 'ཅེའོ་', 'ཅེ་', 'ཅིག་', 'ཞིང་', 'ཞེས་', 'ཞེའོ་', 'ཞེ་', 'ཞིག་', 'ཤིང་', 'ཤེའོ་', 'ཤེ་',
                 'ཤིག་', 'པར་', 'བར་', 'པའི་', 'བའི་', 'པོར་']
    for n_gram in tqdm(ngram_list):
        orig_ngram = n_gram[-1]+' '+''.join(n_gram[:-1])
        matches[orig_ngram] = defaultdict(int)
        ngram_indexes = [a for a in range(len(n_gram)-1)]
        hollowed_ngram_indexes = [(j, [b for b in ngram_indexes if b != j]) for j in ngram_indexes if j != 0 and j != len(ngram_indexes)-1]
        for i in range(len(orig_list)-1):
            for h in hollowed_ngram_indexes:
                hole = h[0]
                if i + hole <= len(orig_list) - 1 and n_gram[hole] in particles:
                    hole_syl_orig = no_trailing_tsek(orig_list[i + hole])
                    hole_syl_ngram = no_trailing_tsek(n_gram[hole])
                    lev_index = Levenshtein.jaro_winkler(hole_syl_orig, hole_syl_ngram)*100
                    if lev_index < 100 and lev_index >= similarity and no_punct(hole_syl_ngram) != no_punct(hole_syl_orig):
                        hollowed_orig_slice = ''.join([orig_list[i + j] for j in h[1] if i + j <= len(orig_list) - 1])
                        hollowed_ngram_list = ''.join([n_gram[j] for j in h[1]])
                        if no_trailing_tsek(hollowed_orig_slice) == no_trailing_tsek(hollowed_ngram_list):
                            matches[orig_ngram][''.join(orig_list[i:i + len(n_gram)-1])] += 1
    # formatting
    output = ''
    for t in sorted(matches, reverse=True):
        if matches[t]:
            output += t + '\n'
            for occ in tib_sort(matches[t]):
                output += '\t'+occ+'\t'+str(matches[t][occ])+'\n'
            output += '\n'
    return output

#raw_string = open_file('/home/drupchen/PycharmProjects/nalanda_corpus/gyu_raw/རྒྱུད། པུ།.txt').replace('\n', '')
#syls = Segment().segment(raw_string.replace('༌', '་'), ant_segment=1, unknown=0, space_at_punct=True)
#write_file('syls_seperated.txt', ''.join(syls))

# finding variants of a the ngrams
#original = open_file('./syls_seperated.txt').split(' ')
#ngrams = [a.split(' ')[:-1] for a in open_file('./reduced_algo3.txt').split('\n')]
#A = time.time()
#write_file('test.txt', ngram_minimal_pairs(original, ngrams))
#B = time.time()
#print(B-A)


# kangyur bigram agreement
agrmnt_path = '/home/drupchen/Documents/TibTAL/ngram/kangyur_results/'+'4-grams_agreement.txt'
text_path = '/home/drupchen/PycharmProjects/nalanda_corpus/gyu_raw/རྒྱུད་ཡ།.txt'
out_path = './out.txt'
# segmenting on syllables without separating the fusioned particles
original = pre_process(open_file(text_path).replace('\n', '').replace('༌', '་'), mode='syls')
# segmenting on syllables separating fusioned particles
#original = Segment().segment(open_file(text_path).replace('\n', '').replace('༌', '་'), ant_segment=1, unknown=0, space_at_punct=True).split(' ')
ngrams = [a.split(' ') for a in open_file(agrmnt_path).split('\n')]
write_file(out_path, find_wrong_agreement(original, ngrams, similarity=72).replace('_', ' '))


