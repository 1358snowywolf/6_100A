import string

class PhraseTrigger(object):
    def __init__(self, trigger):
        self.trigger = trigger.lower()
    
    def is_phrase_in(self, text):
        updatedText = self.getRidOfPunctuation(text)
        
        return self.trigger in updatedText
    
    #helper methods
    def getRidOfPunctuation(self, text):
        text = text.lower()
        
        for i in range (len(string.punctuation)):
            text = text.replace(string.punctuation[i], ' ')
        
        for i in range (len(text)):
            j = i 
            removed = False
            
            while(j < len(text) and text[j] == ' '):
                removed = True
                j += 1
            
            if(removed):
                text = text[0:i] + " " + text[j:]
        
        return text

pt = PhraseTrigger("purple cow")
print(pt.getRidOfPunctuation("purple@#$%cow"))
print(pt.is_phrase_in("purple@#$%cow"))