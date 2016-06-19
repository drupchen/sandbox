import re
import zipfile

class MLD:
    def __init__(self, string):
        self.base_string = string
        self.layers = {'1': 'segmentation', '2': ''}
        self.dependency = []

    def __repr__(self):
        # generate a list of the layers
        layers = ' + '.join([key+value for key, value in self.layers.items()])

        # generate the first string_len characters separated on a new line every line_len characters
        string_len = 594
        line_len = 200
        start = '\n'.join([self.base_string[:string_len][i:i+line_len] for i in range(0, string_len, line_len)])+'[...]'

        return '\n'.join([layers, start])

    def create_layer(self, input, name):



test = MLD('བཀྲ་ཤིས་བདེ་ལེགས། '*200)
print(test)



'''
Layers:

    create layer()
        input : - processed base string that contains +, - or = signs and name for the layer
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

    export_indexed(suffix, layers)
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