import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PyTib.NGrams import NGrams
from PyTib.common import pre_process, DefaultOrderedDict, write_file

import re
def no_space(string):
    for regex in [r'([་|༌])\s', r'(ང[་|༌])\s', r'\s(ར)', r'\s(ས)', r'\s(འི)', r'\s(འོ)']:
        string = re.sub(regex, r'\1', string)
    return string

test = 'བྱང་ཆུབ་ ལམ་ གྱི་ རིམ་པ འི་ འཁྲིད་ གསེར་ གྱི་ ཡང་ ཞུན་ ཞེས་བྱ་བ་ བཞུགས་ སོ། ། རྗེ་བཙུན་བླ་མ་ སྐྱབས་གསུམ་ ཀུན་ འདུས་ ཀྱི་ བདག་ཉིད་ཆེན་པོ་ གང་དེ འི་ ཞབས་ ལ་ གུས་པ་ ཆེན་པོ ས་ ཕྱག་ འཚལ་ ཞིང་ སྐྱབས་ སུ་ མཆི འོ། །བྱིན་ གྱིས་ བརླབ་ ཏུ་ གསོལ། དེ་ ལ་ འདི ར་ དལ་འབྱོར་ གྱི་ རྟེན་ ལ་ སྙིང་ བོ་ ལེན་ བར་ འདོད་པ འི་ སྐྱེས་བུ་ རྣམས་ ཀྱིས་ ཉམས་ སུ་ བླང་བ ར་ བྱ་བ་ ནི། བྱང་ཆུབ་ རྒྱལ་བའི་གསུང་རབ་ ཐམས་ཅད་ ཀྱི་ སྙིང་ བོ། །དུས་གསུམ་ འཕགས་པ་ ཐམས་ཅད་ ཀྱི་ བགྲོད་པ་གཅིག་ པ འི་ ལམ། ཤིང་རྟ་ཆེན་པོ་ ཀླུ་སྒྲུབ་ དང་ ཐོགས་མེད་ གཉིས་ ཀྱི་ ལམ་སྲོལ། རྣམ་པ་ཐམས་ཅད་ མཁྱེན་པ འི་ སར་འགྲོ་ བ འི་ སྐྱེ་བོ་ མཆོག་ གི་ ཆོས་ལུགས། བྱང་ཆུབ་ སྐྱེས་བུ་གསུམ་ གྱིས་ ཉམས་ སུ་ བླང་ བྱ འི་ རིམ་པ་ ཐམས་ཅད་ བྱང་ཆུབ་ མ་ཚང་ བ་ མེད་པ་ བསྡུས་པ། '
ng = NGrams().filtered_levels(test, 2, 3, unit='syls', freq=2)
write_file('filtered.txt', ng)
