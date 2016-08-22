from PyTib.common import open_file, write_file

raw = open_file('./khabda.csv').split('\n')
for line in raw:
    parts = line.split(',')
    file_num = parts[1]
    link = parts[5]
    title = parts[6]
    author = parts[7]
    article = parts[8][len(author):]
    write_file('khabda_files/'+file_num+'_'+title+'.txt', link+'\t'+author+'\t'+title+'\n'+article)

