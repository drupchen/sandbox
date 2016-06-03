with open('segmented.txt', 'r', -1, 'utf-8-sig') as f:
    content = [line.strip() for line in f.readlines()]

conc = []
for line in content:
    words = line.split(' ')
    for num, word in enumerate(words):
        if word == 'བར་' and words[num-1] not in conc:
            conc.append(words[num-1])
print(len(' '.join(content).split(' ')))
with open('rules.txt', 'w', -1, 'utf-8-sig') as f:
    for c in conc:
        f.write(',,'+c+'- བ+ར་,,\n')