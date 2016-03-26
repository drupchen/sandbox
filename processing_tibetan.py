
# coding: utf-8

# In[12]:

import re


# In[13]:

#chunk = re.sub(r'([^།])\s', r'\1', chunk) # eliminate the extra spaces added by the segmentation in words


# In[14]:

# syllable = re.sub("་", "", syllable)


# In[7]:

def add_tsheg(line_list):
    '''
    takes as input a list of text splitted at the tshek.
    It deals with the final ། and the extra tshek added to ང་
    '''
    to_del = 0
    for s in range(len(line_list)):
        if line_list[s].endswith("།") or line_list[s].endswith("། ") or line_list[s].endswith("_")or line_list[s].endswith(" ") or line_list[s] == "":
            s = s
        elif line_list[s].endswith("ང") and line_list[s+1].startswith("།"):
            line_list[s] = line_list[s]+"་"+line_list[s+1]
            to_del = s+1
        else:
            line_list[s] += "་"
    if to_del != 0:
        del line_list[to_del]
    return line_list

line = "།བཅོམ་ལྡན་འདས་དེའི་ཚེ་ན་ཚེ་དང་ལྡན་པ་ཀུན་དགང་།ཀུན ་ཀུན་"
splitted = line.split("་")
print(add_tsheg(splitted))


# In[9]:

def joinedword_list(word, line):
    '''
    splits by tsheks a tibetan string(line)
    splits by tsheks a given multi-syllabled tibetan word 
    puts together the syllables of the word in the splitted string
    '''
    word_syllables = []
    if "་" in word:
        if word.endswith("་"):
            word_syllables = word.split("་")
            del(word_syllables[len(word_syllables)-1])    
        else:
            word_syllables = word.split("་")
    word_syllables = add_tsheg(word_syllables)
    
    syllabled = line.split("་")
    syllabled = add_tsheg(syllabled)
    occurences = []
    for s in range(len(syllabled)-len(word_syllables)):
        temp = []
        for m in range(len(word_syllables)):
            if word_syllables[m] == syllabled[s+m].strip("།"):#
                temp.append(s+m)
        if len(temp) == len(word_syllables):
            up = temp[0]
            down = temp[len(temp)-1]
            occurences.append((up,"".join(syllabled[up:down+1])))
    # replace first syllable with joined word
    for o in range(len(occurences)):
        syllabled[occurences[o][0]] = occurences[o][1]
    
    number = len(word_syllables)-1
    no = 0
    for o in range(len(occurences)):
        for i in range(number):
            del syllabled[occurences[o][0]+1-o-no]
        no = no+1
    return syllabled

line = "།བཅོམ་ལྡན་འདས་དེའི་ཚེ་ན་ཚེ་དང་ལྡན་པ་ཀུན་དགའ་བོ་བཅོམ་ལྡན་འདས་ཀྱི་སྣམ་ལོགས་ན་བསིལ་ཡབ་ཐོགས་ཏེ་བཅོམ་ལྡན་འདས་ལ་བསིལ་ཡབ་ཀྱིས་གཡོབ་ཅིང་འདུག་བཅོམ་ལྡན་འདས་"
word = "བཅོམ་ལྡན་འདས་"
print(joinedword_list(word, line))


# In[ ]:



