import re
from .common import strip_list

class AntPut:
    def __init__(self, AT):
        self.AT = AT
        self.bad_line = '*** '*5+'BAD LINE '+'*** '*5+'\n'
        self.sep = '\t'
        self.nums = r'[.0-9]+\t'
        self.chars = r'[ a-zA-Z]+'

    def process(self, lines, comments, num, l_regex):
        """
        Serves as the common part of all lists to be proceeded
        :param lines: list to be processed
        :param comments: the number of first lines starting with #
        :param num: number of columns filled with numbers
        :param l_regex: ensures the line is correctly formed and can be processed
        :return: returns the string with the AntTib converted to Unicode
        """
        out = ''
        # put the three first lines in out and delete them from lines[]
        for line in lines[0:comments]:
            out +=line+'\n'
        del lines[0:comments]

        # process the whole file
        for line in lines:
            if re.match(l_regex, line):
                l_out = ''
                parts = line.split('\t')
                for i in range(num):
                    l_out += parts[i]+self.sep
                tib = self.AT.from_ant_text(parts[num]).replace('***་', '་')
                if len(parts[num]) == 1:
                    tib = '-'+tib  # add a - to show it is a merged particle
                l_out += tib+self.sep
                out += l_out+'\n'
            else:
                out += self.bad_line
        return out

    def keyword_list(self, string):
        lines = string.split('\n')
        strip_list(lines)

        comments = 3  # number of commented lines at the beginning
        num = 3  # number of columns with numbers
        l_regex = self.nums * num + self.chars
        if re.match(r'#Types Before Cut: [.0-9]+', lines[0]) and re.match(r'#Types After Cut: [.0-9]+', lines[1]) and re.match(r'#Search Hits: [.0-9]+', lines[2]) and re.match(l_regex, lines[3]):
            process = self.process(lines, comments, num, l_regex)
            if not process:
                return None
            else:
                return process
        else:
            return None

    def cluster(self, string):
        lines = string.split('\n')
        strip_list(lines)

        comments = 2  # number of commented lines at the beginning
        num = 3  # number of columns with numbers
        l_regex = self.nums * num + self.chars
        if re.match(r'#Total No. of Cluster Types: [0-9]+', lines[0]) and re.match(r'#Total No. of Cluster Tokens: [0-9]+', lines[1]) and re.match(l_regex, lines[2]):
            process = self.process(lines, comments, num, l_regex)
            if not process:
                return None
            else:
                return process
        else:
            return None

    def collocates(self, string):
        lines = string.split('\n')
        strip_list(lines)

        comments = 2  # number of commented lines at the beginning
        num = 5  # number of columns with numbers
        l_regex = self.nums * num + self.chars
        if re.match(r'#Total No. of Collocate Types: [0-9]+', lines[0]) and re.match(r'#Total No. of Collocate Tokens: [0-9]+', lines[1]) and re.match(l_regex, lines[2]):
            process = self.process(lines, comments, num, l_regex)
            if not process:
                return None
            else:
                return process
        else:
            return None

    def ngram(self, string):
        lines = string.split('\n')
        strip_list(lines)

        comments = 2  # number of commented lines at the beginning
        num = 3  # number of columns with numbers
        l_regex = self.nums * num + self.chars
        if re.match(r'#Total No. of N-Gram Types: [0-9]+', lines[0]) and re.match(r'#Total No. of N-Gram Tokens: [0-9]+', lines[1]) and re.match(l_regex, lines[2]):
            process = self.process(lines, comments, num, l_regex)
            if not process:
                return None
            else:
                return process
        else:
            return None

    def word_list(self, string):
        lines = string.split('\n')
        strip_list(lines)

        comments = 3  # number of commented lines at the beginning
        num = 2  # number of columns with numbers
        l_regex = self.nums * num + self.chars
        if re.match(r'#Word Types: [0-9]+', lines[0]) and  re.match(r'#Word Tokens: [0-9]+', lines[1]) and re.match(r'#Search Hits: [0-9]+', lines[2]) and re.match(l_regex, lines[3]):
            process = self.process(lines, comments, num, l_regex)
            if not process:
                return None
            else:
                return process
        else:
            return None

    def concordance(self, string):
        lines = string.split('\n')
        strip_list(lines)

        l_regex = self.nums+r'[ ;:*a-zA-Z]+\t'*2+r'[^\.]+\.txt'+r'\t[.0-9]+'*2
        if re.match(l_regex, lines[0]):
            out = ''
            for line in lines:
                if re.match(l_regex, line):
                    l_out = ''
                    parts = line.split('\t')
                    l_out += parts[0] + self.sep
                    for i in range(2):
                        l_out += self.AT.from_ant_text(parts[i+1].strip()) + self.sep
                    for i in range(3):
                        l_out += parts[i+3] + self.sep
                    out += l_out + '\n'
                else:
                    out += self.bad_line
            return out
        else:
            return None

    def profiler_tags(self, string):
        words = string.split(' ')

        converted = []
        for word in words:
            if '_' in word:
                parts = re.split(r'(_.)', word)
                converted.append(self.AT.from_ant_text(parts[0])+parts[1])
            else:
                converted.append(self.AT.from_ant_text(word))
        return ' '.join(converted)

    def profiler_stats(self, string):
        lines = string.split('\n')
        strip_list(lines)

        comments = 33  # number of commented lines at the beginning
        num = 2  # number of columns with numbers
        l_regex = self.chars+'\t'+self.nums+r'[0-9]+'
        if re.match(r'Group	Range	Freq	uf_1', lines[32]) and re.match(l_regex, lines[33]):
                out = ''
                out += '\n'.join(lines[:33])
                del lines[:33]

                for line in lines:
                    if re.match(l_regex, line):
                        parts = line.split('\t')
                        l_out = self.AT.from_ant_text(parts[0]) + self.sep
                        l_out += self.sep.join(parts[1:])
                        out += l_out + '\n'
                    else:
                        out += self.bad_line
                return out
        else:
            return None

    def words(self, string):
        lines = string.split('\n')
        strip_list(lines)
        words = []
        for word in lines:
            w = self.AT.from_ant_text(word)
            if len(word) <= 1:
                w = '-'+w
            words.append(w)
        return '\n'.join(words)