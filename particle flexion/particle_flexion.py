import re
import os

#############
# Read the particles and exceptions files
#############

for file in os.listdir('./RULES/'):
    if file.endswith(".txt"):
        # read particles list
        if file == 'particles.txt':
            try:
                with open('./RULES/' + file, 'r', -1, 'utf-8-sig') as f:
                    particles = f.read().split('\n')
            except:
                print("\nSave the EXCEPTIONS file as UTF-8 and try again.")
                input()
        # read exceptions list
        elif file == 'exceptions.txt':
            try:
                with open('./RULES/' + file, 'r', -1, 'utf-8-sig') as f:
                    content = f.read().split('#')
            except:
                print("\nSave the PARTICLES file as UTF-8 and try again.")
                input()
        else:
            print('\n'+file+' is not a supported file.')
            input()
    else:
        print("\nThe files with particles and exception rules must be raw text files.")
        input()

############
# Prepare the regex including all particles and exceptions
############

# prepare the particles
flexion = []
for particle in particles:
    if particle != '':
        parts = particle.split('***')
        flexion.append((parts[0], parts[1]))
accords = {}
for elt in flexion:
    if elt[1] in accords:
        accords[elt[1]] = accords[elt[1]]+elt[0]
    else:
        accords[elt[1]] = elt[0]

# prepare the exceptions
exceptions = {}
for case in content:
    exception = case.split('\n')
    if len(exception) == 3:
        exceptions[exception[0]] = exception[1] 

############
# Create the regex
############

regex = '('
for accord in accords.keys():
    particle = accord
    letters = accords[particle]
    regex += '[^'+letters+']་'+particle+'[་༌།༎༏༐༑༔]+'
    ###
    # include exceptions where needed
    if particle in exceptions:
        regex += '(?!'+exceptions[particle]+')'
    #
    ###
    regex += '|'
if regex.endswith('|'):
    regex = regex[:-1] # removing the extra '|' character
regex += ')'

############
# Applying the regex to the files in the IN folder
############

# check file format, open and apply regex
for file in os.listdir('./IN/'):
    if file.endswith(".txt"):
    #todo - replace \n by \s try: with open('drugs') as temp_file: \n drugs = [line.rstrip('\n') for line in temp_file]
        try:
            with open('./IN/' + file, 'r', -1, 'utf-8-sig') as f:
                current_file = f.read()
        except:
            print("Save all IN files as UTF-8 and try again.")
            input()
    else:
        print("\nSave all IN files as text files and try again.")
        input()

    # apply regexes
    marker = '༼༚༽'
    current_file = re.sub(regex, r'\1'+marker, current_file)

    # write a new file
    with open('./OUT/' + 'new_' + file, 'w', -1, 'utf-8-sig') as f:
        f.write(current_file)
