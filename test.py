test = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt;">བཀྲ་</span><img src="C:/Users/NT$/Desktop/MyUI/Part-4/icons/align-justify.png" />ཤི<span style=" background-color:#00aa00;">ས་</span><span style=" color:#00ff00;">བདེ་ལེགས།</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#00ff00;"><br /></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#000000;"><br /></p></body></html>'''
import re
from bs4 import BeautifulSoup as Soup


soup = Soup(test, 'html.parser').html.body

for t in soup.stripped_strings:
    print(repr(t))

for par in soup.children:
    for char in par.stripped_strings:
        print(repr(char))

