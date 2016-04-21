
# coding: utf-8

# # Monlam Lexicon

# ## From xml

# In[ ]:

from bs4 import BeautifulSoup as Soup


# In[ ]:

import re


# In[ ]:

with open('monlamTb1.xml', 'r', -1, 'utf-8-sig') as f:
    monlam = f.read()


# In[ ]:

soup = Soup(monlam, 'lxml')


# In[ ]:

dicts = soup.array.findAll('dict')


# In[ ]:

monlam_dict = []
for dic in dicts:
    entry = dic.find_all('string')
    lemma = entry[0].string
    descr = entry[1].string.replace('\n', '')
    monlam_dict.append(lemma+' | '+descr)


# In[ ]:

with open('./monlam/monlam1_total.txt', 'w', -1, 'utf-8-sig') as f:
    f.write('\n'.join(monlam_dict))


# ## From txt

# In[ ]:

with open('./monlam/monlam1_total.txt','r', -1, 'utf-8-sig') as f:
    content0 = [line.strip() for line in f.readlines()]


# ### find all Categories

# In[ ]:

combined_entries = []
for line in content0:
    # separate the entry and the description
    parts = line.split(' | ')
    lemma = parts[0].strip()
    #print(lemma, end = ' ')
    # separate all sub-entries
    sub_entries = re.split(r'༡(མིང|བྱ|རྒྱན|བསྣན|ཚབ|མཚུངས|སྒྲུབ|ཕྲད|འབོད|གྲངས|འཇལ|གྲོགས)་ཚིག', parts[1])
    tags = ''
    for i in range(1, len(sub_entries), 2):
        tags += sub_entries[i]+'+'
    if tags not in combined_entries:
        combined_entries.append(tags)
        if tags == '':
            print(line)


# In[ ]:

print(combined_entries)
for e in combined_entries:
    plus = re.findall('\+', e)
    print(plus)


# ### POS

# ### correct missing tags

# In[ ]:

# list all the pos by looking at the 
pos = []
for line in content0:
    tags = re.findall(r' [༡༢][^ ༡༢༣༤༥༦༧༨༩༠.༽]+[ །]', line)
    pos.extend(tags)
pos = sorted(set(pos))

for p in pos:
    print(p)


# In[ ]:

num_missing = []
num_inserted = []
# insert the missing number in all tags that lack it
for num, line in enumerate(content0):
    #tag = re.findall(r'[། ][^༡༢](ཆོས་ལུགས།|ལོ་རྒྱུས།|ལྟ་གྲུབ།|རྩོམ་རིག|གསོ་རིག|ཆབ་སྲིད།|ཚན་རིག|བཟོ་རིག|རྩིས་རིག|ཁྲིམས་ལུགས།|དཔལ་འབྱོར།|དམག་དོན།|འཛིན་སྐྱོང་།|སྒྲ་རིག་པ།|ཤེས་ཡོན།|སློབ་གསོ།|ཚད་མ།|ཚད་མ་རིག་པ།|སྐྱེ་དངོས་རིག་པ།|ཟུར་ཆག|རྒྱ་གར།|རྒྱ་ནག|རྒྱ་ནག།|སོག་པོ།|མན་ཇུ།|དབྱིན་ཇི།|བལ་བོ།|མིང་གི་རྣམ་གྲངས།|མིང་གི་གྲངས།|མིང་གི་རྣམ་གྲངས་ལ།|ལྡོག་ཚིག|ལྡོག་ཚིིག|ལྡོག་ཚིག|ཉེ་ཚིག|ཟུར་མཆན།|ཡུལ་སྐད།|ཞེ་ས།|བརྙས་ཚིག|ལོག་སྐད།|དཔེ་ཆོས།|མངོན་བརྗོད།|བརྡ་རྙིང་།|བསྡུས་ཚིག|རྒྱུན་སྤྱོད།|བསྡུར་རིམ།|མ་འོངས་པ།|མ་འོངས།|ད་ལྟ་བ་།|ད་ལྟ་བ།|འདས་པ།|འདས།|སྐུ་ཚིག|སྐུར་ཚིག|སྐུལ་ཚིག|སྐུལ་ཚིག།|སྐུུལ་ཚིག) ', line)
    tag = re.findall(r'\| +(ཕྲད་ཚིག) ', line)
    if tag != []:
        #truc = re.sub(r'([^༡༢])(ཆོས་ལུགས།|ལོ་རྒྱུས།|ལྟ་གྲུབ།|རྩོམ་རིག|གསོ་རིག|ཆབ་སྲིད།|ཚན་རིག|བཟོ་རིག|རྩིས་རིག|ཁྲིམས་ལུགས།|དཔལ་འབྱོར།|དམག་དོན།|འཛིན་སྐྱོང་།|སྒྲ་རིག་པ།|ཤེས་ཡོན།|སློབ་གསོ།|ཚད་མ།|ཚད་མ་རིག་པ།|སྐྱེ་དངོས་རིག་པ།|ཟུར་ཆག|རྒྱ་གར།|རྒྱ་ནག|རྒྱ་ནག།|སོག་པོ།|མན་ཇུ།|དབྱིན་ཇི།|བལ་བོ།|མིང་གི་རྣམ་གྲངས།|མིང་གི་གྲངས།|མིང་གི་རྣམ་གྲངས་ལ།|ལྡོག་ཚིག|ལྡོག་ཚིིག|ལྡོག་ཚིག|ཉེ་ཚིག|ཟུར་མཆན།|ཡུལ་སྐད།|ཞེ་ས།|བརྙས་ཚིག|ལོག་སྐད།|དཔེ་ཆོས།|མངོན་བརྗོད།|བརྡ་རྙིང་།|བསྡུས་ཚིག|རྒྱུན་སྤྱོད།|བསྡུར་རིམ།|མ་འོངས་པ།|མ་འོངས།|ད་ལྟ་བ་།|ད་ལྟ་བ།|འདས་པ།|འདས།|སྐུ་ཚིག|སྐུར་ཚིག|སྐུལ་ཚིག|སྐུལ་ཚིག།|སྐུུལ་ཚིག) ', r'\1༡\2 ', line)
        truc = re.sub('\|( +)(ཕྲད་ཚིག) ', r'\1༡\2 ', line)
        num_inserted.append(str(num)+truc)
        num_missing.append(str(num)+line)
with open('monlam_num_missing.txt', 'w', -1, 'utf-8-sig') as f:
    for line in num_missing:
        f.write(line+'\n')
with open('monlam_num_inserted.txt', 'w', -1, 'utf-8-sig') as f:
    for line in num_inserted:
        f.write(line+'\n')


# to do : compare in Meld the two, put a '*' at the beginning of each line where the ༡ is not necessary, and delete the extra ones in lines where needed. Save the files in the monlam folder to not risk delete the work.

# In[ ]:

with open('./monlam/monlam_num_inserted.txt', 'r', -1, 'utf-8-sig') as f:
    inserted = [line.strip() for line in f.readlines()]
monlam_corrected = content0

# replace the bad entries by the ones from monlam_num_inserted.txt
for line in inserted:
    if not line.startswith('*'):
        entry = [i for i in re.split('^([0-9]+)', line) if i != '']
        monlam_corrected[int(entry[0])] = entry[1]

with open('monlam1_total_corrected.txt', 'w', -1, 'utf-8-sig') as f:
    for line in monlam_corrected:
        f.write(line+'\n')


# ### Insert the modifications in monlam_errors.txt and save the file. The file is ready to be parsed !

# In[1]:

import re


# In[2]:

with open('monlam1_total_corrected.txt', 'r', -1, 'utf-8-sig') as f:
    content1 = [line.strip() for line in f.readlines()]


# ### Verbs

# In[3]:

verbs = []
rest = []
for line in content1:
    if '༡བྱ་ཚིག' in line and '༡རྒྱ་གར།' not in line:
        verbs.append(line)
    else:
        rest.append(line)


# In[4]:

# shows the entry
def show_entry(string):
    for line in content1:
        if line.startswith(string+'་ '):
            print(line)


# In[5]:

def isRef(string):
    test = False
    if re.findall(r'[^༡༢](མ་འོངས་པ།|ད་ལྟ་བ།|འདས་པ།|སྐུལ་ཚིག)', string):
        test = True
    return test


# In[6]:

def add2dict(key, value, dic):
    if key not in dic.keys():
        dic[key] = value
    else:
        dic[key] = list(set(dic[key] + value))


# In[7]:

thadepa = 'ཐ་དད་པ'
thamidepa = 'ཐ་མི་དད་པ'
zugmigyur = 'གཟུགས་མི་འགྱུར་བ'
empty = '###'
unknown = 'བྱ་ཚིག'
attr_sep = '_'
pos_sep = '+'

verbs_dict = {}
for verb in verbs:
    # separate the entry and the description
    parts = verb.split(' | ')
    lemma = parts[0].strip().replace('་', '')
    
    # separate all sub-entries
    sub_entries = re.split(r'༡(མིང|བྱ|རྒྱན|བསྣན|ཚབ|མཚུངས|སྒྲུབ|ཕྲད|འབོད|གྲངས|འཇལ|གྲོགས)་ཚིག', parts[1])
    # only keep the verb sub-entry
    sub = ''
    for i in range(len(sub_entries)):
        if sub_entries[i] == 'བྱ':
            sub = sub_entries[i+1]
    
    # separate meanings
    meanings = re.split(r' [0-9]+\. ', sub)
    
    # keep only verbs that are not references
    #new_meanings = [m.strip() for m in meanings if not isRef(m) and m != '']
    new_meanings = [m.strip() for m in meanings if m != '']
    
    if new_meanings != []:
        for meaning in new_meanings:
            #print(lemma, meaning)
            # ཐ་དད་པ་ or ཐ་མི་དད་པ་
            tha = empty
            
            if  'བྱ་བྱེད་ཐ་མི་དད་པ། ' in meaning: tha = thamidepa
            elif 'བྱ་བྱེད་ཐ་དད་པ། ' in meaning: tha = thadepa
            
            # tenses
            if ' གཟུགས་མི་འགྱུར་བ། ' in meaning:
                add2dict(lemma, [zugmigyur+attr_sep+tha], verbs_dict)
                #print({lemma : zugmigyur+attr_sep+tha})
            else:
                if 'མ་འོངས་པ།' in meaning or 'ད་ལྟ་བ།' in meaning or 'འདས་པ།' in meaning or 'སྐུལ་ཚིག' in meaning:
                    if re.findall('(གི|ཀྱི|གྱི|ཡི|གིས|ཀྱིས|གྱིས|ཡིས)་(མ་འོངས་པ།|མ་འོངས།|ད་ལྟ་བ་།|ད་ལྟ་བ།|ལྟ་བ།|འདས་པ།|འདས།|སྐུ་ཚིག|སྐུར་ཚིག|སྐུལ་ཚིག|སྐུལ་ཚིག།|སྐུུལ་ཚིག) ', meaning) == []:
                        tenses = re.findall(r'.(མ་འོངས་པ།|མ་འོངས།) ([^་\s]+་?[ག།]) .(ད་ལྟ་བ་།|ད་ལྟ་བ།|ལྟ་བ།) ([^་\s]+་?[ག།]) .(འདས་པ།|འདས།) ([^་\s]+་?[ག།]) ?.?(སྐུ་ཚིག|སྐུར་ཚིག|སྐུལ་ཚིག|སྐུལ་ཚིག།|སྐུུལ་ཚིག)? ?([^་\s]+་?[ག།])?', meaning)

                        ############################
                        # hack because of a strange behaviour of python : the structure of tenses is a tuple embedded in a list
                        for t in tenses: 
                            temp = []
                            for elt in t:
                                if elt != '':
                                    temp.append(elt)
                        tenses = temp
                        temp = []
                        #
                        ############################

                        #print(tenses)
                        for i in range(0, len(tenses)-1, 2):
                            inflected = tenses[i+1].replace('།', '').replace('་', '')
                            tense = tenses[i]
                            add2dict(inflected, [lemma+attr_sep+tense+attr_sep+tha], verbs_dict)
                            #print({inflected : lemma+attr_sep+tense+attr_sep+tha})
                        # empty the tenses list for the next verb
                        tenses = []
                else:
                    add2dict(lemma, [unknown+attr_sep+tha], verbs_dict)
                    #print({lemma : unknown+attr_sep+tha})
    


# ### Alternative Verbs

# #### find all alternatives

# In[ ]:

alternative = []
for verb in verbs:
    if 'འབྲི་ཚུལ་' in verb:
        alternative.append(verb)


# In[ ]:

with open('alternative_verbs.txt', 'w', -1, 'utf-8-sig') as f:
    for line in alternative:
        f.write(line+'\n')


# In[ ]:

print(len(alternative))


# #### apply alternatives to verbs_dict

# In[8]:

with open('./monlam/alternative_verbs.txt', 'r', -1, 'utf-8-sig') as f:
    alt_content = [line.strip() for line in f.readlines()]


# In[9]:

for verb in alt_content:
    parts = verb.split(' = ')
    lemma = parts[0]
    pos = parts[1]+'_འབྲི་ཚུལ'
    if lemma in verbs_dict.keys():
        verbs_dict[lemma] = verbs_dict[lemma] + [pos]
        #print(lemma, verbs_dict[lemma])
    else:
        verbs_dict[lemma] = [pos]
        #print(verbs_dict[lemma])


# In[10]:

verbs_dict['ཕྲུལ']


# In[11]:

# flatten the pos list into a string
for v in verbs_dict.keys():
    flattened = '+'.join(list(set(verbs_dict[v])))
    verbs_dict[v] = flattened


# In[12]:

with open('monlam1_verbs.txt', 'w', -1, 'utf-8-sig') as f:
    for verb in sorted(verbs_dict.keys()):
        f.write(verb+' | '+verbs_dict[verb]+'\n')


# ## Other tags

# In[12]:

no_pos = []
pos_tagged = []
for entry in content1:
    # separate the entry and the description
    parts = entry.split(' | ')
    lemma = parts[0].strip()
    if lemma.endswith('་'):
        lemma = lemma[:-1]
    # separate all sub-entries
    sub_entries = re.split(r'༡(མིང|བྱ|རྒྱན|བསྣན|ཚབ|མཚུངས|སྒྲུབ|ཕྲད|འབོད|གྲངས|འཇལ|གྲོགས)་ཚིག', parts[1])
    
    # only keep the verb sub-entry
    sub = []
    for i in range(len(sub_entries)):
        if sub_entries[i] == 'བྱ' and '༡རྒྱ་གར།' not in sub_entries[i+1]:
            if lemma not in verbs_dict.keys():
                print(lemma, end= ' ')
            else:
                sub.append('བྱ་ཚིག:'+verbs_dict[lemma])
        else:
            if sub_entries[i] in ['མིང', 'བྱ', 'རྒྱན', 'བསྣན', 'ཚབ', 'མཚུངས', 'སྒྲུབ', 'ཕྲད', 'འབོད', 'གྲངས', 'འཇལ', 'གྲོགས']:
                tags = re.findall(r'[། ]?[^་ ](ཆོས་ལུགས།|ལོ་རྒྱུས།|ལྟ་གྲུབ།|རྩོམ་རིག|གསོ་རིག|ཆབ་སྲིད།|ཚན་རིག|བཟོ་རིག|རྩིས་རིག|ཁྲིམས་ལུགས།|དཔལ་འབྱོར།|དམག་དོན།|འཛིན་སྐྱོང་།|སྒྲ་རིག་པ།|ཤེས་ཡོན།|སློབ་གསོ།|ཚད་མ།|ཚད་མ་རིག་པ།|སྐྱེ་དངོས་རིག་པ།|ཟུར་ཆག|རྒྱ་གར།|རྒྱ་ནག|རྒྱ་ནག།|སོག་པོ།|མན་ཇུ།|དབྱིན་ཇི།|བལ་བོ།|མིང་གི་རྣམ་གྲངས།|མིང་གི་གྲངས།|མིང་གི་རྣམ་གྲངས་ལ།|ལྡོག་ཚིག|ལྡོག་ཚིིག|ལྡོག་ཚིག|ཉེ་ཚིག|ཟུར་མཆན།|ཡུལ་སྐད།|ཞེ་ས།|བརྙས་ཚིག|ལོག་སྐད།|དཔེ་ཆོས།|མངོན་བརྗོད།|བརྡ་རྙིང་།|བསྡུས་ཚིག|རྒྱུན་སྤྱོད།|བསྡུར་རིམ།|མ་འོངས་པ།|མ་འོངས།|ད་ལྟ་བ་།|ད་ལྟ་བ།|འདས་པ།|འདས།|སྐུ་ཚིག|སྐུར་ཚིག|སྐུལ་ཚིག|སྐུལ་ཚིག།|སྐུུལ་ཚིག) ', sub_entries[i+1])
                sub.append(sub_entries[i]+'་ཚིག:'+'_'.join(tags))
    
    total_tags = '/'.join(sub)
    if total_tags != '':
        pos_tagged.append(lemma+'—'+total_tags)
    else:
        no_pos.append(entry)


# In[ ]:

verbs_dict['']


# In[13]:

with open('monlam1_pos.txt', 'w', -1, 'utf-8-sig') as f:
    f.write('\n'.join(pos_tagged))
with open('monlam1_no_pos.txt', 'w', -1, 'utf-8-sig') as f:
    f.write('\n'.join(no_pos))


# In[ ]:

for truc in ['གདིང', 'གནན', 'གྲུས', 'ཆུམ', 'ཉར', 'ཉོར', 'དགོག', 'དགྱེད', 'དབྲབ', 'ཕིག', 'ཕྲད', 'ཕྲུལ', 'ཕྲོས', 'བཀོག', 'བང', 'བངས', 'བཅོ', 'བཏིངས', 'བཙགས', 'བཟབ', 'བརྒྱུ', 'བརྒྱུས', 'བརྟིབ', 'བརྟིབས', 'བཤག', 'བཤགས', 'བསྒོངས', 'བསྒོངས', 'བསྒྲོག', 'བསྒྲོགས', 'བསླ', 'བསླས', 'ཚོལ', 'ཟླུམས', 'འཁྲིས', 'འགེལ', 'འཆགས', 'འཆོགས', 'འཆོབས', 'འཇབས', 'འཇས', 'འཐུས', 'འདིང', 'འདོས', 'འདྲུབས', 'འཕྱོགས', 'འཕྲད', 'འཚོབས', 'རྐོམས', 'རྒྱུད', 'རྒྱུས', 'རྟིབས', 'ལྟུང', 'ལྟུངས', 'ལྡིང', 'ལྡིང', 'ཤོགས', 'སྒོང', 'སྒོངས', 'སྨྲོས', 'སྲོགས']:
    show_entry(truc)


# In[ ]:

show_entry('ཉོར')
verbs_dict['བཤག']


# ### basic tags

# In[ ]:

import re


# In[ ]:

with open('monlam1_pos.txt', 'r', -1, 'utf-8-sig') as f:
    content2 = [line.strip() for line in f.readlines()]

basic_pos = {}
for line in content2:
    parts = line.split('—')
    form = parts[0]
    pos = re.findall(r' ?([^ \:]+)\:', parts[1])
    basic_pos[form] = pos
    


# In[ ]:

with open('monlam1_verbs.txt', 'r', -1, 'utf-8-sig') as f:
    content3 = [line.strip() for line in f.readlines()]


# In[ ]:

verb_tenses = {}
for verb in content3:
    entry = verb.split(' | ')
    form = entry[0]
    tags = entry[1].split('+')
    pos = []
    for tag in tags:
        parts = tag.split('_')
        if len(parts) == 3:
            pos.append(parts[1])
        if len(parts) == 2:
            pos.append(parts[0])
    pos = list(set(pos))
    verb_tenses[form] = '-'.join(pos)
#print(verb_tenses)


# In[ ]:

for entry in basic_pos.keys():
    for num, pos in enumerate(basic_pos[entry]):
        if pos == 'བྱ་ཚིག' and entry in verb_tenses.keys():
            basic_pos[entry][num] = basic_pos[entry][num] +'|'+ verb_tenses[entry]


# In[ ]:

with open('monlam1_basic_pos.txt', 'w', -1, 'utf-8-sig') as f:
    for entry in sorted(basic_pos.keys()):
        f.write(entry+'\t'+'_'.join(basic_pos[entry])+'\n')


# In[ ]:



