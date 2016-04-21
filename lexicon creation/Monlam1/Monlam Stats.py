
# coding: utf-8

# In[3]:

import re


# In[5]:

with open('../monlam1_basic_pos.txt', 'r', -1, 'utf-8-sig') as f:
    content = [line.strip() for line in f.readlines()]


# In[31]:

syls_num = {}
for line in content:
    entry = line.split('\t')[0]
    syls = re.findall('་', entry)
    len_syls = len(syls)+1
    if len_syls == 51:
        print(line)
    if len_syls in syls_num.keys():
        syls_num[len_syls] = syls_num[len_syls]+1
    else:
        syls_num[len_syls] = 1
     


# In[30]:

print('syls\toccurences\tpercentage\nin word\n')
for Type in sorted(syls_num.keys()):
    print(str(Type)+'\t'+str(syls_num[Type])+'\t\t'+str(syls_num[Type] * 100 / len(content)))


# In[11]:

syls_num


# In[19]:

len(content)


# In[1]:

with open('./monlam1_verbs.txt', 'r', -1, 'utf-8-sig') as f:
    content1 = [line.strip() for line in f.readlines()]


# In[4]:

pos_num = {}
for line in content1:
    entry = line.split(' | ')[1]
    pos = re.findall('\+', entry)
    len_pos = len(pos)+1
    if len_pos == 18 or len_pos == 14 or len_pos == 13:
        print(line)
    if len_pos in pos_num.keys():
        pos_num[len_pos] = pos_num[len_pos]+1
    else:
        pos_num[len_pos] = 1


# In[5]:

print('pos per\t\toccurences\tpercentage\nverb form\n')
for Type in sorted(pos_num.keys()):
    print(str(Type)+'\t\t'+str(pos_num[Type])+'\t\t'+str(pos_num[Type] * 100 / len(content1)))


# In[ ]:



