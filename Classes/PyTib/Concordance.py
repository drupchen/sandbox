import re
with open('/home/drupchen/PycharmProjects/sandbox/Classes/new_lexicon/segmented.txt', 'r', -1, 'utf-8-sig') as f:
    string = f.read()

left = 5
right = 5
# matches a syllable constituted of zero or one non-punctuation + zero or more punctuation



to_match = []
# find all words marked with *
words = string.split()
for word in words:
    if word.startswith('#'):
        to_match.append(word)
to_match = sorted(list(set(to_match)))

concordances = []
for match in to_match:
    # find all occurrences of the current regex together with the contexts
    i = 0
    while i <= len(words)-1:
        if words[i] == match:

            left_context = []
            l = 1
            while i-l >= 0 and i-l >= i-left:
                left_context.insert(0, words[i-l])
                l += 1

            right_context = []
            r = 1
            while i+r <= len(words) and i+r <= i+right:
                right_context.append(words[i+r])
                r += 1

            concordances.append((' '.join(left_context), match, ' '.join(right_context)))
        i += 1

with open('conc.csv', 'w', -1, 'utf-8-sig') as f:
    for c in concordances:
        f.write(c[0]+' \t'+c[1]+' '+c[2]+'\n')