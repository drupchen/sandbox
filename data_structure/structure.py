import re
import zipfile
from  collections import OrderedDict, defaultdict


class MLD:
    def __init__(self, mld=None):
        self.base_string = ''
        self.layers = defaultdict(dict)
        self.dependency = []
        self.file_name = ''
        self.metadata = ''

        # if a mld file is given as argument
        if mld.endswith('.mld'):
            # find the name from the file name
            self.file_name = mld.split('/')[-1].replace('.mld', '')
            # read the zip
            zf = zipfile.ZipFile(mld, 'r')

            # Populate the object variables
            # list the files in the zip
            filenames = zf.namelist()
            # read the base string to base_string
            self.base_string = str(zf.read('base_string'), 'utf-8')
            # populate the layer dict
            layers = [l for l in filenames if re.match('[0-9]+', l)]
            for layer in layers:
                string = str(zf.read(layer), 'utf-8')
                self.import_layer(string)
        elif mld:
            self.base_string = mld

    def import_layer(self, name, string):
        lines = [(line.split('\t')[0], line.split('\t')[1]) for line in string.split('\n')]
        flattened = {}
        idx = 0  # the index of the base string
        val = 1  # the string obtained from the operations
        for index, modif in lines:
            temp = ['', '']  # simulates the key and value to add to flattened
            if index in flattened:
                temp = [index, flattened[index]]
            operation = modif[0]
            modified = modif[1:]
            if temp[idx] == '':
                temp[idx] = index

            if temp[idx] == '' or index == temp[idx]:
                if operation == '+':
                    if temp[val] == '':
                        temp[val] = modified+'_'
                    else:
                        temp[val] = temp[val][:-1]+modified+temp[val][-1]
                elif operation == '=':
                    temp[val] = temp[val][:-1] + modified
                elif operation == '-':  # assumes that there is at least on character in the string
                    temp[val] = temp[val][:-1]+ '-'
            flattened[temp[0]] = temp[1]
        self.layers[name].update(flattened)

    def export_view(self, layers=''):
        """
        method to export a view of the multi-layered data
        :param layers: provide references of the layers to apply separated by '+'
        :return: a string where none or the specified layers have been applied
        """
        if layers == '':
            return self.base_string
        else:
            layers = layers.split('+')
            view = ''
            for num, char in enumerate(self.base_string):
                # searches in all layers if the current index exists
                # todo : try to merge all layers first
                temp = char
                for l in self.layers:
                    if str(num) in self.layers[l]:
                        modif = self.layers[l][str(num)]
                        # if modif is only 1 char, it can either be a deletion ('-') or a replacement
                        if len(modif) == 1:
                            if modif == '-':
                                # delete the current char
                                temp = ''
                            else:
                                # replace the current char
                                temp = modif
                        # if it has more than a char, 1. either an addition (xxx_), or 2. an addition and a deletion (xxx-) or 3. an addition and a replacement (xxxy)
                        # 1. add modif before the current index char
                        elif modif.endswith('_'):
                            temp = temp[:-1]+modif+temp[-1]
                        # 2. delete current index char
                        elif modif.endswith('-'):
                            temp = temp[:-1]+modif[:-1]
                        # 3. apply the addition and replace the current index char
                        else:
                            temp = temp[:-1]+modif
                view += temp
            return view

    def write_mld(self):
        with zipfile.ZipFile(self.file_name+'.mld', 'w', zipfile.ZIP_DEFLATED) as z:
            z.writestr('base_string', self.base_string)
            for l in self.layers:
                z.writestr(l, self.layers[l])

    def __repr__(self):
        if type(self.base_string) is str:
            # generate a list of the layers
            layers = ' + '.join([key+value for key, value in self.layers.items()])

            # generate the first string_len characters separated on a new line every line_len characters
            string_len = 594
            line_len = 200
            start = '\n'.join([self.base_string[:string_len][i:i+line_len] for i in range(0, string_len, line_len)])+'[...]'

            return '\n'.join([layers, start])
        else:
            return 'non-valid file'




test = MLD('བཀྲ་ཤིས་བདེ་ལེགས། ')
li = '0\t=P\n0\t+བ\n0\t+ྱ\n0\t+་\n0\t=K'
test.import_layer('test', li)
print(li)
print(test.export_view(layers='test'))
#print(MLD('./test.mld'))


'''
Layers:

    flatten_layer()
        input : a layer file
        output : flattens all the operations into a single string following this scheme:
                    z   : replace the char at current index with z
                    xyz : replace the char at current index by z and add xy before the char
                    xy_ : keep the char at current index and add xy before it
                    xy- : delete the char at current index and add xy before it
                    -   : delete the char at current index

    create layer()
        input : - processed base string that contains +, - or = signs and name for the layer
                note : regroup all the characters preceded by a + in a single operation
                - compares  1. either the base string (default) or the provided indexed file
                   and 2. the processed string minus modifications and breaks if different
                - can compare to either an index file (export_indexed() ) or to the base_string
        Action : adds an entry in self.layers with the name and the layer as the key.

    delete layer()
        - deletes the layer corresponding to the name given

    rename_layer()
        input : old_name, new_name

    layer_dependency()
        keeps a dict of layers with the name/serial number of its dependencies


Output:

    export_flattened(suffix, layers)
        generates a txt file with the given suffix.
        The output string is the base string on which the given layers have been applied.
        the raw string is given if layers equals ''

    cache_indexed(suffix, layers)
        the output is the the same string than export_flattened(), but together with the indexes
        of each character referring to the base string.


Metadata:

    fields to have :
        id : int, generated number corresponding to the
        name : string, human-readable name
        dependencies : list of names or ids
        author : string
        description : multi-line string
        project : path to a project file (used to copy the meta-data of the file)

'''
'''
layer layout :
    index\t+char    # add a character before index
    index\t-        # deletes the character at index
    index\t=char    # replaces the character at index
'''