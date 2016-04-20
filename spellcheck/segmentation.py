
# coding: utf-8

# In[58]:

import re
import os
w_nb = 50 # number of words before linebreaks in output


# In[13]:

# import the lexicon
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

# import the Monlam POS tags
with open('./monlam1_pos.txt', 'r', -1, 'utf-8-sig') as f: # Monlam
    monlam = [line.strip() for line in f.readlines()]
monlam_pos = {}
for line in monlam:
    parts = line.split('—') # Monlam
    monlam_pos[parts[0]] = parts[1] 

# import the Hill POS tags
with open('hill_pos.txt', 'r', -1, 'utf-8-sig') as f: # Hill
    hill = [line.strip() for line in f.readlines()]
hill_pos = {}
for line in hill:
    parts = line.split('***') # Hill
    hill_pos[parts[0]] = parts[1]


# In[100]:

def part_agreement(previous, particle):
    final = previous[-1]
    print(final)
    dreldra = {'ད' : 'ཀྱི', 'བ' : 'ཀྱི', 'ས' : 'ཀྱི', 'ག' : 'གི', 'ང' : 'གི', 'ན' : 'གྱི', 'མ' : 'གྱི', 'ར' : 'གྱི', 'ལ' : 'གྱི', 'འ' : 'ཡི', 'མཐའ་མེད' : 'ཡི'}
    jedra = {'ད' : 'ཀྱིས', 'བ' : 'ཀྱིས', 'ས' : 'ཀྱིས', 'ག' : 'གིས', 'ང' : 'གིས', 'ན' : 'གྱིས', 'མ' : 'གྱིས', 'ར' : 'གྱིས', 'ལ' : 'གྱིས', 'འ' : 'ཡིས', 'མཐའ་མེད' : 'ཡིས'}
    ladon = {'ག' : 'ཏུ', 'བ' : 'ཏུ', 'ད་དྲག' : 'ཏུ', 'ང' : 'དུ', 'ད' : 'དུ', 'ན' : 'དུ', 'མ' : 'དུ', 'ར' : 'དུ', 'ལ' : 'དུ', 'འ' : 'རུ', 'མཐའ་མེད' : 'རུ', 'ས' : 'སུ'}
    lhakce = {'ན' : 'ཏེ', 'ར' : 'ཏེ', 'ལ' : 'ཏེ', 'ས' : 'ཏེ', 'ད' : 'དེ', 'ག' : 'སྟེ', 'ང' : 'སྟེ', 'བ' : 'སྟེ', 'མ' : 'སྟེ', 'འ' : 'སྟེ', 'མཐའ་མེད' : 'སྟེ'}
    gyendu = {'ག' : 'ཀྱང', 'ད' : 'ཀྱང', 'བ' : 'ཀྱང', 'ས' : 'ཀྱང', 'འ' : 'འང', 'མཐའ་མེད' : 'འང', 'ང' : 'ཡང', 'ན' : 'ཡང', 'མ' : 'ཡང', 'འ' : 'ཡང', 'ར' : 'ཡང', 'ལ' : 'ཡང', 'མཐའ་མེད' : 'ཡང'}
    jedu = {'ག' : 'གམ', 'ང' : 'ངམ', 'ད་དྲག' : 'ཏམ', 'ད' : 'དམ', 'ན' : 'ནམ', 'བ' : 'བམ', 'མ' : 'མམ', 'འ' : 'འམ', 'ར' : 'རམ', 'ལ' : 'ལམ', 'ས' : 'སམ'}
    dagdra = {'ག' : 'པ', 'ད' : 'པ', 'བ' : 'པ', 'ས' : 'པ', 'ན' : 'པ', 'མ' : 'པ', 'ག' : 'པོ', 'ད' : 'པོ', 'བ' : 'པོ', 'ས' : 'པོ', 'ན' : 'པོ', 'མ' : 'པོ', 'ང' : 'བ', 'འ' : 'བ', 'ར' : 'བ', 'ལ' : 'བ', 'མཐའ་མེད' : 'བ', 'ང' : 'བོ', 'འ' : 'བོ', 'ར' : 'བོ', 'ལ' : 'བོ', 'མཐའ་མེད' : 'བོ'}
    lardu = {'ག' : 'གོ', 'ང' : 'ངོ', 'ད་དྲག' : 'ཏོ', 'ད' : 'དོ', 'ན' : 'ནོ', 'བ' : 'བོ', 'མ' : 'མོ', 'འ' : 'འོ', 'ར' : 'རོ', 'ལ' : 'ལོ', 'ས' : 'སོ'}
    cing = {'ག' : 'ཅིང', 'ད' : 'ཅིང', 'བ' : 'ཅིང', 'ད་དྲག' : 'ཅིང', 'ང' : 'ཞིང', 'ན' : 'ཞིང', 'མ' : 'ཞིང', 'འ' : 'ཞིང', 'ར' : 'ཞིང', 'ལ' : 'ཞིང', 'མཐའ་མེད' : 'ཞིང', 'ས' : 'ཤིང'}
    ces = {'ག' : 'ཅེས', 'ད' : 'ཅེས', 'བ' : 'ཅེས', 'ད་དྲག' : 'ཅེས', 'ང' : 'ཞེས', 'ན' : 'ཞེས', 'མ' : 'ཞེས', 'འ' : 'ཞེས', 'ར' : 'ཞེས', 'ལ' : 'ཞེས', 'ས' : 'ཞེས', 'མཐའ་མེད' : 'ཞེས'}
    ceo = {'ག' : 'ཅེའོ', 'ད' : 'ཅེའོ', 'བ' : 'ཅེའོ', 'ད་དྲག' : 'ཅེའོ', 'ང' : 'ཞེའོ', 'ན' : 'ཞེའོ', 'མ' : 'ཞེའོ', 'འ' : 'ཞེའོ', 'ར' : 'ཞེའོ', 'ལ' : 'ཞེའོ', 'མཐའ་མེད' : 'ཞེའོ', 'ས' : 'ཤེའོ'}
    cena = {'ག' : 'ཅེ་ན', 'ད' : 'ཅེ་ན', 'བ' : 'ཅེ་ན', 'ད་དྲག' : 'ཅེ་ན', 'ང' : 'ཞེ་ན', 'ན' : 'ཞེ་ན', 'མ' : 'ཞེ་ན', 'འ' : 'ཞེ་ན', 'ར' : 'ཞེ་ན', 'ལ' : 'ཞེ་ན', 'མཐའ་མེད' : 'ཞེ་ན', 'ས' : 'ཤེ་ན'}
    cig = {'ག' : 'ཅིག', 'ད' : 'ཅིག', 'བ' : 'ཅིག', 'ད་དྲག' : 'ཅིག', 'ང' : 'ཞིག', 'ན' : 'ཞིག', 'མ' : 'ཞིག', 'འ' : 'ཞིག', 'ར' : 'ཞིག', 'ལ' : 'ཞིག', 'མཐའ་མེད' : 'ཞིག', 'ས' : 'ཤིག'}
    cases = [(["གི", "ཀྱི", "གྱི", "ཡི"], dreldra), (["གིས", "ཀྱིས", "གྱིས", "ཡིས"], jedra), (["སུ", "ཏུ", "དུ", "རུ"] , ladon), (["སྟེ", "ཏེ", "དེ"], lhakce), (["ཀྱང", "ཡང", "འང"], gyendu), (["གམ", "ངམ", "དམ", "ནམ", "བམ", "མམ", "འམ", "རམ", "ལམ", "སམ", "ཏམ"], jedu), (["པ", "པོ", "བ", "བོ"], dagdra), (["གོ", "ངོ", "དོ", "ནོ", "བོ", "མོ", "འོ", "རོ", "ལོ", "སོ", "ཏོ"] , lardu), (["ཅིང",  "ཤིང", "ཞིང"], cing), (["ཅེས",  "ཞེས"], ces), (["ཅེའོ",  "ཤེའོ",  "ཞེའོ"], ceo), (["ཅེ་ན",  "ཤེ་ན",  "ཞེ་ན"], cena), (["ཅིག",  "ཤིག",  "ཞིག"], cig)]
    correction = ''
    for case in cases:
        if particle in case[0]:
            correction = case[1][final]
    return correction


# In[95]:

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
    main = []
    if pos != None:
        # Monlam
        if num == 0:
            parts = pos.split('#')
            for part in parts:
                if part != '':
                    main.append(part.split(':')[0])

        # Hill
        if num == 1:
            parts = pos.split('_')
            for part in parts:
                if part != '':
                    if '.' in part:
                        main.append(part.split('.')[0])
                    else:
                        main.append(part)        
    return main


# In[116]:

import timeit
def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def costly_func(lst):
    return map(lambda x: x^2, lst)

wrapped = wrapper(get_main_pos, 'བྱེད', 0)
timeit.timeit(wrapped, number=1000)


# In[114]:

def isWord(syls):
    maybe = '་'.join(syls)
    final = False
    if maybe in lexicon:
        final = True
    elif re.sub(merged_part, '', maybe) in lexicon:
        final = True
    return final

def process(list1, list2, num):
    word = '་'.join(list1[:num])
    if word not in lexicon:
        maybe = re.split(merged_part, word)
        list2.append(maybe[0])
        list2.append(maybe[1]+'་')
        del list1[:num]
    else:
        list2.append(word+"་")
        del list1[:num]


# In[99]:

for file in os.listdir('./IN/'):
    if file.endswith(".txt"):
    #todo - replace \n by \s try: with open('drugs') as temp_file: \n drugs = [line.rstrip('\n') for line in temp_file]
        try:
            with open('./IN/' + file, 'r', -1, 'utf-8-sig') as f:
                current_file = f.read().replace('\n', '').replace('\r\n', '')

        except:
            print("Save all IN files as UTF-8 and try again.")
            input()
    else:
        print("\nSave all IN files as text files and try again.")
        input()
    
    ######################
    # Segmentation process
    merged_part = r'(ར|ས|འི|འམ|འང)$'
    
    syls = re.sub(r"([།|༎|༏|༐|༑|༔|\s]+)", "་\g<1>་", current_file)
    syls = re.split(r"་+", syls)
    
    non_words = []
    words = []
    while len(syls) > 0:
        if   isWord(syls[:4]): process(syls, words, 4)
        elif isWord(syls[:3]): process(syls, words, 3)
        elif isWord(syls[:2]): process(syls, words, 2)
        elif isWord(syls[:1]): process(syls, words, 1)
        else:
            words.append('་'.join(syls[:1])+"་*")
            non_words.append('་'.join(syls[:1])+"་")
            del syls[:1]
    #
    ######################
    
    ######################
    # particle check
    for num, word in enumerate(words):
        # དེ་ : if preceded by a noun, it is a pronoun, if preceded by a verb, it is a particle
        if word == 'དེ':
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
                words[num-1] = words[num-1]+'_'+'/'.join(hill_previous+monlam_previous)
    
    #
    ######################
    
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


# In[103]:




# In[104]:

long_list = range(1000)
wrapped = wrapper(costly_func, long_list)
timeit.timeit(wrapped, number=1000)


# In[ ]:



