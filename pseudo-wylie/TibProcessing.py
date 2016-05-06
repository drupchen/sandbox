
# coding: utf-8

# In[1]:

import re


# In[2]:

class SylComponents:
    '''
    takes a syllable as input
    outputs:
        (prefix+main-stack, vowel+suffixes)
        (exceptions, x) 
        a list of solutions if there is more than one
        None if the syllable is not wellformed
    '''

    def __init__(self):
        # roots is an import from root + rareC and wazurC and suffixes is the 'AB' entry from  suffixes.json
        # all dicts from https://github.com/eroux/tibetan-spellchecker/tree/master/syllables
        self.Aroots  = ['ཀ', 'ཀྱ', 'ཀྲ', 'ཀླ', 'ཁ', 'ཁྱ', 'ཁྲ', 'ག', 'གཏྲ', 'གྱ', 'གྲ', 'གླ', 'ང', 'ཅ', 'ཆ', 'ཇ', 'ཉ', 'ཏ', 'ཏྲ', 'ཐ', 'ཐྲ', 'ད', 'དཀྱ', 'དཀྲ', 'དཀླ', 'དགྱ', 'དགྲ', 'དཔྱ', 'དཔྲ', 'དབྱ', 'དབྲ', 'དམྱ', 'དམྲ', 'དྲ', 'ན', 'པ', 'པྱ', 'པྲ', 'ཕ', 'ཕྱ', 'ཕྲ', 'བ', 'བཀྱ', 'བཀྲ', 'བཀླ', 'བགྱ', 'བགྲ', 'བཏྲ', 'བཟླ', 'བརྐ', 'བརྐྱ', 'བརྒ', 'བརྒྱ', 'བརྔ', 'བརྗ', 'བརྙ', 'བརྟ', 'བརྡ', 'བརྣ', 'བརྩ', 'བརྫ', 'བརླ', 'བལྟ', 'བལྡ', 'བསྐ', 'བསྐྱ', 'བསྐྲ', 'བསྒ', 'བསྒྱ', 'བསྒྲ', 'བསྔ', 'བསྙ', 'བསྟ', 'བསྡ', 'བསྣ', 'བསྩ', 'བསྲ', 'བསླ', 'བྱ', 'བྲ', 'བླ', 'མ', 'མཁྱ', 'མཁྲ', 'མགྱ', 'མགྲ', 'མྱ', 'མྲ', 'ཙ', 'ཚ', 'ཛ', 'ཝ', 'ཞ', 'ཟ', 'ཟླ', 'འ', 'འཁྱ', 'འཁྲ', 'འགྱ', 'འགྲ', 'འདྲ', 'འཕྱ', 'འཕྲ', 'འབྱ', 'འབྲ', 'ཡ', 'ར', 'རྐ', 'རྐྱ', 'རྒ', 'རྒྱ', 'རྔ', 'རྗ', 'རྙ', 'རྟ', 'རྡ', 'རྣ', 'རྦ', 'རྨ', 'རྨྱ', 'རྩ', 'རྫ', 'རླ', 'ལ', 'ལྐ', 'ལྒ', 'ལྔ', 'ལྕ', 'ལྗ', 'ལྟ', 'ལྡ', 'ལྤ', 'ལྦ', 'ལྷ', 'ཤ', 'ས', 'སྐ', 'སྐྱ', 'སྐྲ', 'སྒ', 'སྒྱ', 'སྒྲ', 'སྔ', 'སྙ', 'སྟ', 'སྡ', 'སྣ', 'སྣྲ', 'སྤ', 'སྤྱ', 'སྤྲ', 'སྦ', 'སྦྱ', 'སྦྲ', 'སྨ', 'སྨྱ', 'སྨྲ', 'སྩ', 'སྲ', 'སླ', 'ཧ', 'ཧྲ', 'ཨ']
        self.NBroots = ['གཅ', 'གཉ', 'གཏ', 'གད', 'གན', 'གཙ', 'གཞ', 'གཟ', 'གཡ', 'གཤ', 'གས', 'དཀ', 'དག', 'དང', 'དཔ', 'དབ', 'དམ', 'བཀ', 'བག', 'བཅ', 'བཏ', 'བད', 'བཙ', 'བཞ', 'བཟ', 'བཤ', 'བས', 'མཁ', 'མག', 'མང', 'མཆ', 'མཇ', 'མཉ', 'མཐ', 'མད', 'མན', 'མཚ', 'མཛ', 'འཁ', 'འག', 'འཆ', 'འཇ', 'འཐ', 'འད', 'འཕ', 'འབ', 'འཚ', 'འཛ']
        self.Croots  = ['ཀའུ', 'ཀིའུ', 'ཀེའུ', 'ཀོའུ', 'ཀྭ', 'ཀྭའི', 'ཀྲུའུ', 'ཁེའུ', 'ཁྭ', 'ཁྱིའུ', 'ཁྱེའུ', 'ཁྲིའུ', 'ཁྲུའུ', 'ཁྲེའུ', 'གཅིའུ', 'གཅེའུ', 'གཏེའུ', 'གཙེའུ', 'གཞུའུ', 'གའུ', 'གཡིའུ', 'གྭ', 'གྲིའུ', 'གྲེའུ', 'གྲྭ', 'གླེའུ', 'ཉེའུ', 'ཉྭ', 'ཏེའུ', 'ཐིའུ', 'ཐུའུ', 'ཐེའུ', 'ཐོའུ', 'དཔེའུ', 'དུའུ', 'དེའུ', 'དྭ', 'དྭོ', 'དྲེའུ', 'དྲྭ', 'ནའུ', 'ནེའུ', 'ནོའུ', 'པདྨ', 'ཕེའུ', 'ཕྱྭ', 'ཕྲའུ', 'ཕྲེའུ', 'བསེའུ', 'བསྭ', 'བསྭོ', 'བེའུ', 'བྱའུ', 'བྱིའུ', 'བྱེའུ', 'བྲའུ', 'བྲའོ', 'བྲེའུ', 'བྲོའུ', 'མཐེའུ', 'མདེའུ', 'མཚེའུ', 'མིའུ', 'མུའུ', 'མོའུ', 'མྱིའུ', 'ཙིའུ', 'ཙེའུ', 'ཚའུ', 'ཚུའུ', 'ཚེའུ', 'ཚྭ', 'ཞྭ', 'ཟེའུ', 'ཟྭ', 'འགིའུ', 'འགོའུ', 'འཕེའུ', 'འབེའུ', 'ཡེའུ', 'རེའུ', 'རྒེའུ', 'རྔེའུ', 'རྗེའུ', 'རྟའུ', 'རྟེའུ', 'རྡེའུ', 'རྨེའུ', 'རྩེའུ', 'རྩྭ', 'རྫིའུ', 'རྫེའུ', 'རྭ', 'ལའུ', 'ལིའུ', 'ལེའུ', 'ལོའུ', 'ལྕེའུ', 'ལྭ', 'ཤའུ', 'ཤེའུ', 'ཤྭ', 'སིའུ', 'སེའུ', 'སྒའུ', 'སྒེའུ', 'སྒྱེའུ', 'སྒྲེའུ', 'སྔེའུ', 'སྙེའུ', 'སྟེའུ', 'སྟྭ', 'སྡེའུ', 'སྣེའུ', 'སྤའུ', 'སྤེའུ', 'སྤྱིའུ', 'སྤྲེའུ', 'སྦྲེའུ', 'སྨེའུ', 'སྭ', 'སྲིའུ', 'སླེའུ', 'སླེའོ', 'ཧུའུ', 'ཧེའུ', 'ཧྭ', 'ཧྲུའུ']

        suffixes =      ['ག', 'གས', 'ང', 'ངས', 'ད', 'ན', 'བ', 'བས', 'མ', 'མས', 'ལ', 'འི', 'འོ', 'འང', 'འམ', 'ར', 'ས',
                     'ི', 'ིག', 'ིགས', 'ིང', 'ིངས', 'ིད', 'ིན', 'ིབ', 'ིབས', 'ིམ', 'ིམས', 'ིལ', 'ིའི', 'ིའོ', 'ིའང', 'ིའམ', 'ིར', 'ིས',
                     'ུ', 'ུག', 'ུགས', 'ུང', 'ུངས', 'ུད', 'ུན', 'ུབ', 'ུབས', 'ུམ', 'ུམས', 'ུལ', 'ུའི', 'ུའོ', 'ུའང', 'ུའམ', 'ུར', 'ུས',
                     'ེ', 'ེག', 'ེགས', 'ེང', 'ེངས', 'ེད', 'ེན', 'ེབ', 'ེབས', 'ེམ', 'ེམས', 'ེལ', 'ེའི', 'ེའོ', 'ེའང', 'ེའམ', 'ེར', 'ེས',
                     'ོ', 'ོག', 'ོགས', 'ོང', 'ོངས', 'ོད', 'ོན', 'ོབ', 'ོབས', 'ོམ', 'ོམས', 'ོལ', 'ོའི', 'ོའོ', 'ོའང', 'ོའམ', 'ོར', 'ོས']
        self.Asuffixes = ['འ'] + suffixes
        self.NBsuffixes = [''] + suffixes
        self.Csuffixes =  ['','འི', 'འོ', 'འང', 'འམ', 'ར', 'ས']

        special = ['བགླ', 'མདྲོན', 'བརྡའ', 'བརྟའ']
        wazurs = ['ཧྭག', 'ཀྭས', 'ཁྭངས', 'ཧྭང', 'ཀྭན', 'དྭགས', 'ཧྭགས', 'དྭངས', 'ཏྭོན']
        self.exceptions = special + wazurs
        self.ambiguous = {'མངས' : ('མ', 'ངས'), 'མགས' : ('མ', 'གས'), 'དབས' : ('ད', 'བས'), 'དངས' : ('ད', 'ངས'), 'དགས' : ('དག', 'ས'), 'དམས' : ('དམ', 'ས'), 'བགས' : ('བ', 'གས'), 'འབས' : ('འབ', 'ས'), 'འགས' : ('འག', 'ས')}

    def get(self, syl):
        solutions = []
        if syl in self.exceptions:
            solutions.append((syl, 'x'))
        elif syl in self.ambiguous:
            solutions.append(self.ambiguous[syl])
        else:
            for i in range(len(syl)+1):
                if len(syl) > i+1 and syl[i+1] not in ('ག', 'ང', 'ད', 'ན', 'བ', 'མ', 'འ', 'ར', 'ལ', 'ས'): continue
                root = syl[0:i]
                suf = syl[i:]
                if (suf in self.Asuffixes and root in self.Aroots) or (root in self.NBroots and suf in self.NBsuffixes) or (suf in self.Csuffixes and root in self.Croots):
                    solutions.append((root, suf))

        if len(solutions) > 1:
            return solutions
        if len(solutions) == 1:
            return solutions[0]
        if solutions == []:
            return None

class Mingzhi():
    def __init__(self):
        # dict of roots with their corresponding mingzhi
        self.roots = {'ཀ' : 'ཀ', 'ཀྱ' : 'ཀ', 'ཀྲ' : 'ཀ', 'ཀླ' : 'ལ', 'དཀ' : 'ཀ', 'དཀྱ' : 'ཀ', 'དཀྲ' : 'ཀ', 'དཀླ' : 'ལ', 'བཀ' : 'ཀ', 'བཀྱ' : 'ཀ', 'བཀྲ' : 'ཀ', 'བཀླ' : 'ླ', 'རྐ' : 'ྐ', 'རྐྱ' : 'ྐ', 'ལྐ' : 'ྐ', 'སྐ' : 'ྐ', 'སྐྱ' : 'ྐ', 'སྐྲ' : 'ྐ', 'བརྐ' : 'ྐ', 'བརྐྱ' : 'ྐ', 'བསྐ' : 'ྐ', 'བསྐྱ' : 'ྐ', 'བསྐྲ' : 'ྐ', 'ཁ' : 'ཁ', 'ཁྱ' : 'ཁ', 'ཁྲ' : 'ཁ', 'མཁ' : 'ཁ', 'མཁྱ' : 'ཁ', 'མཁྲ' : 'ཁ', 'འཁ' : 'ཁ', 'འཁྱ' : 'ཁ', 'འཁྲ' : 'ཁ', 'ག' : 'ག', 'གྱ' : 'ག', 'གྲ' : 'ག', 'གླ' : 'ླ', 'དག' : 'ག', 'དགྱ' : 'ག', 'དགྲ' : 'ག', 'བག' : 'ག', 'བགྱ' : 'ག', 'བགྲ' : 'ག', 'མག' : 'ག', 'མགྱ' : 'ག', 'མགྲ' : 'ག', 'འག' : 'ག', 'འགྱ' : 'ག', 'འགྲ' : 'ག', 'རྒ' : 'ྒ', 'རྒྱ' : 'ྒ', 'ལྒ' : 'ྒ', 'སྒ' : 'ྒ', 'སྒྱ' : 'ྒ', 'སྒྲ' : 'ྒ', 'བརྒ' : 'ྒ', 'བརྒྱ' : 'ྒ', 'བསྒ' : 'ྒ', 'བསྒྱ' : 'ྒ', 'བསྒྲ' : 'ྒ', 'ང' : 'ང', 'དང' : 'ང', 'མང' : 'ང', 'རྔ' : 'ྔ', 'ལྔ' : 'ྔ', 'སྔ' : 'ྔ', 'བརྔ' : 'ྔ', 'བསྔ' : 'ྔ', 'ཅ' : 'ཅ', 'གཅ' : 'ཅ', 'བཅ' : 'ཅ', 'ལྕ' : 'ྕ', 'ཆ' : 'ཆ', 'མཆ' : 'ཆ', 'འཆ' : 'ཆ', 'ཇ' : 'ཇ', 'མཇ' : 'ཇ', 'འཇ' : 'ཇ', 'རྗ' : 'ྗ', 'ལྗ' : 'ྗ', 'བརྗ' : 'ྗ', 'ཉ' : 'ཉ', 'གཉ' : 'ཉ', 'མཉ' : 'ཉ', 'རྙ' : 'ྙ', 'སྙ' : 'ྙ', 'བརྙ' : 'ྙ', 'བསྙ' : 'ྙ', 'ཏ' : 'ཏ', 'ཏྲ' : 'ཏ', 'གཏ' : 'ཏ', 'གཏྲ' : 'ཏ', 'བཏ' : 'ཏ', 'བཏྲ' : 'ཏ', 'རྟ' : 'ྟ', 'ལྟ' : 'ྟ', 'སྟ' : 'ྟ', 'བརྟ' : 'ྟ', 'བལྟ' : 'ྟ', 'བསྟ' : 'ྟ', 'ཐ' : 'ཐ', 'ཐྲ' : 'ཐ', 'མཐ' : 'ཐ', 'འཐ' : 'ཐ', 'ད' : 'ད', 'དྲ' : 'ད', 'གད' : 'ད', 'བད' : 'ད', 'མད' : 'ད', 'འད' : 'ད', 'འདྲ' : 'ད', 'རྡ' : 'ྡ', 'ལྡ' : 'ྡ', 'སྡ' : 'ྡ', 'བརྡ' : 'ྡ', 'བལྡ' : 'ྡ', 'བསྡ' : 'ྡ', 'ན' : 'ན', 'གན' : 'ན', 'མན' : 'ན', 'རྣ' : 'ྣ', 'སྣ' : 'ྣ', 'སྣྲ' : 'ྣ', 'བརྣ' : 'ྣ', 'བསྣ' : 'ྣ', 'པ' : 'པ', 'པྱ' : 'པ', 'པྲ' : 'པ', 'དཔ' : 'པ', 'དཔྱ' : 'པ', 'དཔྲ' : 'པ', 'ལྤ' : 'ྤ', 'སྤ' : 'ྤ', 'སྤྱ' : 'ྤ', 'སྤྲ' : 'ྤ', 'ཕ' : 'ཕ', 'ཕྱ' : 'ཕ', 'ཕྲ' : 'ཕ', 'འཕ' : 'ཕ', 'འཕྱ' : 'ཕ', 'འཕྲ' : 'ཕ', 'བ' : 'བ', 'བྱ' : 'བ', 'བྲ' : 'བ', 'བླ' : 'ླ', 'དབ' : 'བ', 'དབྱ' : 'བ', 'དབྲ' : 'བ', 'འབ' : 'བ', 'འབྱ' : 'བ', 'འབྲ' : 'བ', 'རྦ' : 'ྦ', 'ལྦ' : 'ྦ', 'སྦ' : 'ྦ', 'སྦྱ' : 'ྦ', 'སྦྲ' : 'ྦ', 'མ' : 'མ', 'མྱ' : 'མ', 'མྲ' : 'མ', 'དམ' : 'མ', 'དམྱ' : 'མ', 'དམྲ' : 'མ', 'རྨ' : 'ྨ', 'རྨྱ' : 'ྨ', 'སྨ' : 'ྨ', 'སྨྱ' : 'ྨ', 'སྨྲ' : 'ྨ', 'ཙ' : 'ཙ', 'གཙ' : 'ཙ', 'བཙ' : 'ཙ', 'རྩ' : 'ྩ', 'སྩ' : 'ྩ', 'བརྩ' : 'ྩ', 'བསྩ' : 'ྩ', 'ཚ' : 'ཚ', 'མཚ' : 'ཚ', 'འཚ' : 'ཚ', 'ཛ' : 'ཛ', 'མཛ' : 'ཛ', 'འཛ' : 'ཛ', 'རྫ' : 'ྫ', 'བརྫ' : 'ྫ', 'ཝ' : 'ཝ', 'ཞ' : 'ཞ', 'གཞ' : 'ཞ', 'བཞ' : 'ཞ', 'ཟ' : 'ཟ', 'ཟླ' : 'ླ', 'གཟ' : 'ཟ', 'བཟ' : 'ཟ', 'བཟླ' : 'ླ', 'འ' : 'འ', 'ཡ' : 'ཡ', 'གཡ' : 'ཡ', 'ར' : 'ར', 'རླ' : 'ླ', 'བརླ' : 'ླ', 'ལ' : 'ལ', 'ཤ' : 'ཤ', 'གཤ' : 'ཤ', 'བཤ' : 'ཤ', 'ས' : 'ས', 'སྲ' : 'ས', 'སླ' : 'ླ', 'གས' : 'ས', 'བས' : 'ས', 'བསྲ' : 'ས', 'བསླ' : 'ླ', 'ཧ' : 'ཧ', 'ཧྲ' : 'ཧ', 'ལྷ' : 'ྷ', 'ཨ' : 'ཨ', 'ཀའུ' : 'འ', 'ཀིའུ' : 'འ', 'ཀེའུ' : 'འ', 'ཀོའུ' : 'འ', 'ཀྲུའུ' : 'འ', 'ཁེའུ' : 'འ', 'ཁྱིའུ' : 'འ', 'ཁྱེའུ' : 'འ', 'ཁྲིའུ' : 'འ', 'ཁྲུའུ' : 'འ', 'ཁྲེའུ' : 'འ', 'གའུ' : 'འ', 'གྲིའུ' : 'འ', 'གྲེའུ' : 'འ', 'གླེའུ' : 'འ', 'འགིའུ' : 'འ', 'འགོའུ' : 'འ', 'རྒེའུ' : 'འ', 'སྒའུ' : 'འ', 'སྒེའུ' : 'འ', 'སྒྱེའུ' : 'འ', 'སྒྲེའུ' : 'འ', 'རྔེའུ' : 'འ', 'སྔེའུ' : 'འ', 'གཅིའུ' : 'འ', 'གཅེའུ' : 'འ', 'ལྕེའུ' : 'འ', 'རྗེའུ' : 'འ', 'ཉེའུ' : 'འ', 'སྙེའུ' : 'འ', 'ཏེའུ' : 'འ', 'གཏེའུ' : 'འ', 'རྟའུ' : 'འ', 'རྟེའུ' : 'འ', 'སྟེའུ' : 'འ', 'ཐིའུ' : 'འ', 'ཐུའུ' : 'འ', 'ཐེའུ' : 'འ', 'ཐོའུ' : 'འ', 'མཐེའུ' : 'འ', 'དུའུ' : 'འ', 'དེའུ' : 'འ', 'དྲེའུ' : 'འ', 'མདེའུ' : 'འ', 'རྡེའུ' : 'འ', 'སྡེའུ' : 'འ', 'ནའུ' : 'འ', 'ནེའུ' : 'འ', 'ནོའུ' : 'འ', 'སྣེའུ' : 'འ', 'དཔེའུ' : 'འ', 'སྤའུ' : 'འ', 'སྤེའུ' : 'འ', 'སྤྱིའུ' : 'འ', 'སྤྲེའུ' : 'འ', 'ཕེའུ' : 'འ', 'ཕྲའུ' : 'འ', 'ཕྲེའུ' : 'འ', 'འཕེའུ' : 'འ', 'བེའུ' : 'འ', 'བྱའུ' : 'འ', 'བྱིའུ' : 'འ', 'བྱེའུ' : 'འ', 'བྲའུ' : 'འ', 'བྲའོ' : 'འ', 'བྲེའུ' : 'འ', 'བྲོའུ' : 'འ', 'འབེའུ' : 'འ', 'སྦྲེའུ' : 'འ', 'མིའུ' : 'འ', 'མུའུ' : 'འ', 'མོའུ' : 'འ', 'མྱིའུ' : 'འ', 'རྨེའུ' : 'འ', 'སྨེའུ' : 'འ', 'ཙིའུ' : 'འ', 'ཙེའུ' : 'འ', 'གཙེའུ' : 'འ', 'རྩེའུ' : 'འ', 'ཚའུ' : 'འ', 'ཚུའུ' : 'འ', 'ཚེའུ' : 'འ', 'མཚེའུ' : 'འ', 'མཚེའུ' : 'འ', 'རྫིའུ' : 'འ', 'རྫེའུ' : 'འ', 'གཞུའུ' : 'འ', 'ཟེའུ' : 'འ', 'ཡེའུ' : 'འ', 'གཡིའུ' : 'འ', 'རེའུ' : 'འ', 'ལའུ' : 'འ', 'ལིའུ' : 'འ', 'ལེའུ' : 'འ', 'ལོའུ' : 'འ', 'ཤའུ' : 'འ', 'ཤེའུ' : 'འ', 'སིའུ' : 'འ', 'སེའུ' : 'འ', 'སྲིའུ' : 'འ', 'སླེའུ' : 'འ', 'བསེའུ' : 'འ', 'སླེའོ' : 'འ', 'ཧུའུ' : 'འ', 'ཧེའུ' : 'འ', 'ཧྲུའུ' : 'འ', 'སྟྭ': 'ྟ', 'གྭ': 'ག', 'ཞྭ': 'ཞ', 'ཁྭ': 'ཁ', 'དྲྭ': 'ད', 'ཀྭའི': 'ཀ', 'བསྭོ': 'ས', 'དྭ': 'ད', 'རྭ': 'ར', 'སྭ': 'ས', 'ཤྭ': 'ཤ', 'ཧྭ': 'ཧ', 'ལྭ': 'ལ', 'ཕྱྭ': 'ཕ', 'ཟྭ': 'ཟ', 'ཀྭ': 'ཀ', 'དྭོ': 'ད', 'ཉྭ': 'ཉ', 'ཚྭ': 'ཚ', 'རྩྭ': 'ྩ', 'བསྭ': 'ས', 'གྲྭ': 'ག', 'ཧྭག': 'ཧ', 'ཀྭས': 'ཀ', 'ཁྭངས': 'ཁ', 'ཧྭང': 'ཧ', 'ཀྭན': 'ཀ', 'དྭགས': 'ད', 'ཧྭགས': 'ཧ', 'དྭངས': 'ད', 'ཏྭོན': 'ཏ', 'ཧྤ' : 'ྤ', 'ཀརྨ' : 'ྨ', 'པདྨ' : 'ྨ'}
        self.exceptions = {'བགླ' : 'ླ', 'མདྲོན' : 'ད', 'བརྡའ' : 'ྡ', 'བརྟའ' : 'ྟ'}
        self.wazurs = {'ཧྭག': 'ཧ', 'ཀྭས': 'ཀ', 'ཁྭངས': 'ཁ', 'ཧྭང': 'ཧ', 'ཀྭན': 'ཀ', 'དྭགས': 'ད', 'ཧྭགས': 'ཧ', 'དྭངས': 'ད', 'ཏྭོན': 'ཏ'}
        self.mingzhis = {**self.roots, **self.exceptions, **self.wazurs}

    def get(self, components):
        self.components = components
        '''
        takes as input the output of get_components() and outputs the mingzhi that will serve for the particle agreement.
        for example, ཁྱེའུར will return འ
        returns None if more than one solution from get_components()
        '''
        if type(self.components) == 'list' or self.components == None:
            return None
        else:
            return self.mingzhis[self.components[0]]


# In[4]:

class AntTib:
    '''
    to and from pseudo-Wylie
    to_pw_text() requires the 
    '''
    
    def __init__(self):            
        self.punct_beginning = ["༄", "༅", "࿓", "࿔", "༇", "༆", "༈"]
        self.punct_separators = [" ", "།", "༎", "༏", "༐", "༑", "༔"]
        self.punct_other = ["༼", "༽", "༒", "༓"]
        self.syl_punct = ["་", "༌", "ཿ"]

        # 1rst part of the syllable
        self.roots = {'ཀ': 'k', 'ཀྱ': 'ky', 'ཀྲ': 'kr', 'ཀླ': 'kl', 'ཁ': 'kh', 'ཁྱ': 'khy', 'ཁྲ': 'khr', 'ག': 'g', 'གཅ': 'gc', 'གཉ': 'gny', 'གཏ': 'gt', 'གཏྲ': 'gtr', 'གད': 'gd', 'གན': 'gn', 'གཙ': 'gts', 'གཞ': 'gzh', 'གཟ': 'gz', 'གཡ': 'gqy', 'གཤ': 'gsh', 'གས': 'gs', 'གྱ': 'gy', 'གྲ': 'gr', 'གླ': 'gl', 'ང': 'ng', 'ཅ': 'c', 'ཆ': 'ch', 'ཇ': 'j', 'ཉ': 'ny', 'ཏ': 't', 'ཏྲ': 'tr', 'ཐ': 'th', 'ཐྲ': 'thr', 'ད': 'd', 'དཀ': 'dk', 'དཀྱ': 'dky', 'དཀྲ': 'dkr', 'དཀླ': 'dkl', 'དག': 'dg', 'དགྱ': 'dgy', 'དགྲ': 'dgr', 'དང': 'dng', 'དཔ': 'dp', 'དཔྱ': 'dpy', 'དཔྲ': 'dpr', 'དབ': 'db', 'དབྱ': 'dby', 'དབྲ': 'dbr', 'དམ': 'dm', 'དམྱ': 'dmy', 'དམྲ': 'dmr', 'དྲ': 'dr', 'ན': 'n', 'པ': 'p', 'པྱ': 'py', 'པྲ': 'pr', 'ཕ': 'ph', 'ཕྱ': 'phy', 'ཕྲ': 'phr', 'བ': 'b', 'བཀ': 'bk', 'བཀྱ': 'bky', 'བཀྲ': 'bkr', 'བཀླ': 'bkl', 'བག': 'bg', 'བགྱ': 'bgy', 'བགྲ': 'bgr', 'བཅ': 'bc', 'བཏ': 'bt', 'བཏྲ': 'btr', 'བད': 'bd', 'བཙ': 'bts', 'བཞ': 'bzh', 'བཟ': 'bz', 'བཟླ': 'bzl', 'བརྐ': 'brk', 'བརྐྱ': 'brky', 'བརྒ': 'brg', 'བརྒྱ': 'brgy', 'བརྔ': 'brng', 'བརྗ': 'brj', 'བརྙ': 'brny', 'བརྟ': 'brt', 'བརྡ': 'brd', 'བརྣ': 'brn', 'བརྩ': 'brts', 'བརྫ': 'brdz', 'བརླ': 'brl', 'བལྟ': 'blt', 'བལྡ': 'bld', 'བཤ': 'bsh', 'བས': 'bs', 'བསྐ': 'bsk', 'བསྐྱ': 'bsky', 'བསྐྲ': 'bskr', 'བསྒ': 'bsg', 'བསྒྱ': 'bsgy', 'བསྒྲ': 'bsgr', 'བསྔ': 'bsng', 'བསྙ': 'bsny', 'བསྟ': 'bst', 'བསྡ': 'bsd', 'བསྣ': 'bsn', 'བསྩ': 'bsts', 'བསྲ': 'bsr', 'བསླ': 'bsl', 'བྱ': 'by', 'བྲ': 'br', 'བླ': 'bl', 'མ': 'm', 'མཁ': 'mkh', 'མཁྱ': 'mkhy', 'མཁྲ': 'mkhr', 'མག': 'mg', 'མགྱ': 'mgy', 'མགྲ': 'mgr', 'མང': 'mng', 'མཆ': 'mch', 'མཇ': 'mj', 'མཉ': 'mny', 'མཐ': 'mth', 'མད': 'mad', 'མན': 'mn', 'མཚ': 'mtsh', 'མཛ': 'mdz', 'མྱ': 'my', 'མྲ': 'mr', 'ཙ': 'ts', 'ཚ': 'tsh', 'ཛ': 'dz', 'ཝ': 'w', 'ཞ': 'zh', 'ཟ': 'z', 'ཟླ': 'zl', 'འ': 'v', 'འཁ': 'vkh', 'འཁྱ': 'vkhy', 'འཁྲ': 'vkhr', 'འག': 'vg', 'འགྱ': 'vgy', 'འགྲ': 'vgr', 'འཆ': 'vch', 'འཇ': 'vj', 'འཐ': 'vth', 'འད': 'vd', 'འདྲ': 'vdr', 'འཕ': 'vph', 'འཕྱ': 'vphy', 'འཕྲ': 'vphr', 'འབ': 'vb', 'འབྱ': 'vby', 'འབྲ': 'vbr', 'འཚ': 'vtsh', 'འཛ': 'vdz', 'ཡ': 'y', 'ར': 'r', 'རྐ': 'rk', 'རྐྱ': 'rky', 'རྒ': 'rg', 'རྒྱ': 'rgy', 'རྔ': 'rng', 'རྗ': 'rj', 'རྙ': 'rny', 'རྟ': 'rt', 'རྡ': 'rd', 'རྣ': 'rn', 'རྦ': 'rb', 'རྨ': 'rm', 'རྨྱ': 'rmy', 'རྩ': 'rts', 'རྫ': 'rdz', 'རླ': 'rl', 'ལ': 'l', 'ལྐ': 'lk', 'ལྒ': 'lg', 'ལྔ': 'lng', 'ལྕ': 'lc', 'ལྗ': 'lj', 'ལྟ': 'lt', 'ལྡ': 'ld', 'ལྤ': 'lp', 'ལྦ': 'lb', 'ལྷ': 'lh', 'ཤ': 'sh', 'ས': 's', 'སྐ': 'sk', 'སྐྱ': 'sky', 'སྐྲ': 'skr', 'སྒ': 'sg', 'སྒྱ': 'sgy', 'སྒྲ': 'sgr', 'སྔ': 'sng', 'སྙ': 'sny', 'སྟ': 'st', 'སྡ': 'sd', 'སྣ': 'sn', 'སྣྲ': 'snr', 'སྤ': 'sp', 'སྤྱ': 'spy', 'སྤྲ': 'spr', 'སྦ': 'sb', 'སྦྱ': 'sby', 'སྦྲ': 'sbr', 'སྨ': 'sm', 'སྨྱ': 'smy', 'སྨྲ': 'smr', 'སྩ': 'sts', 'སྲ': 'sr', 'སླ': 'sl', 'ཧ': 'h', 'ཧྲ': 'hr', 'ཨ': 'A'}
        self.rareC = {'བེའུ': 'bevu', 'ཧུའུ': 'huvu', 'ཀིའུ': 'kivu', 'བྲའོ': 'bravo', 'སླེའུ': 'slevu', 'འགོའུ': 'govu', 'ཁྱེའུ': 'khyevu', 'མདེའུ': 'mdevu', 'རྔེའུ': 'rngevu', 'ཚུའུ': 'tshuvu', 'གཅེའུ': 'gcevu', 'རྟའུ': 'rtavu', 'ཁྱིའུ': 'khyivu', 'ཐེའུ': 'thevu', 'སྟེའུ': 'stevu', 'རྩེའུ': 'rtsevu', 'སླེའོ': 'slevo', 'ཤའུ': 'shavu', 'ཉེའུ': 'nyevu', 'སྨེའུ': 'smevu', 'རྟེའུ': 'rtevu', 'ཚའུ': 'tshavu', 'ཙེའུ': 'tsevu', 'གཡིའུ': 'g.yivu', 'སྤྲེའུ': 'sprevu', 'ལོའུ': 'lovu', 'གྲིའུ': 'grivu', 'སྤྱིའུ': 'spyivu', 'འབེའུ': 'bevu', 'གླེའུ': 'glevu', 'ལའུ': 'lavu', 'སྙེའུ': 'snyevu', 'ཕེའུ': 'phevu', 'རྡེའུ': 'rdevu', 'ཀྲུའུ': 'kruvu', 'ཁྲིའུ': 'khrivu', 'བྲེའུ': 'brevu', 'རྨེའུ': 'rmevu', 'གཏེའུ': 'gtevu', 'སྣེའུ': 'snevu', 'ཕྲའུ': 'phravu', 'དྲེའུ': 'drevu', 'སྡེའུ': 'sdevu', 'ནོའུ': 'novu', 'ཟེའུ': 'zevu', 'མིའུ': 'mivu', 'ཁེའུ': 'khevu', 'རྫེའུ': 'rdzevu', 'གཙེའུ': 'gtsevu', 'མཐེའུ': 'mthevu', 'མོའུ': 'movu', 'ཀེའུ': 'kevu', 'སྤའུ': 'spavu', 'དེའུ': 'devu', 'ཧེའུ': 'hevu', 'ཕྲེའུ': 'phrevu', 'ཚེའུ': 'tshevu', 'རྒེའུ': 'rgevu', 'བྲོའུ': 'brovu', 'བྱའུ': 'byavu', 'ཏེའུ': 'tevu', 'ཀོའུ': 'kovu', 'རེའུ': 'revu', 'ལིའུ': 'livu', 'ཡེའུ': 'yevu', 'མུའུ': 'muvu', 'སྒྲེའུ': 'sgrevu', 'ཁྲུའུ': 'khruvu', 'ལེའུ': 'levu', 'བྱེའུ': 'byevu', 'བྱིའུ': 'byivu', 'བྲའུ': 'bravu', 'འཕེའུ': 'phevu', 'གཅིའུ': 'gcivu', 'མཚེའུ': 'mtshevu', 'སྦྲེའུ': 'sbrevu', 'འགིའུ': 'givu', 'སྔེའུ': 'sngevu', 'ནེའུ': 'nevu', 'རྫིའུ': 'rdzivu', 'རྗེའུ': 'rjevu', 'སེའུ': 'sevu', 'ཐིའུ': 'thivu', 'སྒའུ': 'sgavu', 'སིའུ': 'sivu', 'མྱིའུ': 'myivu', 'ཙིའུ': 'tsivu', 'སྲིའུ': 'srivu', 'ནའུ': 'navu', 'བསེའུ': 'bsevu', 'གའུ': 'gavu', 'སྒེའུ': 'sgevu', 'ཀའུ': 'kavu', 'གྲེའུ': 'grevu', 'ཁྲེའུ': 'khrevu', 'སྤེའུ': 'spevu', 'སྒྱེའུ': 'sgyevu', 'དཔེའུ': 'dpevu', 'ཧྲུའུ': 'hruvu', 'ཐོའུ': 'thovu', 'ཤེའུ': 'shevu', 'ཐུའུ': 'thuvu', 'གཞུའུ': 'gzhuvu', 'དུའུ': 'duvu', 'ལྕེའུ': 'lcevu'}
        self.wazurC = {'སྟྭ': 'stw', 'གྭ': 'gw', 'ཞྭ': 'zhw', 'ཁྭ': 'khw', 'དྲྭ': 'drw', 'ཀྭའི': 'kwavi', 'བསྭོ': 'bswo', 'དྭ': 'dw', 'རྭ': 'rw', 'སྭ': 'sw', 'ཤྭ': 'shw', 'ཧྭ': 'hw', 'ལྭ': 'lw', 'ཕྱྭ': 'phyw', 'ཟྭ': 'zw', 'ཀྭ': 'kw', 'དྭོ': 'dwo', 'ཉྭ': 'nyw', 'ཚྭ': 'tshw', 'རྩྭ': 'rtsw', 'བསྭ': 'bsw', 'གྲྭ': 'grw'}
        self.A = {**self.roots, **self.rareC, **self.wazurC}
        # second part of the syllable
        self.B = {'ག': 'ag', 'གས': 'ags', 'ང': 'ang', 'ངས': 'angs', 'ད': 'ad', 'ན': 'an', 'བ': 'ab', 'བས': 'abs', 'མ': 'am', 'མས': 'ams', 'འ': 'av', 'འང': 'avang', 'འམ': 'avam', 'འི': 'avi', 'འོ': 'avo', 'ར': 'ar', 'ལ': 'al', 'ས': 'as', 'ི': 'i', 'ིག': 'ig', 'ིགས': 'igs', 'ིང': 'ing', 'ིངས': 'ings', 'ིད': 'id', 'ིན': 'in', 'ིབ': 'ib', 'ིབས': 'ibs', 'ིམ': 'im', 'ིམས': 'ims', 'ིའང': 'ivang', 'ིའམ': 'ivam', 'ིའི': 'ivi', 'ིའོ': 'ivo', 'ིར': 'ir', 'ིལ': 'il', 'ིས': 'is', 'ུ': 'u', 'ུག': 'ug', 'ུགས': 'ugs', 'ུང': 'ung', 'ུངས': 'ungs', 'ུད': 'ud', 'ུན': 'un', 'ུབ': 'ub', 'ུབས': 'ubs', 'ུམ': 'um', 'ུམས': 'ums', 'ུའང': 'uvang', 'ུའམ': 'uvam', 'ུའི': 'uvi', 'ུའོ': 'uvo', 'ུར': 'ur', 'ུལ': 'ul', 'ུས': 'us', 'ེ': 'e', 'ེག': 'eg', 'ེགས': 'egs', 'ེང': 'eng', 'ེངས': 'engs', 'ེད': 'ed', 'ེན': 'en', 'ེབ': 'eb', 'ེབས': 'ebs', 'ེམ': 'em', 'ེམས': 'ems', 'ེའང': 'evang', 'ེའམ': 'evam', 'ེའི': 'evi', 'ེའོ': 'evo', 'ེར': 'er', 'ེལ': 'el', 'ེས': 'es', 'ོ': 'o', 'ོག': 'og', 'ོགས': 'ogs', 'ོང': 'ong', 'ོངས': 'ongs', 'ོད': 'od', 'ོན': 'on', 'ོབ': 'ob', 'ོབས': 'obs', 'ོམ': 'om', 'ོམས': 'oms', 'ོའང': 'ovang', 'ོའམ': 'ovam', 'ོའི': 'ovi', 'ོའོ': 'ovo', 'ོར': 'or', 'ོལ': 'ol', 'ོས': 'os'}
        # exceptions
        self.special = {'བགླ' : 'bgla', 'མདྲོན' : 'mdron', 'བརྡའ' : 'brdav', 'བརྟའ' : 'brtav'}
        self.wazur = {'ཧྭག': 'hwag', 'ཀྭས': 'kwas', 'ཁྭངས': 'khwangs', 'ཧྭང': 'hwang', 'ཀྭན': 'kwan', 'དྭགས': 'dwags', 'ཧྭགས': 'hwags', 'དྭངས': 'dwangs', 'ཏྭོན': 'twon'}
        self.exceptions = {**self.special, **self.wazur}
        # inversed lists
        self.C = {v: k for k, v in self.A.items()}
        self.D = {v: k for k, v in self.B.items()}
        self.E = {v: k for k, v in self.exceptions.items()}

    def to_pw_syl(self, components):
        if type(components) == 'list' or components == None:
            return '***'        
        else:
            part1 = components[0]
            part2 = components[1]
            #print(part1, part2)
            if part1 not in self.A and part1 not in self.exceptions:
                return '***'
            else:
                # first part of the syllable
                if part1 in self.exceptions:
                    a = self.exceptions[part1]
                else:
                    a = self.A[part1]
                # second part of the syllable
                b = ''
                if part2 == '':
                    b = 'a'
                elif part2 != 'x':
                    b = self.B[part2]
                return a+b

    def from_pw_syl(self, syl):
        #print(syl)
        if syl == '***':
            return '***'
        else:
            a = ''
            if syl in self.E:
                return self.E[syl]
            elif syl in self.C:
                return self.C[syl]
            else:
                i = len(syl)-1
                while i >= 0:
                    if syl[:i] in self.C:
                        a = syl[:i]
                        break
                    i = i-1
            b = syl[len(a):]
            if b.startswith('v') or b.startswith('r') or b.startswith('l') or b.startswith('s'):
                b = 'a'+b
            if b == 'a':
                return self.C[a]
            else:
                return self.C[a]+self.D[b]

    def __is_punct(self, string):
        if '།' in string or '༎' in string or '༏' in string or '༐' in string or '༑' in string or '༔' in string or ';' in string or ':' in string:
            return True
        else:
            return False
    
    def __trim_punct(self, List):  
        # a hack to keep only one time the punctuation. 
        # being forced to put the (xxx)+ into brackets, re.split() creates two list elements for one punctuation block
        i = 0
        while i < len(List)-1:
            if self.__is_punct(List[i]) and self.__is_punct(List[i+1]):
                del List[i+1]
            i = i+1
    
    def to_pw_text(self, string):
        ### Prepare the string : delete all extra punctuations
        # replace the tabs by normal spaces
        string = string.replace('	', ' ')
        # replace all non-breaking tsek by a normal tsek
        string = string.replace('༌', '་')
        # delete all yigos
        string = re.sub('(༄༅+|༆|༇|༈)།?༎? ?།?༎?', '', string)
        # split on the punctuation. here, a paragraph is just a chunk of text separated by shads.
        
        ### split on remaining punctuation
        paragraphs = re.split(r'(( *། *| *༎ *| *༏ *| *༐ *| *༑ *| *༔ *)+)', string)
        # trim the extra punctuation 
        self.__trim_punct(paragraphs)
        #delete the last element of the list if it is an empty string
        if paragraphs[len(paragraphs)-1] == '':
            del paragraphs[len(paragraphs)-1]
        
        ### replace all shads by a ';' and the tershe by a ':'
        for num, element in enumerate(paragraphs):
            if '།' in element or '༏' in element or '༐' in element or '༑' in element:
                paragraphs[num] = element.replace('།', ';').replace('༎', ';').replace('༏', ';').replace('༐', ';').replace('༑', ';')
            elif '༎' in element:
                paragraphs[num] = element.replace('༎', ';;')
            elif '༔' in element:
                paragraphs[num] = element.replace('༔', ':')

        ### translate the syllables into pseudo-wylie
        parts = SylComponents() # instantiate object
        pw_text = []
        for par in paragraphs:
            if ';' not in par and ':' not in par:
                par = re.sub(r'་$', '', par.replace('་ ', ' ')) # delete all tsek at the end of words
                pw_par = []
                words = par.split(' ')
                for word in words:
                    syls = word.split('་')
                    pw_word = []
                    for syl in syls:
                        #print(syl)
                        pw_word.append(self.to_pw_syl(parts.get(syl)))
                    pw_par.append('x'.join(pw_word))
                pw_text.append(' '.join(pw_par))
            else:
                pw_text.append(par)
        return ''.join(pw_text)

    def from_pw_text(self, string):
        text = ''
        syl = ''
        for char in string:
            if char == ' ':
                if syl != '':
                    text += self.from_pw_syl(syl)+'་'
                syl = ''
                text += char
            elif char == ';':
                if syl != '':
                    text += self.from_pw_syl(syl)
                    if syl.endswith('ng'):
                        text += '་'
                syl = ''
                text += '།'
            elif char == ':':
                if syl != '':
                    text += self.from_pw_syl(syl)
                    if syl.endswith('ng'):
                        text += '་'
                syl = ''
                text += '༔'
            elif char == 'x':
                if syl != '':
                    text += self.from_pw_syl(syl)+'་'
                syl = ''
            else:
                syl += char

    def from_pw_text(self, string):
        paragraphs = re.split(r'(( *; *| *: *)+)', string)
        #delete the last element of the list if it is an empty string
        if paragraphs[len(paragraphs)-1] == '':
            del paragraphs[len(paragraphs)-1]
        # trim the extra punctuation 
        self.__trim_punct(paragraphs)
        pw_text = []
        for par in paragraphs:
            if ';' not in par and ':' not in par:
                pw_par = []
                words = par.split(' ')
                for word in words:
                    syls = word.split('x')
                    pw_word = []
                    for syl in syls:
                        pw_word.append(self.from_pw_syl(syl))
                    pw_par.append('་'.join(pw_word)+'་')
                pw_text.append(' '.join(pw_par))
            else:
                pw_text.append(par.replace(';', '།').replace(':', '༔'))
        pw_text = ''.join(pw_text)
        pw_text = re.sub(r'([^ང])་([༔།])', r'\1\2', pw_text)
        return pw_text
    
    def no_space(self, string):
        return string.replace('་ ', '༌')
# In[6]:

import time
pw = AntTib()
with open('../../../TibTAL/resources/wylie/ཤེར་ཕྱིན།ཕ།-_clean.txt', 'r', -1, 'utf-8-sig') as f:
    content = f.read()
o = time.time()
ps = pw.to_pw_text(content)
t = time.time()
print(t - o)


# In[ ]:

a = time.time()
un = pw.from_pw_text(ps)
b = time.time()
print(b - a)


# In[ ]:

text = '༄༅།	།འཕགས་པ་ ཤེས་རབ་ ཀྱི་ ཕ་རོལ་ ཏུ་ ཕྱིན་པ་ འབུམ་པ་ དང༌༔  ཉི་ཁྲི་ ལྔ་ སྟོང་པ་ དང།  ཁྲི་ བརྒྱད་སྟོང་པའི་ རྒྱ་ ཆེར་ བཤད་པ༎ ༄༅༅། །འཕགས་པ་ ཤེས་རབ་ ཀྱི་ ཕ་རོལ་ ཏུ་ ཕྱིན་པ་ འབུམ་པ་ དང༌། །ཉི་ཁྲི་ ལྔ་ སྟོང་པ་ དང༌ ། ཁྲི་ བརྒྱད་སྟོང་པའི་ རྒྱ་ ཆེར་ བཤད་པ།'

pw = AntTib()
no = pw.no_space(text)
pseudo = pw.to_pw_text(text)
uni = pw.from_pw_text(pseudo)
nospace = pw.no_space(uni)

print('original text :\n',text)
print('no space original text :\n', no)
print('pseudo-wylie :\n', pseudo)
print('back to uni :\n', uni)
print('no space uni :\n', nospace)


# In[ ]:

pseudo


# In[ ]:

text = ''
word = ''
for char in pseudo:
    if char == ' ':
        if word != '':
            text += word+'་'
        word = ''
        text += char
    elif char == ';':
        if word != '':
            text += word
            if word.endswith('ng'):
                text += '་'
        word = ''
        text += '།'
    elif char == ':':
        if word != '':
            text += word
            if word.endswith('ng'):
                text += '་'
        word = ''
        text += '༔'
    elif char == 'x':
        if word != '':
            text += word+'་'
        word = ''
    else:
        word += char
print(text)


# In[ ]:



