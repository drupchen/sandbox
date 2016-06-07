import re
string = ''

left = 5
right = 5

# matches a syllable constituted of zero or one non-punctuation + zero or more punctuation
context = r'[^་༌།༎༏༐༑༔ ]*[་༌།༎༏༐༑༔ ]*'
to_match = []

concordances = {}
for match in to_match:
    # find all occurrences of the current regex together with the contexts
    occurrences = re.findall('('+context*left+')('+match+')('+context*right+')', string)