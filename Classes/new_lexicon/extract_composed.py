import re

with open('lexicon.txt', 'r', -1, 'utf-8-sig') as f:
    entries = [line.strip() for line in f.readlines()]

syllabled = []
for entry in entries:
    syllabled.append(entry.split('་'))


parts = {}
for e in syllabled:
    word = e
    i = 0
    while i <= len(word)-1:
        if [word[i]] in syllabled:
            for j in range(i+1):
                del word[0]

        i += 1


print(parts)

com_entries = []
for e in entries:
    List = [word for word in syllabled if word != e]
    composed = re.sub(r'|'.join(List), '', e)
    if composed == '':
        com_entries.append(e)
print(com_entries)

#print(syllabled)