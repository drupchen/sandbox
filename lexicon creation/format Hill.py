
# coding: utf-8

# # Hill Lexicon

# In[ ]:

with open('./2016-04-06-uncompound_lexicon.txt', 'r', -1, 'utf-8-sig') as f:
    content = [line.strip() for line in f.readlines()]


# In[ ]:

lexicon = {}
for line in content:
    parts = line.split('\t')
    entry = parts[0]
    pos = [elt.strip(' -') for elt in parts[1:]]
    if entry.endswith('་'):
        entry = entry[:-1]
    if entry in lexicon.keys():
        for p in pos:
            if p not in lexicon[entry]:
                lexicon[entry].append(p)
    else:
        lexicon[entry] = pos


# In[ ]:

flat_lexicon = {}
for entry in lexicon.keys():
    flat_lexicon[entry] = '_'.join(lexicon[entry])


# In[ ]:

pos_list = []
for entry in lexicon.keys():
    pos_list.extend(lexicon[entry])
pos_set = set(pos_list)


# In[ ]:

print(sorted(pos_set))


# In[ ]:

with open('hill_lexicon.txt', 'w', -1, 'utf-8-sig') as f:
    for entry in no_prop.keys():
        f.write(entry+'***'+no_prop[entry]+'\n')


# In[ ]:

cases = {}
for entry in flat_lexicon.keys():
    pos = flat_lexicon[entry]
    if 'case' in pos and 'cv' not in pos:
        print('nocv: ', entry, pos)
    #elif 'case' not in pos and 'cv' in pos:
     #   print('nocase: ', entry, pos)


# In[ ]:

for entry in flat_lexicon.keys():
    pos = flat_lexicon[entry]
    if 'case' not in pos and 'cv' in pos:
        print('nocase: ', entry, pos)


# In[ ]:

no_prop = {}
prop = []
for entry in flat_lexicon.keys():
    pos = flat_lexicon[entry]
    if 'prop' in pos:
        prop.append(entry)
    else:
        no_prop[entry] = pos


# In[ ]:

print(prop)


# In[ ]:

len(one_pos)


# In[ ]:

len(flat_lexicon)


# In[ ]:

22279-15963


# In[ ]:

6316*100/22279

