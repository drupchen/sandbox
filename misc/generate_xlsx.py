from xlwt import Workbook
from PyTib.common import open_file

# generating the spreadsheet showing the changes
raw = open_file('./lugs bstan.csv')


wb = Workbook()
for num, sentence in enumerate(raw.split('\n')):
    sheet = wb.add_sheet(str(num))
    for n, word in enumerate(sentence.split('\t')):
        sheet.write(0, n, word)

wb.save('lugs bstan.xls')