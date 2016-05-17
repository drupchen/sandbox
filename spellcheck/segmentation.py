
# coding: utf-8

# In[1]:

import re
import os
from bisect import bisect_left
import time
w_nb = 50  # number of words before linebreaks in output


# In[2]:

# import the lexicon
one = time.time()
with open('tsikchen.txt', 'r', -1, 'utf-8-sig') as f:
    lexicon = [line.strip() for line in f.readlines()]
# add all the particles
lexicon.extend(['གི', 'ཀྱི', 'གྱི', 'ཡི', 'གིས', 'ཀྱིས', 'གྱིས', 'ཡིས', 'སུ', 'ཏུ', 'དུ', 'རུ', 'སྟེ', 'ཏེ', 'དེ', 'ཀྱང', 'ཡང', 'འང', 'གམ', 'ངམ', 'དམ', 'ནམ', 'བམ', 'མམ', 'འམ', 'རམ', 'ལམ', 'སམ', 'ཏམ', 'གོ', 'ངོ', 'དོ', 'ནོ', 'མོ', 'འོ', 'རོ', 'ལོ', 'སོ', 'ཏོ', 'ཅིང', 'ཅེས', 'ཅེའོ', 'ཅེ་ན', 'ཅིག', 'ཞིང', 'ཞེས', 'ཞེའོ', 'ཞེ་ན', 'ཞིག', 'ཤིང', 'ཤེའོ', 'ཤེ་ན', 'ཤིག', 'ལ', 'ན', 'ནས', 'ལས', 'ནི', 'དང', 'གང', 'ཅི', 'ཇི', 'གིན', 'གྱིན', 'ཀྱིན', 'ཡིན', 'པ', 'བ', 'པོ', 'བོ'])
# add all Monlam verbs
with open('monlam1_verbs.txt', 'r', -1, 'utf-8-sig') as f:
    monlam_verbs = [line.strip() for line in f.readlines()]
for entry in monlam_verbs:
    verb = entry.split(' | ')[0]
    if verb not in lexicon:
        lexicon.append(verb)
lexicon = sorted(lexicon)
len_lexicon = len(lexicon)
        
# import the Monlam POS tags
with open('./monlam1_pos.txt', 'r', -1, 'utf-8-sig') as f: # Monlam
    monlam = [line.strip() for line in f.readlines()]
monlam_pos = {}
for line in monlam:
    parts = line.split('—')  # Monlam
    monlam_pos[parts[0]] = parts[1] 

# import the Hill POS tags
with open('hill_pos.txt', 'r', -1, 'utf-8-sig') as f: # Hill
    hill = [line.strip() for line in f.readlines()]
hill_pos = {}
for line in hill:
    parts = line.split('—')  # Hill
    hill_pos[parts[0]] = parts[1]
two = time.time()

# In[43]:

def get_pos(dict, key):
    if key.endswith('་'):
        key = key[:-1]
    return dict.get(key)

def get_main_pos(key, num):
    if num == 0:
        Dict = monlam_pos
    if num == 1:
        Dict = hill_pos
    pos = get_pos(Dict, key)

    main_pos = []
    if pos != None:
        # Monlam
        if num == 0:
            parts = pos.split('/')
            for part in parts:
                if part != '':
                    main_pos.append(part.split(':')[0])

        # Hill
        if num == 1:
            parts = pos.split('/')
            for part in parts:
                if part != '':
                    if '.' in part:
                        main_pos.append(part.split('.')[0])
                    else:
                        main_pos.append(part)        
    return main_pos


# In[44]:

get_main_pos('གཟུགས', 0)


# In[108]:

def search(List, entry):
    global len_lexicon
    index = bisect_left(List, entry, 0, len_lexicon)
    return(True if index != len_lexicon and List[index] == entry else False)
    
def isWord(syls):
    global total
    maybe = '་'.join(syls)
    final = False
    if search(lexicon, maybe) == True:
        final = True
    elif search(lexicon, re.sub(merged_part, '', maybe)) == True:
        final = True
    return final

def process(list1, list2, num):
    global c
    word = '་'.join(list1[c:c+num])
    if search(lexicon, word) == False:
        maybe = re.split(merged_part, word)
        list2.append(maybe[0])
        list2.append(maybe[1]+'་')
        #del list1[:num]
        c = c + num
    else:
        list2.append(word+"་")
        #del list1[:num]
        c = c + num


# In[109]:

print(re.findall(r"[།|༎|༏|༐|༑|༔|\s]+་", ' །་'))


# In[110]:

words[11]


# In[132]:

for file in os.listdir('./IN/'):
    if file.endswith(".txt"):
        # todo - replace \n by \s try: with open('drugs') as temp_file: \n drugs = [line.rstrip('\n') for line in temp_file]
        try:
            with open('./IN/' + file, 'r', -1, 'utf-8-sig') as f:
                current_file = f.read().replace('\n', '').replace('\r\n', '')

        except:
            print("Save all IN files as UTF-8 and try again.")
            #input()
    else:
        print("\nSave all IN files as text files and try again.")
        #input()
    #start = time.time()
    ######################
    # segmentation process
    merged_part = r'(ར|ས|འི|འམ|འང)$'
    
    syls = re.sub(r"([།|༎|༏|༐|༑|༔|\s]+)", "་\g<1>་", current_file)
    syls = re.split(r"་+", syls)
    
    non_words = []
    words = []
    c = 0
    while c < len(syls):
        if   isWord(syls[c:c+4]): process(syls, words, 4)
        elif isWord(syls[c:c+3]): process(syls, words, 3)
        elif isWord(syls[c:c+2]): process(syls, words, 2)
        elif isWord(syls[c:c+1]): process(syls, words, 1)
        else:
            words.append('་'.join(syls[c:c+1])+"་*")
            non_words.append('་'.join(syls[c:c+1])+"་")
            c = c + 1
    #
    ######################
    
    #end = time.time()
    ######################
    # particle check
    for num, word in enumerate(words):
        
        # all non-ambiguous particles :
        # 'གི', 'ཀྱི', 'གྱི', 'གིས', 'ཀྱིས', 'ཡིས', 'ཏུ', 'རུ', 'སྟེ', 'ཏེ', 'ཀྱང', 'ཡང', 'འང',
        # 'མམ', 'འམ', 'སམ', 'ཏམ', 'ནོ', 'ཏོ',
        # 'ཅིང', 'ཅེས', 'ཅེའོ', 'ཅིག', 'ཞེས', 'ཞེའོ', 'ཞིག', 'ཤིང', 'ཤེའོ', 'ཤིག'
        non_amb = ['གི', 'ཀྱི', 'གྱི', 'གིས', 'ཀྱིས', 'ཡིས', 'ཏུ', 'རུ', 'སྟེ', 'ཏེ', 'ཀྱང', 'ཡང', 'འང', 'མམ', 'འམ', 'སམ', 'ཏམ', 'ནོ', 'ཏོ', 'ཅིང', 'ཅེས', 'ཅེའོ', 'ཅིག', 'ཞེས', 'ཞེའོ', 'ཞིག', 'ཤིང', 'ཤེའོ', 'ཤིག']
        if word[:-1] in non_amb:
            previous = words[num-1]
            corr = part_agreement(previous[:-1], word[:-1])+'་'
            if corr != word:
                print(''.join(words[num-3:num]), word, corr)
                words[num] = corr
        
        # དེ་ : if preceded by a noun, it is a pronoun, if preceded by a verb, it is a particle
        if word == 'དེ་':
            previous = words[num-1]
            monlam_previous = get_main_pos(previous, 0)
            monlam_previous = list(set(monlam_previous))
            hill_previous = get_main_pos(previous, 1)
            hill_previous = list(set(hill_previous))
            if 'བྱ་ཚིག' in monlam_previous or 'v' in hill_previous:
                words[num] = words[num]+'P'
                corr = part_agreement(previous[:-1], word)
                if corr != word:
                    words[num] = words[num] + corr
                words[num-1] = words[num-1]+'#'+'v'
                
        # hack to remove all * in the punctuation
        if re.findall(r'[།|༎|༏|༐|༑|༔|༄|༅|\s]+', word) != []:
            words[num] = words[num].replace('*', '')
    #['ཡི', 'གྱིས', 'སུ', 'དུ', 'ལམ', 'གམ', 'ངམ', 'དམ', 'ནམ', 'བམ', 'རམ', 'པ', 'པོ', 'བ', 'བོ', 'གོ', 'ངོ', 'དོ', 'མོ', 'འོ', 'རོ', 'ལོ', 'སོ', 'དེ',  'ཞིང']
    #
    ######################
    #print(end-start)
    ######################
    # count percentage of POS tagged words
    #pos_tagged = []
    #for word in words:
    #    wor = word
    #    if word.endswith('་'):
    #        wor = word[:-1]
    #    if wor in monlam_pos.keys() and wor in hill_pos.keys():
    #        pos_tagged.append(word+'|'+hill_pos[wor]+'#'+monlam_pos[wor])
    #    elif wor in monlam_pos.keys() and wor not in hill_pos.keys():
    #        pos_tagged.append(word+'|'+monlam_pos[wor])
    #    elif wor not in monlam_pos.keys() and wor in hill_pos.keys():
    #        pos_tagged.append(word+'|'+hill_pos[wor])
    #    else:
    #        pos_tagged.append(word)

    #pos = 0
    #no_pos = 0
    #for word in pos_tagged:
    #    if '|' in word:
    #        pos = pos+1
    #    else:
    #        no_pos = pos+1
    #print(pos, 'words out of', len(pos_tagged), 'have a POS.', '\n', pos*100/len(pos_tagged), '% of the words have tags.')
    #
    ######################
    
    ######################
    # flag particles
    
    
    #
    ######################
    
    ######################
    # flag verbs
    
    
    #
    ######################
    

    # add linebreaks after 400 words
    for i in range(w_nb-1, len(words), w_nb):
        words[i] += '\n'
    
    # write output
    with open('./OUT/' + 'seg_' + file, 'w', -1, 'utf-8-sig') as f:
        f.write(' '.join(words))
    
    with open('nonwords_' + file, 'w', -1, 'utf-8-sig') as f:
        f.write('\n'.join(sorted(list(set(non_words)))))


# In[98]:

words[:20]


# In[ ]:



