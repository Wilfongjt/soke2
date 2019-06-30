from data_process_interface import DataProcessInterface
from util import Util
from buffered_writer import BufferedWriter
import os
from os.path import isfile, join
import json
from util import Util

class MovieProcess(DataProcessInterface):
    
    def __init__(self, table_name_key):
        DataProcessInterface.__init__(self, table_name_key)
        print('MovieProcess 1')
        self.dict_={
            table_name_key: {},
        }
        print('MovieProcess 2: ', self.dict_)
        util = Util()
        self.input_folder = util.getInputFolder(table_name_key)
        #self.output_filename = table_name_key
        #self.output_folder = output_folder #self.util.getOutputFolder(table_name_key)
        #self.buff_writer = output_file_name #BufferedWriter(self.output_folder, self.output_filename, count_limit=25)
        #self.bufferedWriter = BufferedWriter(util.getOutputFolder(table_name_key),table_name_key)
        
        self.bufferedWriter = BufferedWriter(util.getOutputFolder(table_name_key),
                                             '{}.json'.format(table_name_key))
    def getBufferedWriter(self):
        return self.bufferedWriter
    
    def getFilenameList(self, ext):
        print('MovieProcess getFilenameList 1')
        print('inputfolder: ', self.input_folder)
        files = [f for f in os.listdir(self.input_folder) if isfile(join(self.input_folder, f))]
        onlyfiles = ['{}/{}'.format(self.input_folder, n ) for n in files if n.endswith('.json')]
        return onlyfiles 
    
    def process(self):
        print('MovieProcess process 1')
        #input_fn = '{}{}'.format(self.util.getInputFolder(table_name_key))
        print('input_fn: ', self.input_folder)
        util = Util()
        input_fn = self.getFilenameList('.json')[0] # get first 
        print('input_fn: ', input_fn)
        with open(input_fn) as json_file:
        
            json_object = json.load(json_file)
                
            for item in json_object:

                item = util.typifyItem( item )
                item = {'PutRequest': {'Item': item}}
                self.getBufferedWriter().write(item)

    def writeDictionaryFile(self):    
        print('MovieProcess writeDictionaryFile 1')
        self.getBufferedWriter().flush() # write last of items if any
        
