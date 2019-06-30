from interface import implements, Interface 
    
class ProcessInterface(Interface):
    
    def getClassName(self): pass
    def preProcess(self): pass
    def process(self): pass
    def postProcess(self): pass
    def run(self):pass