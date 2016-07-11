import sys
import os
import re
import ngram
import time
import tempfile
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from PyTib import Segment
from PyTib.common import write_file, open_file
from PyTib.NGrams import text2ngram




raw_string = open_file('files/བསྟོདཚོགས.txt').replace('\n', '')
syls = Segment().segment(raw_string.replace('༌', '་'), ant_segment=1, unknown=0, space_at_punct=True)
ngrams = text2ngram(string=syls)
