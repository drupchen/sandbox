import re

mark = '*'  # marker of unknown syllables. Can’t be a letter. Only 1 char allowed. Can’t be left empty.

class AntTib:
    """
    Pseudo-Wylie created for use in AntConc.
    The output only contains letters for the syllables, :; for the punctuation.
    All yigos are deleted
    """

    def __init__(self):
        self.punct_beginning = ["༄", "༅", "࿓", "࿔", "༇", "༆", "༈"]
        self.punct_separators = [" ", "།", "༎", "༏", "༐", "༑", "༔"]
        self.punct_other = ["༼", "༽", "༒", "༓"]
        self.syl_punct = ["་", "༌", "ཿ"]
        self.punct_all = self.punct_beginning + self.punct_separators + self.punct_other + self.syl_punct

        # 1rst part of the syllable
        self.roots = {'ཀ': 'k', 'ཀྱ': 'ky', 'ཀྲ': 'kr', 'ཀླ': 'kl', 'ཁ': 'kh', 'ཁྱ': 'khy', 'ཁྲ': 'khr', 'ག': 'g',
                      'གཅ': 'gc', 'གཉ': 'gny', 'གཏ': 'gt', 'གཏྲ': 'gtr', 'གད': 'gd', 'གན': 'gn', 'གཙ': 'gts',
                      'གཞ': 'gzh', 'གཟ': 'gz', 'གཡ': 'gqy', 'གཤ': 'gsh', 'གས': 'gs', 'གྱ': 'gy', 'གྲ': 'gr', 'གླ': 'gl',
                      'ང': 'ng', 'ཅ': 'c', 'ཆ': 'ch', 'ཇ': 'j', 'ཉ': 'ny', 'ཏ': 't', 'ཏྲ': 'tr', 'ཐ': 'th', 'ཐྲ': 'thr',
                      'ད': 'd', 'དཀ': 'dk', 'དཀྱ': 'dky', 'དཀྲ': 'dkr', 'དཀླ': 'dkl', 'དག': 'dg', 'དགྱ': 'dgy',
                      'དགྲ': 'dgr', 'དང': 'dng', 'དཔ': 'dp', 'དཔྱ': 'dpy', 'དཔྲ': 'dpr', 'དབ': 'db', 'དབྱ': 'dby',
                      'དབྲ': 'dbr', 'དམ': 'dm', 'དམྱ': 'dmy', 'དམྲ': 'dmr', 'དྲ': 'dr', 'ན': 'n', 'པ': 'p', 'པྱ': 'py',
                      'པྲ': 'pr', 'ཕ': 'ph', 'ཕྱ': 'phy', 'ཕྲ': 'phr', 'བ': 'b', 'བཀ': 'bk', 'བཀྱ': 'bky', 'བཀྲ': 'bkr',
                      'བཀླ': 'bkl', 'བག': 'bg', 'བགྱ': 'bgy', 'བགྲ': 'bgr', 'བཅ': 'bc', 'བཏ': 'bt', 'བཏྲ': 'btr',
                      'བད': 'bd', 'བཙ': 'bts', 'བཞ': 'bzh', 'བཟ': 'bz', 'བཟླ': 'bzl', 'བརྐ': 'brk', 'བརྐྱ': 'brky',
                      'བརྒ': 'brg', 'བརྒྱ': 'brgy', 'བརྔ': 'brng', 'བརྗ': 'brj', 'བརྙ': 'brny', 'བརྟ': 'brt',
                      'བརྡ': 'brd', 'བརྣ': 'brn', 'བརྩ': 'brts', 'བརྫ': 'brdz', 'བརླ': 'brl', 'བལྟ': 'blt',
                      'བལྡ': 'bld', 'བཤ': 'bsh', 'བས': 'bs', 'བསྐ': 'bsk', 'བསྐྱ': 'bsky', 'བསྐྲ': 'bskr', 'བསྒ': 'bsg',
                      'བསྒྱ': 'bsgy', 'བསྒྲ': 'bsgr', 'བསྔ': 'bsng', 'བསྙ': 'bsny', 'བསྟ': 'bst', 'བསྡ': 'bsd',
                      'བསྣ': 'bsn', 'བསྩ': 'bsts', 'བསྲ': 'bsr', 'བསླ': 'bsl', 'བྱ': 'by', 'བྲ': 'br', 'བླ': 'bl',
                      'མ': 'm', 'མཁ': 'mkh', 'མཁྱ': 'mkhy', 'མཁྲ': 'mkhr', 'མག': 'mg', 'མགྱ': 'mgy', 'མགྲ': 'mgr',
                      'མང': 'mng', 'མཆ': 'mch', 'མཇ': 'mj', 'མཉ': 'mny', 'མཐ': 'mth', 'མད': 'md', 'མན': 'mn',
                      'མཚ': 'mtsh', 'མཛ': 'mdz', 'མྱ': 'my', 'མྲ': 'mr', 'ཙ': 'ts', 'ཚ': 'tsh', 'ཛ': 'dz', 'ཝ': 'w',
                      'ཞ': 'zh', 'ཟ': 'z', 'ཟླ': 'zl', 'འ': 'v', 'འཁ': 'vkh', 'འཁྱ': 'vkhy', 'འཁྲ': 'vkhr', 'འག': 'vg',
                      'འགྱ': 'vgy', 'འགྲ': 'vgr', 'འཆ': 'vch', 'འཇ': 'vj', 'འཐ': 'vth', 'འད': 'vd', 'འདྲ': 'vdr',
                      'འཕ': 'vph', 'འཕྱ': 'vphy', 'འཕྲ': 'vphr', 'འབ': 'vb', 'འབྱ': 'vby', 'འབྲ': 'vbr', 'འཚ': 'vtsh',
                      'འཛ': 'vdz', 'ཡ': 'y', 'ར': 'r', 'རྐ': 'rk', 'རྐྱ': 'rky', 'རྒ': 'rg', 'རྒྱ': 'rgy', 'རྔ': 'rng',
                      'རྗ': 'rj', 'རྙ': 'rny', 'རྟ': 'rt', 'རྡ': 'rd', 'རྣ': 'rn', 'རྦ': 'rb', 'རྨ': 'rm', 'རྨྱ': 'rmy',
                      'རྩ': 'rts', 'རྫ': 'rdz', 'རླ': 'rl', 'ལ': 'l', 'ལྐ': 'lk', 'ལྒ': 'lg', 'ལྔ': 'lng', 'ལྕ': 'lc',
                      'ལྗ': 'lj', 'ལྟ': 'lt', 'ལྡ': 'ld', 'ལྤ': 'lp', 'ལྦ': 'lb', 'ལྷ': 'lh', 'ཤ': 'sh', 'ས': 's',
                      'སྐ': 'sk', 'སྐྱ': 'sky', 'སྐྲ': 'skr', 'སྒ': 'sg', 'སྒྱ': 'sgy', 'སྒྲ': 'sgr', 'སྔ': 'sng',
                      'སྙ': 'sny', 'སྟ': 'st', 'སྡ': 'sd', 'སྣ': 'sn', 'སྣྲ': 'snr', 'སྤ': 'sp', 'སྤྱ': 'spy',
                      'སྤྲ': 'spr', 'སྦ': 'sb', 'སྦྱ': 'sby', 'སྦྲ': 'sbr', 'སྨ': 'sm', 'སྨྱ': 'smy', 'སྨྲ': 'smr',
                      'སྩ': 'sts', 'སྲ': 'sr', 'སླ': 'sl', 'ཧ': 'h', 'ཧྲ': 'hr', 'ཨ': 'A'}
        self.rareC = {'བེའུ': 'bevu', 'ཧུའུ': 'huvu', 'ཀིའུ': 'kivu', 'བྲའོ': 'bravo', 'སླེའུ': 'slevu',
                      'འགོའུ': 'vgovu', 'ཁྱེའུ': 'khyevu', 'མདེའུ': 'mdevu', 'རྔེའུ': 'rngevu', 'ཚུའུ': 'tshuvu',
                      'གཅེའུ': 'gcevu', 'རྟའུ': 'rtavu', 'ཁྱིའུ': 'khyivu', 'ཐེའུ': 'thevu', 'སྟེའུ': 'stevu',
                      'རྩེའུ': 'rtsevu', 'སླེའོ': 'slevo', 'ཤའུ': 'shavu', 'ཉེའུ': 'nyevu', 'སྨེའུ': 'smevu',
                      'རྟེའུ': 'rtevu', 'ཚའུ': 'tshavu', 'ཙེའུ': 'tsevu', 'གཡིའུ': 'g.yivu', 'སྤྲེའུ': 'sprevu',
                      'ལོའུ': 'lovu', 'གྲིའུ': 'grivu', 'སྤྱིའུ': 'spyivu', 'འབེའུ': 'bevu', 'གླེའུ': 'glevu',
                      'ལའུ': 'lavu', 'སྙེའུ': 'snyevu', 'ཕེའུ': 'phevu', 'རྡེའུ': 'rdevu', 'ཀྲུའུ': 'kruvu',
                      'ཁྲིའུ': 'khrivu', 'བྲེའུ': 'brevu', 'རྨེའུ': 'rmevu', 'གཏེའུ': 'gtevu', 'སྣེའུ': 'snevu',
                      'ཕྲའུ': 'phravu', 'དྲེའུ': 'drevu', 'སྡེའུ': 'sdevu', 'ནོའུ': 'novu', 'ཟེའུ': 'zevu',
                      'མིའུ': 'mivu', 'ཁེའུ': 'khevu', 'རྫེའུ': 'rdzevu', 'གཙེའུ': 'gtsevu', 'མཐེའུ': 'mthevu',
                      'མོའུ': 'movu', 'ཀེའུ': 'kevu', 'སྤའུ': 'spavu', 'དེའུ': 'devu', 'ཧེའུ': 'hevu',
                      'ཕྲེའུ': 'phrevu', 'ཚེའུ': 'tshevu', 'རྒེའུ': 'rgevu', 'བྲོའུ': 'brovu', 'བྱའུ': 'byavu',
                      'ཏེའུ': 'tevu', 'ཀོའུ': 'kovu', 'རེའུ': 'revu', 'ལིའུ': 'livu', 'ཡེའུ': 'yevu', 'མུའུ': 'muvu',
                      'སྒྲེའུ': 'sgrevu', 'ཁྲུའུ': 'khruvu', 'ལེའུ': 'levu', 'བྱེའུ': 'byevu', 'བྱིའུ': 'byivu',
                      'བྲའུ': 'bravu', 'འཕེའུ': 'phevu', 'གཅིའུ': 'gcivu', 'མཚེའུ': 'mtshevu', 'སྦྲེའུ': 'sbrevu',
                      'འགིའུ': 'givu', 'སྔེའུ': 'sngevu', 'ནེའུ': 'nevu', 'རྫིའུ': 'rdzivu', 'རྗེའུ': 'rjevu',
                      'སེའུ': 'sevu', 'ཐིའུ': 'thivu', 'སྒའུ': 'sgavu', 'སིའུ': 'sivu', 'མྱིའུ': 'myivu',
                      'ཙིའུ': 'tsivu', 'སྲིའུ': 'srivu', 'ནའུ': 'navu', 'བསེའུ': 'bsevu', 'གའུ': 'gavu',
                      'སྒེའུ': 'sgevu', 'ཀའུ': 'kavu', 'གྲེའུ': 'grevu', 'ཁྲེའུ': 'khrevu', 'སྤེའུ': 'spevu',
                      'སྒྱེའུ': 'sgyevu', 'དཔེའུ': 'dpevu', 'ཧྲུའུ': 'hruvu', 'ཐོའུ': 'thovu', 'ཤེའུ': 'shevu',
                      'ཐུའུ': 'thuvu', 'གཞུའུ': 'gzhuvu', 'དུའུ': 'duvu', 'ལྕེའུ': 'lcevu'}
        self.wazurC = {'སྟྭ': 'stw', 'གྭ': 'gw', 'ཞྭ': 'zhw', 'ཁྭ': 'khw', 'དྲྭ': 'drw', 'ཀྭའི': 'kwavi',
                       'བསྭོ': 'bswo', 'དྭ': 'dw', 'རྭ': 'rw', 'སྭ': 'sw', 'ཤྭ': 'shw', 'ཧྭ': 'hw', 'ལྭ': 'lw',
                       'ཕྱྭ': 'phyw', 'ཟྭ': 'zw', 'ཀྭ': 'kw', 'དྭོ': 'dwo', 'ཉྭ': 'nyw', 'ཚྭ': 'tshw', 'རྩྭ': 'rtsw',
                       'བསྭ': 'bsw', 'གྲྭ': 'grw'}
        self.A = {**self.roots, **self.rareC, **self.wazurC}
        # second part of the syllable
        self.NB = {'ག': 'ag', 'གས': 'ags', 'ང': 'ang', 'ངས': 'angs', 'ད': 'ad', 'ན': 'an', 'བ': 'ab', 'བས': 'abs',
                   'མ': 'am', 'མས': 'ams', 'འ': 'av', 'འང': 'avang', 'འམ': 'avam', 'འི': 'avi', 'འོ': 'avo', 'ར': 'ar',
                   'ལ': 'al', 'ས': 'as', 'ི': 'i', 'ིག': 'ig', 'ིགས': 'igs', 'ིང': 'ing', 'ིངས': 'ings', 'ིད': 'id',
                   'ིན': 'in', 'ིབ': 'ib', 'ིབས': 'ibs', 'ིམ': 'im', 'ིམས': 'ims', 'ིའང': 'ivang', 'ིའམ': 'ivam',
                   'ིའི': 'ivi', 'ིའོ': 'ivo', 'ིར': 'ir', 'ིལ': 'il', 'ིས': 'is', 'ུ': 'u', 'ུག': 'ug', 'ུགས': 'ugs',
                   'ུང': 'ung', 'ུངས': 'ungs', 'ུད': 'ud', 'ུན': 'un', 'ུབ': 'ub', 'ུབས': 'ubs', 'ུམ': 'um',
                   'ུམས': 'ums', 'ུའང': 'uvang', 'ུའམ': 'uvam', 'ུའི': 'uvi', 'ུའོ': 'uvo', 'ུར': 'ur', 'ུལ': 'ul',
                   'ུས': 'us', 'ེ': 'e', 'ེག': 'eg', 'ེགས': 'egs', 'ེང': 'eng', 'ེངས': 'engs', 'ེད': 'ed', 'ེན': 'en',
                   'ེབ': 'eb', 'ེབས': 'ebs', 'ེམ': 'em', 'ེམས': 'ems', 'ེའང': 'evang', 'ེའམ': 'evam', 'ེའི': 'evi',
                   'ེའོ': 'evo', 'ེར': 'er', 'ེལ': 'el', 'ེས': 'es', 'ོ': 'o', 'ོག': 'og', 'ོགས': 'ogs', 'ོང': 'ong',
                   'ོངས': 'ongs', 'ོད': 'od', 'ོན': 'on', 'ོབ': 'ob', 'ོབས': 'obs', 'ོམ': 'om', 'ོམས': 'oms',
                   'ོའང': 'ovang', 'ོའམ': 'ovam', 'ོའི': 'ovi', 'ོའོ': 'ovo', 'ོར': 'or', 'ོལ': 'ol', 'ོས': 'os'}
        # exceptions
        self.special = {'བགླ': 'bgla', 'མདྲོན': 'mdron', 'བརྡའ': 'brdav', 'བརྟའ': 'brtav'}
        self.wazur = {'ཧྭག': 'hwag', 'ཀྭས': 'kwas', 'ཁྭངས': 'khwangs', 'ཧྭང': 'hwang', 'ཀྭན': 'kwan', 'དྭགས': 'dwags',
                      'ཧྭགས': 'hwags', 'དྭངས': 'dwangs', 'ཏྭོན': 'twon'}
        self.exceptions = {**self.special, **self.wazur}
        # inversed lists
        self.C = {v: k for k, v in self.A.items()}
        self.D = {v: k for k, v in self.NB.items()}
        self.E = {v: k for k, v in self.exceptions.items()}

    def to_ant_syl(self, components):
        """

        :param components: the tuple outputed by SylComponents().get_parts(<syl>)
        :return: the AntTib of that syllable
        """
        if type(components) == 'list' or not components:
            return '***'
        else:
            part1 = components[0]
            part2 = components[1]
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
                    b = self.NB[part2]
                return a + b

    def from_ant_syl(self, syl):
        """

        :param syl: takes as input a AntTib syllable
        :return: its Tibetan unicode counterpart
        """
        if syl == '***':
            return '***'
        else:
            a = ''
            if syl in self.E:
                return self.E[syl]
            elif syl in self.C:
                return self.C[syl]
            else:
                i = len(syl) - 1
                while i >= 0:
                    if syl[:i] in self.C:
                        a = syl[:i]
                        break
                    i -= 1
            b = syl[len(a):]
            if b.startswith('v') or b.startswith('r') or b.startswith('l') or b.startswith('s'):
                b = 'a' + b
            if b == 'a':
                return self.C[a]
            else:
                return self.C[a] + self.D[b]

    def __is_punct(self, string):
        if '།' in string or '༎' in string or '༏' in string or '༐' in string or '༑' in string or '༔' in string or ';' in string or ':' in string:
            return True
        else:
            return False

    def __trim_punct(self, l):
        """
        :param l:    a list splitted on the punctuation with re.split() where the regex was
                        something like ((<punct>|<punct>)+)
        :return: the same list, only keeping one of the two punctuation elements re.split() gave
        """
        i = 0
        while i < len(l) - 1:
            if self.__is_punct(l[i]) and self.__is_punct(l[i + 1]):
                del l[i + 1]
            i = i + 1

    def to_ant_text(self, string):
        """

        :param string: a Tibetan text string
        :return: its counterpart in AntTib with the punctuation diminished to shads(;) and tershe(:)
        """
        # Todo : make a new class to deal with the punctuation instead of doing it here
        # Prepare the string : delete all extra punctuations
        # replace the tabs by normal spaces
        string = string.replace('   ', ' ')
        # replace all non-breaking tsek by a normal tsek
        string = string.replace('༌', '་')
        # delete all yigos
        string = re.sub('(༄༅+|༆|༇|༈)།?༎? ?།?༎?', '', string)
        # split on the punctuation. here, a paragraph is just a chunk of text separated by shads.

        # split on remaining punctuation
        paragraphs = re.split(r'(( *། *| *༎ *| *༏ *| *༐ *| *༑ *| *༔ *)+)', string)
        # trim the extra punctuation
        self.__trim_punct(paragraphs)
        strip_list(paragraphs)  # delete empty elements beginning or ending the list

        # replace all shads by a ';' and the tershe by a ':'
        for num, element in enumerate(paragraphs):
            if '།' in element or '༏' in element or '༐' in element or '༑' in element:
                paragraphs[num] = element.replace('།', ';').replace('༎', ';').replace('༏', ';').replace('༐',
                                                                                                        ';').replace(
                        '༑', ';')
            elif '༎' in element:
                paragraphs[num] = element.replace('༎', ';;')
            elif '༔' in element:
                paragraphs[num] = element.replace('༔', ':')

        # translate the syllables into pseudo-wylie
        parts = SylComponents()  # instantiate object
        ant_text = []
        for par in paragraphs:
            if ';' not in par and ':' not in par:
                par = re.sub(r'([^་]) ', r'\1-',
                             par)  # adds a - everywhere a space is not preceded by a tsek to find the merged particles
                par = re.sub(r'་$', '', par.replace('་ ', ' '))  # delete all tsek at the end of words
                ant_par = []
                words = par.split(' ')
                for word in words:
                    syls = word.split('་')
                    ant_word = []
                    for syl in syls:
                        # deals with the fusioned particles like མཐར་ that have become མཐའ ར་. we want to see 'mthav r'
                        # it is a bit of a hack because I already add a space instead of doing it with ' '.join()
                        if '-' in syl:
                            if syl.startswith(mark):
                                psyl = syl[1:].split('-')
                                ant_word.append(
                                        mark + self.to_ant_syl(parts.get_parts(psyl[0])) + ' ' + self.to_ant_syl(
                                                parts.get_parts(psyl[1])).replace('a', ''))
                            else:
                                psyl = syl.split('-')
                                ant_word.append(self.to_ant_syl(parts.get_parts(psyl[0])) + ' ' + self.to_ant_syl(
                                        parts.get_parts(psyl[1])).replace('a', ''))
                        else:
                            if syl.startswith(mark):
                                ant_word.append(mark + self.to_ant_syl(parts.get_parts(syl[1:])))
                            else:
                                ant_word.append(self.to_ant_syl(parts.get_parts(syl)))
                    ant_par.append('x'.join(ant_word))
                ant_text.append(' '.join(ant_par))
            else:
                ant_text.append(par)
        return ''.join(ant_text)

    def from_ant_text(self, string):
        """

        :param string: an AntTib string
        :return: its counterpart in Tibetan unicode
        """
        paragraphs = re.split(r'(( *; *| *: *)+)', string)
        # delete the last element of the list if it is an empty string
        strip_list(paragraphs)
        # trim the extra punctuation (see comment in to_pw_text)
        self.__trim_punct(paragraphs)
        ant_text = []
        for par in paragraphs:
            if ';' not in par and ':' not in par:
                ant_par = []
                par = re.sub(r' (r|s|vi|vo) ', r'-\1 ', par)
                words = par.split(' ')
                for word in words:
                    syls = word.split('x')
                    ant_word = []
                    for syl in syls:
                        # deals with the fusioned particles
                        # is a similar hack as for the previous function
                        if '-' in syl:
                            if syl.startswith(mark):
                                psyl = syl[1:].split('-')
                                ant_word.append(mark + self.from_ant_syl(psyl[0]) + ' ' + self.from_ant_syl(psyl[1]))
                            else:
                                psyl = syl.split('-')
                                ant_word.append(self.from_ant_syl(psyl[0]) + ' ' + self.from_ant_syl(psyl[1]))
                        else:
                            if syl.startswith(mark):
                                ant_word.append(mark + self.from_ant_syl(syl[1:]))
                            else:
                                ant_word.append(self.from_ant_syl(syl))
                    ant_par.append('་'.join(ant_word) + '་')
                ant_text.append(' '.join(ant_par))
            else:
                ant_text.append(par.replace(';', '།').replace(':', '༔'))
        ant_text = ''.join(ant_text)
        ant_text = re.sub(r'([^ང])་([༔།])', r'\1\2', ant_text)
        return ant_text

    def no_space(self, string):
        """

        :param string: a segmented Tibetan unicode string
        :return: the same string without the spaces between syllables (keeps all spaces at punctuation)
        """
        regexes = [r'([་|༌])\s',  # spaces preceded by a tsek
                   r'(ང[་|༌])\s',  # ང་ plus space
                   r'\s(ར)',  #
                   r'\s(ས)',
                   r'\s(འི)',
                   r'\s(འོ)']
        for regex in regexes:
            string = re.sub(regex, r'\1', string)
        return string