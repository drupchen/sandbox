with open('../PYTib/data/lexicon.txt', 'r', -1, 'utf-8-sig') as f:
    words = [word.strip() for word in f.readlines()]

length = []
for word in words:
    l = len(word.split('་'))
    if l not in length:
        length.append(l)
length = sorted(length, reverse=True)

print(length)