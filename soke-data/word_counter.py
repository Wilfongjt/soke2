class WordCounter(dict):
                
    def add(self, word):
        if word not in self:
            self[word]=1
        else:
            self[word]+=1
            
        return self[word] # return the new count
    
    def get(self, word):
        rc = 0
        if word in self:
            rc = self[word]
            
        return rc # return current count
    
    #def clear(self):
    #    # empty the dictionary 
    #    self.clear()
        
#wordCounter = WordCounter()
#assert wordCounter.add('the') == 1
#assert wordCounter.add('The') == 1
#assert wordCounter.get('test') == 0
#assert wordCounter.get('the') == 1
#assert wordCounter.get('The') == 1
#assert wordCounter.add('The') == 2
#assert wordCounter.get('The') == 2