# coding: utf-8
import re
import os
w_nb = 6 # number of words before linebreaks in output

# import the lexicon
with open('lexicon.txt', 'r', -1, 'utf-8-sig') as f:
    content = [line.strip() for line in f.readlines()]
lexicon = {}
for line in content:
    parts = line.split('***')
    lexicon[parts[0]] = parts[1]

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
    
    words = []
    while len(syls) > 0:
        if   isWord(syls[:4]): process(syls, words, 4)
        elif isWord(syls[:3]): process(syls, words, 3)
        elif isWord(syls[:2]): process(syls, words, 2)
        elif isWord(syls[:1]): process(syls, words, 1)
        else:
            words.append('་'.join(syls[:1])+"་*")
            del syls[:1]
    #
    ######################
    
    # add linebreaks
    for i in range(w_nb-1, len(words), w_nb):
        words[i] += '\n'
    
    # write output
    with open('./OUT/' + 'seg_' + file, 'w', -1, 'utf-8-sig') as f:
        f.write(' '.join(words))
