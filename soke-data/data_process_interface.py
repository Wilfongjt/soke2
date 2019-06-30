from interface import implements, Interface
from process_interface import ProcessInterface
import json
class DataProcessInterface(implements(ProcessInterface)):

    '''
    provides interface to file holding data
    provides some utility data processing functions
    '''
    def __init__(self, file_name_key):
        self.file_name_key = file_name_key
        #util = Util()
        #self.input_folder = parameters.get('input_folder')
        #self.output_folder = parameters.get('output_folder')
        #self.input_folder = util.getInputFolder(file_name_key) #parameters.get('input_folder')
        #self.output_folder = util.getOutputFolder(file_name_key) #parameters.get('output_folder')

        self.dict_ = {}
        self.records = []

    def getClassName(self):
        '''
            returns the name of the class
        '''
        return self.__class__.__name__

    def getRecords():
        '''
        self.records holds a list of data items in their final state,
        ready to be loaded into DynamoDb
        '''
        return self.records

    def getDictionary(self):
        '''
        holds the objects in seperate lists:
        - documents, paragraphs, sentences, words... so far
        '''
        return self.dict_

    def run(self):
        self.preProcess()
        self.process()
        self.postProcess()
        return self


    def preProcess(self):
        # raise Exception('{} preProcess not implemented'.format(getClassName()))
        # print('DataProcessInterface.preProcess')
        # just returning allows run() preProcess() when not defined
        #self.records = []
        #self.dict_ = {}
        return

    def process(self):
        '''
        process raw data in self.dict_ into self.records

        '''
        print('DataProcessInterface setup process steps here')
        raise Exception('{}.process() not implemented'.format(getClassName()))
        return

    def postProcess(self):
        # print('DataProcessInterface.postProcess')
        # just returning allows run() preProcess() when not defined
        return

    def spacifyPuncuation(self, line):
        # add spaces around puncuation
        line = line.replace(':',' : ')
        line = line.replace('.',' . ')
        line = line.replace('*',' * ')
        line = line.replace('?',' ? ')
        line = line.replace('(',' ( ')
        line = line.replace(')',' ) ')
        line = line.replace('[',' [ ')
        line = line.replace(']',' ] ')
        line = line.replace('{',' { ')
        line = line.replace('}',' } ')
        line = line.replace(',',' , ')
        line = line.replace('\'',' \' ')
        line = line.replace('’',' \' ')
        line = line.replace('"',' " ')
        line = line.replace('”',' " ') # yes this is a duplicate, leave
        line = line.replace('“',' " ') # yes this is a duplicate, leave
        line = line.replace('/',' / ')
        line = line.replace('\\',' \\ ') # doesnt work
        return line

    def getExpandedUrl(self, filename):
        rc = filename
        rc = rc.replace('..', '/')
        return rc

    def getFilenamePart(self, filename):
        reverse = filename[::-1]
        rc = ''
        for c in reverse:
            if c is '/':
                break
            rc += c
        return rc[::-1]


    
    
    def writeDictionaryFile(self):
        '''
        put contents of dictionary into a file
        the dictionary has already been processed and stored in self.records

        '''
        outputfile = '{}/{}'.format(self.output_folder, self.output_filename)

        with open(outputfile, 'w') as f:
            # recode the key with the id before writing
            f.write(json.dumps(self.getRecords()))
