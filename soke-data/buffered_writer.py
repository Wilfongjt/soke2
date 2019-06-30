import json
class BufferedWriter:
    def __init__(self, out_folder, out_name, table_name_key=None, ext='.json' ,count_limit=25):
        # out_folder is /a/b 
        # out_name is with extention 'somefile.json' 
        # ext='.json' 
        # count_limit=25 
        self.folder = out_folder # no slash at end
        self.out_file_name = out_name
        #self.root_name = out_name # include extention
        if table_name_key == None:
            self.table_name_key = out_name.replace(ext,'') # remove extention assume filename is table name
        else:
            self.table_name_key = table_name_key
            
        self.buffer = [] 
        self.file_count = 0
        self.limit = count_limit
        self.item_count = 0
        self.word_counts = {} # dict of words with a counter {'the' : 1, 'data': 2} 
    
    def formatOutFileName(self):
        #print('folder: ', self.folder, ' file_count: ', self.file_count, ' out_file_name: ', self.out_file_name)
        return '{}/{}.{}'.format(self.folder, self.file_count, self.out_file_name)
    
    def write(self, item):
        
        self.buffer.append(item)
            
        if len(self.buffer) == self.limit:
            # with open('{}/{}.{}'.format(self.folder, self.file_count, self.root_name), 'w') as f:
            with open(self.formatOutFileName(), 'w') as f:    
                # recode the key with the id before writing
                #final = {'documents': self.buffer}
                final = {self.table_name_key: self.buffer}
                f.write(json.dumps(final))
                #f.write(json.dumps(self.buffer))
                self.file_count += 1
                self.buffer=[]
            
    def flush(self):
        if len(self.buffer) > 0:
            
            #with open('{}/{}.{}'.format(self.folder, self.file_count, self.root_name), 'w') as f:
            with open(self.formatOutFileName(), 'w') as f:     
                # recode the key with the id before writing
                #final = {'documents': self.buffer}
                #final = {self.root_name: self.buffer}
                
                final = {self.table_name_key: self.buffer}
                f.write(json.dumps(final))
                # f.write(json.dumps(self.buffer))
                self.file_count = 0
                
                self.buffer=[]   