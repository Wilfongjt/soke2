import os
from os.path import isfile, join
from os import listdir
from pathlib import Path
import json

class Util:

    def getJSON():
        return

    def writeProcessConfig(self, process_config):
        with open('process_config.json', 'w') as f: 
            f.write(json.dumps(process_config)) 

    def readProcessConfig(self):
        with open('process_config.json','r') as f: 
            line = f.readlines() 
        
        jsobj = json.loads(line[0]) 
        return jsobj
    
    def typifyItem( self, item ):
        '''
        shallow first
        '''
        typedItem = {}
        keys = item.keys()
        # print('keys: ', keys)
        for k in keys:
            typ = type(item[k])
            isStr = isinstance(item[k], str)
            if isStr:
                typedItem[k] = {"S": item[k]}
            else:
                isInt = isinstance(item[k], int)
                if isInt:
                    #typedItem[k] = {"N": item[k]}
                    typedItem[k] = {"S": str(item[k])}

        return typedItem
    def makeDataProject(self, table_name_key):
        path = '../../data/{}/'.format(table_name_key)
        
        try:
            os.mkdir('data/')
            print ("Successfully created the directory %s " % path)
        except OSError:
            print ("Creation of the directory %s failed" % path)

        try:
            os.mkdir(path)
            print ("Successfully created the directory %s " % path)
        except OSError:
            print ("Creation of the directory %s failed" % path)

        try:
            path = os.mkdir('{}output'.format(path))
            print ("Successfully created the directory %s " % path)
        except OSError:
            print ("Creation of the directory %s failed" % path)

        try:
            path = os.mkdir('{}input'.format(path))
            print ("Successfully created the directory %s " % path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        
    def depmakeTableDataFolder(self, table_name_key):

        # path = './{}/'.format(table_name_key)
        # os.mkdir('../data/')
        path = '../data/{}/'.format(table_name_key)
        
        try:
            os.mkdir('../data/')
            print ("Successfully created the directory %s " % path)
        except OSError:
            print ("Creation of the directory %s failed" % path)


        
        try:
            os.mkdir(path)
            print ("Successfully created the directory %s " % path)
        except OSError:
            print ("Creation of the directory %s failed" % path)

        try:
            path = os.mkdir('{}output'.format(path))
            print ("Successfully created the directory %s " % path)
        except OSError:
            print ("Creation of the directory %s failed" % path)

        try:
            path = os.mkdir('{}input'.format(path))
            print ("Successfully created the directory %s " % path)
        except OSError:
            print ("Creation of the directory %s failed" % path)


    def getInputFolder(self, table_name_key):
        return '../../../data/{}/input'.format(table_name_key)
        #return '{}/{}'.format(os.getcwd(),table_name_key)
        

    def getOutputFolder(self,table_name_key):
        return '../../../data/{}/output'.format(table_name_key)
        #return '{}/{}/output'.format(os.getcwd(),table_name_key)

    
    def makeOutputFolder(self, outputfolder):

        config = Path(outputfolder)

        if not config.exists():
            os.mkdir(outputfolder)


    def getFileList(self, path, ending=None):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f) )]
        if ending != None:
            onlyfiles = [f for f in onlyfiles if f.startswith(ending) or f.endswith(ending)]
        return onlyfiles

    def getTableDefinitions(self, path, ending='table_definitions.json'):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f) )]
        if ending != None:
            onlyfiles = [f for f in onlyfiles if f.startswith(ending) or f.endswith(ending)]
        return onlyfiles

    def file_exists(self, folder, filename):
        exists = os.path.isfile('{}/{}'.format(folder, filename))
        return exists

    def showDictionary(self, _dict, limit = 0):
        cnt = 0
        for i in _dict:
            if limit > 0:
                cnt += 1
                if cnt > limit:
                    print('...')
                    break

            print('--', i, _dict[i], '\n')

    def getMax(self, attributeName, sourceDict):
        '''
        finds the largest number in a dictionary
        '''
        rc = 0

        for p in sourceDict:
            m = max(sourceDict[p][attributeName])
            if m > rc:
                rc = m

        return rc
    '''
    def make_key(self, item):
        rc = item['pk']
        if item['type'] == 'DOC-PH':
            rc = 'doc-{}-ph-{}'.format(item['pk'], item['doc_id'])

        return

    def setKeyToId(self, sourceDict):
        # problem: JSON.dump and JSON.load convert numeric to string key. this causes problems
        # * assumes sourceDict has an id attribute
        # * converts string key to numeric key by swapping the id attribute for the current key

        # for item in sourceDict:

        return {self.make_key(sourceDict[d]): sourceDict[d] for d in sourceDict}
        # return {sourceDict[d]['pk']: sourceDict[d] for d in sourceDict}
    '''
    '''
    def getOrderizedList(self, paragraph_dict, attName='paragraph'):
        orderAttribute = 'ord_nos'

        order_list = range(1, maxo)
        return [paragraph_dict[p][attName] for i in pageno_list for p in paragraph_dict if i in paragraph_dict[p][orderAttribute]]
    '''
    def show(self, sourceDict, limit=0):
        i = 0
        for p in sourceDict:
            if limit > 0:
                if i < limit:
                    print(p, sourceDict[p] )
                    i += 1
                else:
                    break

    def stringify(self, key_list):

        if len(key_list) == 0:
            return []

        if not (type(key_list[0] is int)):
            return key_list

        return [ str(k) for k in key_list]

    def writeSampleDocument(self, outputfolder, outputfilename, contents):
        with open('{}/{}'.format(outputfolder, outputfilename), 'w') as f:
                f.write(contents)

    def getSampleDocumentContents1(self):
        sample_doc = 'Will a form be developed to provide guidance on compliance for the new opioid education requirements related to implementing the Start Talking Form, and opioid disclosure form, required by Public Act 246 of 2017?'
        sample_doc += '\n \n'
        sample_doc += 'The Department of Health and Human Services (DHHS) and Licensing and Regulatory Affairs (LARA) worked with various health care providers and stakeholders in developing a single page form that can be used to meet the requirements of this new law. This new form can be found under the “Prescribers” tab at the DHHS website: www.michigan.gov/stopoverdoses.'
        sample_doc += '\n \n'
        sample_doc += ' Is a provider required to use the state’s form? '
        sample_doc += '\n \n'
        sample_doc += '         No, but the provider will have to use a similar form that is saved to the patient’s medical record and complies with the requirements of Public Act 246 of 2017'

        return sample_doc
