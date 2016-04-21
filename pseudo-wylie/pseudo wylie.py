
# coding: utf-8

# In[1]:

import re


# In[2]:

class pseudoWylie:
    '''to and from pseudo Wylie'''
    
    def __init__(self, string):    
        self.string = string
        
        # characters inserted by converting unicode into wylie
        self.nonwylie_separator = '\[\#\]'
        self.space = ' '
        self.new_nonwylie = ' [#]'

        self.punct_beginning = r'([\@\u0fd3][\#\u0fd4]+[\/_]+|[\%\$\!]+)' #["༄", "༅", "࿓", "࿔", "༇", "༆", "༈"]
        self.p_b_punct = '*'
        self.new_beginning = '@#/_/'

        self.punct_separators = r'(\/_\/(?!\/)|\/\/?\_?(?!\/\/)|\;\_\;|\u0f10\_\u0f10|\|\_\||\:\_)' # [" ", "།", "༎", "༏", "༐", "༑", "༔"]
        self.p_m_punct = ';'
        self.new_middle = '/_/'

        self.punct_other = r'[\(\)\u0f12\u0f13]+' # ["༼", "༽", "༒", "༓"]
        self.p_o_punct = '-'
        self.new_other = ''

        self.w_e_punct = '//_//'
        self.p_e_punct = '.'
        self.new_end = '//_//'
        
        self.syl_punct = r'[\u0f7f \*]+' # ["་", "༌", "ཿ"]
        self.w_space = 'X'

        self.w_aa = "'"
        self.p_aa = 'v'

        self.w_plus = '+'
        self.p_plus = 'x'

    def from_p_w(self):
        words = self.string.replace(self.space, self.new_nonwylie)
        spaces = words.replace(self.w_space, self.space)
        aa = spaces.replace(self.p_aa, self.w_aa)
        b_punct = aa.replace(self.p_b_punct, self.new_beginning)
        m_punct = b_punct.replace(self.p_m_punct, self.new_middle)
        o_punct = m_punct.replace(self.p_o_punct, self.new_other)
        e_punct = o_punct.replace(self.p_e_punct, self.new_end)
        plus = e_punct.replace(self.p_plus, self.w_plus)
        return plus

    def to_p_w(self):
        spaces = re.sub(self.syl_punct, self.w_space, self.string) # inter-word spaces
        words = re.sub(r''+self.w_space+'*'+self.nonwylie_separator, self.space, spaces)
        aa = words.replace(self.w_aa, self.p_aa) # ' > v
        b_punct = re.sub(self.punct_beginning, self.p_b_punct, aa)
        m_punct = re.sub(self.punct_separators, self.p_m_punct, b_punct) # middle punctuation > ;
        o_punct = re.sub(self.punct_other, self.p_o_punct, m_punct) # other punct > -
        e_punct = o_punct.replace(self.w_e_punct, self.p_e_punct) # add ending punctuation
        plus = e_punct.replace(self.w_plus, self.p_plus) # + > f
        extra_spaces = re.sub(r''+self.w_space+'([\\'+self.p_m_punct+'\\'+self.p_e_punct+'\\'+self.p_o_punct+'\\'+self.p_b_punct+'])', r'\1', plus) # remove spaces (x) in front of punctuation
        return extra_spaces


# In[3]:

with open('A1_wylie.txt', 'r', -1, 'utf-8-sig') as f:
    content = [line.strip() for line in f.readlines()]


# In[18]:

for line in content:
    li = pseudoWylie(line).to_p_w()
    print(li)
    print(line)
    print(pseudoWylie(li).from_p_w())
    print()


# In[ ]:



