from data_process_interface import DataProcessInterface
from word_counter import WordCounter
from buffered_writer import BufferedWriter
from util import Util
import os
from os.path import isfile, join

# 
class DocumentProcess(DataProcessInterface):
    
    # inventory the files designated for processing 
    def __init__(self, table_name_key):
        DataProcessInterface.__init__(self, table_name_key)
        
        #self.output_filename = parameters.get('output_filename')
        #self.output_folder = parameters.get('output_folder')
        util = Util()
        
        self.input_folder = util.getInputFolder(table_name_key)
        
        self.doc_no  = 1 # assumeing all docs are read form the begining to the end
        self.para_no = 1 
        self.sentance_no = 1
        self.word_no = 1 
        self.wordCounter = WordCounter()
        #self.bufferedWriter = BufferedWriter(self.output_folder,
        #                                     self.output_filename)
        
        self.bufferedWriter = BufferedWriter(util.getOutputFolder(table_name_key),
                                             '{}.json'.format(table_name_key))
        
        self.dict_={
            'documents':{},
            'paragraphs':{},
            'words': {},
            'word-documents': {}
        }
        
        self.current_doc_name = None
        
    #def getRecords(self):
    #    return self.records
    def getWordCounter(self):
        return self.wordCounter
    
    def getBufferedWriter(self):
        return self.bufferedWriter
        
        
    def process(self):
        
        i = 1
        for filename in self.getFilenameList(): 
            print('file name: ', filename)
            
            self.getWordCounter().clear()
            
            doc_id = self.getDOC_ID()
            fnpart = self.getFilenamePart(filename)
            expanded = self.getExpandedUrl(fnpart)
            
            self.current_doc_name = fnpart
            
            # r = {'PutRequest':{ 'Item': item } }
            
            if doc_id not in self.getDictionary()['documents']:
                item = {'pk': doc_id, 
                        'sk': 'DOCUMENT', 
                        'data': fnpart, 
                        'type': 'DOC'
                        }
                
                # self.getDictionary()['documents'][doc_id] = item
                item = self.typifyItem( item )
                item = {'PutRequest': {'Item': item}}
                self.getBufferedWriter().write(item)
            # breakup into paragraphs
            # print('process {}'.format(filename))
            
            #doc_name = '{}.{}'.format(self.getBufferedWriter().file_count, self.getBufferedWriter().root_name)
            doc_name = self.getBufferedWriter().formatOutFileName()
            print('{} starts in {}'.format(filename , doc_name))
            self.processPargraphs(doc_id, filename)
            
            self.doc_no += 1
        
        self.getBufferedWriter().flush()
        
    def postProcess(self):  
        # self.writeDictionaryFile()
        return 
    
    def getFilenameList(self):
        files = [f for f in os.listdir(self.input_folder) if isfile(join(self.input_folder, f))]
        onlyfiles = ['{}/{}'.format(self.input_folder, n ) for n in files if n.endswith('.txt')]
        return onlyfiles   
    
    def getDOC_ID(self):
        #self.doc_no += increment 
        return 'd.{}'.format(self.doc_no)
    
    def getPH_ID(self):
        # self.para_no += increment 
        return 'p.{}'.format(self.para_no)
    
    def getST_ID(self):
        # sentance id
        return 's.{}'.format(self.sentance_no)
    
    def getPD_ID(self):
        return 'p{}.d{}'.format(self.para_no, self.doc_no)
    
    #def getID(self):
    #    rc = self.id 
    #    self.id += 1
    #    return rc
    
    def processPargraphs(self, doc_id, filename):
        
        ord_no = 1
        
        # open a file and processself
        # paragraphs are considered to be unique...even though they may no be
        with open(filename, 'r') as f:
            # run through all documents
            # convert file name back to url
            for paragraph in f:
                para_id = self.getPH_ID() # 'ph#{}'.format(self.para_no)
                paragraph = paragraph.replace('\n','').rstrip().lstrip()   
          
                #self.processWords( paragraph )
                self.processSentences( paragraph)
                self.para_no += 1
                
    def sentences(self, paragraph):
        return paragraph
        
    def processSentences(self, paragraph):
        sk_id = self.getDOC_ID()
        para_id = self.getPH_ID()
        
        # make list of sentences
        for sentence in self.sentences( paragraph.lower() ).split('. '):
            sent_id = self.getST_ID()
            altsentence = sentence
            if len(altsentence)==0:
                altsentence='\n'
                
            item = {'pk': sk_id, 
                  'sk': sent_id, 
                  'data':  altsentence
                   }
            # process of a sentence
            
            self.sentance_no += 1
            
            item = self.typifyItem( item )
            item = {'PutRequest': {'Item': item}}
            self.getBufferedWriter().write(item)
            
            self.processWordToDocument( sentence ) 
            #
            # processUniqueWords( sentences )
    
    def processWordToDocument(self, sentence):
        '''
        make word to document relationship
        * make only one word-doc relationship per sentence
        
        '''
        doc_id = self.getDOC_ID()
        para_id = self.getPH_ID()
        sentence_id = 0
        
        # word-paragraph-document
        # opioid-1-1-2
        # opioid-2-2-2
        
        # make sentence unique list of word... avoid same word twice from same sentence
        
        uniqueList = set(self.spacifyPuncuation(sentence.lower()).split())
        
        for word in uniqueList:
            altword = word
            altsentence=sentence
            
            if len(altword) == 0 or altword == '\n' or altword == '':
                altword= 'BLANK-WORD'
            if len(altsentence)==0 or altword == '\n':
                altsentence = 'BLANK-LINE'
                
            w_cnt = self.getWordCounter().add(altword)
            
            word_unique_id = '{}.{}'.format(altword, w_cnt)
            
            item = {'pk': doc_id, 
                  'sk': word_unique_id, 
                  'data':  altsentence,
                  'title': self.current_doc_name.replace('.txt','') 
                   } 
            
            #word_doc_id = '{}.{}'.format(word, self.getPD_ID())
            #item = {'pk': word_doc_id, 
            #      'sk': sk_id, 
            #      'data':  sentence} 
            
            #self.getDictionary()['word-documents'][word_doc_id] = {'pk': word_doc_id, 
            #                                                  'sk': sk_id, 
            #                                                  'data':  sentence}   
            item = self.typifyItem( item )
            item = {'PutRequest': {'Item': item}}
            self.getBufferedWriter().write(item)
            
    def dep_processUniqueWords(self, sentence):
        
        sk_id = self.getDOC_ID()
        para_id = self.getPH_ID()
        for word in self.spacifyPuncuation(paragraph.lower()).split():
            #print('word: ', word)
            word_id = word
            
            # single word for all documents
            if word_id not in self.getDictionary()['words']:
                self.getDictionary()['words'][word_id] = {'pk': word_id, 
                                                          'sk': 'WORD', 
                                                          'data': word, 
                                                          'documents': [sk_id],
                                                          'sentence': [para_id]} 
            else:
                
                if sk_id not in  self.getDictionary()['words'][word_id]['documents']:
                    self.getDictionary()['words'][word_id]['documents'].append(sk_id)
                
      
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
                    typedItem[k] = {"N": str(item[k])} 
                   
        # print('typedItem: ', typedItem )
        return typedItem
  
        
        
    def writeDictionaryFileEither(self, output_type):
        ## output_type 'remote' or 'local'
        
        #put contents of dictionary into three files
        #document
        #words
        #word-document

       
        #if output_type == 'remote':
        #outputfile = '{}/{}'.format(self.output_folder, self.output_filename)
    
        outputfile = '{}/{}.{}'.format(self.output_folder, output_type, self.output_filename)
             
        #documents = self.getDictionary()['documents']
        
        
        ############ Documents
        # load up the records for the dump
        #
        self.records = {'documents': []}
        
        print('documents_output_limit: ', documents_output_limit )
        print('words_output_limit: ', words_output_limit)
        print('word_documents_output_limit: ', word_documents_output_limit)
        
        limit = 0
        for key in self.getDictionary()['documents']:
            # print('documents: ', self.getDictionary()['documents'][key])
            item = {}
            if output_type == 'remote':
                item = self.typifyItem(self.getDictionary()['documents'][key]) 
            else:
                item = self.getDictionary()['documents'][key]
                
            r = {'PutRequest':{ 'Item': item } }
            self.getRecords()['documents'].append( r )
            
            if documents_output_limit > 0:
                if limit < documents_output_limit:
                    limit += 1
                else:
                    break
                
        limit = 0    
        for key in self.getDictionary()['words']:
            
            if output_type == 'remote':
                item = self.typifyItem(self.getDictionary()['words'][key])  
            else:
                item = self.getDictionary()['words'][key]
                
            r = {'PutRequest':{ 'Item': item } }
            self.getRecords()['documents'].append( r )
            if words_output_limit > 0:
                if limit < words_output_limit:
                    limit += 1
                else:
                    break
        
        limit = 0
        for key in self.getDictionary()['word-documents']:
            
            if output_type == 'remote':
                item = self.typifyItem(self.getDictionary()['word-documents'][key])
            else:
                item = self.getDictionary()['word-documents'][key]
            
            r = {'PutRequest':{ 'Item': item } }
            
            self.getRecords()['documents'].append( r )
            
            if word_documents_output_limit > 0:
                if limit < word_documents_output_limit:
                    limit += 1
                else:
                    break
        
        with open(outputfile, 'w') as f:
            # recode the key with the id before writing
            f.write(json.dumps(self.getRecords()))    
            
    def writeDictionaryFile(self):
        self.writeDictionaryFileEither('local')
        self.writeDictionaryFileEither('remote') 
        

