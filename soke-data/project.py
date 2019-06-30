import os
from os.path import isfile, join
class Project:
    def __init__(self, project_name, path):
        self.project_name = project_name
        self.path = path # '../../../data/{}/'.format( self.project_name )
        
    def getInputPath(self):
        return self.path
    
    def mkdir(self, path):
        try:
            #os.mkdir('../../data/{}/'.format( self.table_name_key ))
            os.mkdir(path)
            print ("Successfully created the directory %s " % path)
        except OSError:
            print ("directory %s exists" % path)
    
    def run(self):
        path = 'data/{}/'.format(self.project_name)
        curdir = os.getcwd()
        try:   
            print ("Start directory %s " % curdir)
            os.chdir('../../../')
            os.mkdir('data/')
            
        except OSError:
            print ("A Creation of the directory %s failed" % self.path)

        os.chdir('{}/'.format(curdir))
        
        self.mkdir(self.path)
        self.mkdir('{}/input/'.format( self.path ))   
        self.mkdir('{}/output/'.format( self.path )) 
        
         