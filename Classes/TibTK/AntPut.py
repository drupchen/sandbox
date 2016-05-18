import re


class AntPut:
    def __init__(self, AT):
        self.AT = AT

    def keyword_list(self, string):
        out = ''
        lines = string.split('\n')
        # put the three first lines in out and delete them from lines[]
        for line in lines[:3]:
            out +=line+'\n'
        del lines[:3]

        for line in lines:
            if line != '':
                l_out = ''
                parts = line.split('\t')
                l_out += parts[0]+'\t'+parts[1]+'\t'
                tib = self.AT.from_ant_text(parts[2])
                if tib.endswith('***་'):
                    tib = tib.replace('***་', '')
                l_out += tib
                out += l_out+'\n'
        return out

