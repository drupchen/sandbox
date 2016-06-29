from .common import DefaultOrderedDict, open_file, pre_process
from itertools import tee, islice
import os


class NGrams:
    def __init__(self):
        self.punct_regex = r'([༄༅༆༇༈།༎༏༐༑༔\s]+)'

    def __ngram_generator(self, iterable, n):
        # http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
        return zip(*((islice(seq, i, None) for i, seq in enumerate(tee(iterable, n)))))

    def _raw_ngrams(self, l, min=3, max=12):
        ngrams = DefaultOrderedDict(int)
        for a in range(min, max+1):
            grams = self.__ngram_generator(l, a)
            for g in grams:
                ngrams[g] += 1
        return [entry for entry in ngrams.items() if entry[1] > 1]

    def _ngrams_by_freq(self, raw, freq=10):
        ngrams = sorted(raw, key=lambda x: x[1], reverse=True)
        return [(n[1], ' '.join(n[0]), len(n[0])) for n in ngrams if n[1] >= freq]

    def _format_ngrams(self, l, sep='\t'):
        return '\n'.join([str(n[0]) + sep + n[1] + sep + str(n[2]) for n in l])

    def ngrams(self, raw_string, freq=10, min=3, max=12, unit='words'):
        l = pre_process(raw_string, unit)
        raw = self._raw_ngrams(l, min, max)
        by_freq = self._ngrams_by_freq(raw, freq)
        formatted = self._format_ngrams(by_freq)
        return formatted

    def __filtered_level(self, l, longer, level):
        shorter = set(self._raw_ngrams(l, level, level))
        substrings = set([s for s in shorter for l in longer if ''.join(s[0]) in ''.join(l[0])])
        print(level, list(shorter.difference(substrings)))
        return list(shorter.difference(substrings))

    def filtered_levels(self, raw_string, min, max, unit='words', freq=1):
        l = pre_process(raw_string, mode=unit)
        levels = []
        for i in reversed(range(min, max+1)):
            # fetch higher level for comparison in filtered_level()
            if len(levels) != 0:
                levels.append(self.__filtered_level(l, levels[-1], i))
            else:
                # adds the highest level without filtering it
                up_level = self._raw_ngrams(l, i+1, i+1)
                levels.append(self.__filtered_level(l, up_level, i))

        # flatten the levels in a single list
        grams = [gram for level in levels for gram in level]

        # return the frequence-sorted n-grams
        # similar to _ngrams_by_freq() except that it starts with a list, so there is no .items() method called
        by_freq = sorted(grams, key=lambda x: x[1], reverse=True)
        by_freq = [(n[1], ' '.join(n[0]), len(n[0])) for n in by_freq if n[1] >= freq]

        return self._format_ngrams(by_freq)


def ngrams_by_folder(input_path, freq=2, min=3, max=12, unit='words'):
    ng = NGrams()
    ngram_total = DefaultOrderedDict(int)
    for f in os.listdir(input_path):
        raw = open_file(input_path+f)
        syls = pre_process(raw, mode=unit).tsheks_only()
        ngrams = ng._raw_ngrams(syls, min, max)
        for n in ngrams:
            ngram_total[n[0]] += n[1]
    ngram_total = ng._ngrams_by_freq(ngram_total, freq)
    return ng._format_ngrams(ngram_total)