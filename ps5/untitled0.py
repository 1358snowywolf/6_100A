class Map(object):
    def __init__(self, L1, L2):
        """ L1 is a list of unique int elements
            L2 is a list of unique lowercase str elements
            
            Creates two data attributes. 
            * map, a dict data attribute where the keys are each int in 
              L1 and the value associate with a key is the sorted list 
              of all words in L2 whose length equals that key. 
      
            * unused_list, a list data attribute containing elements in 
              L2 whose length do not equal any of the int values in L1. 
              Elements are sorted in lexicographical order. """
        self.dictionary = dict()
        self.unused_list = []
        
        for i in range(len(L2)):
            if(len(L2[i]) in L1):
                if(len(L2[i]) in self.dictionary):
                    self.dictionary[len(L2[i])].append(L2[i])
                else:
                    self.dictionary[len(L2[i])] = [L2[i],]
            else:
                self.unused_list.append(L2[i])
        
        for i in self.dictionary:
            self.dictionary[i].sort()
        self.unused_list.sort()
        
        for i in L1:
            if i in self.dictionary:
                continue
            
            self.dictionary[i] = []
        
    def get_map(self):
        """ Returns a copy of the map of ints to list of strings. """
        return self.dictionary.copy()

    def get_unused_list(self):
        """ Returns a copy of the list of unused strings. """
        
        return self.unused_list.copy()
    
    def __add__(self, other):
        """ Returns a new Map object whose map data attribute is a merge
        of self and other's maps. When merging, if self and other have 
        the same key, raise a ValueError. Otherwise, the new Map object's 
        map data attribute is all the keys in self and other along with 
        the keys' values. The new Map object's unused_list data attribute 
        is the sorted unique elements from the unused_lists of self and 
        other that are not in the new Map's map. """
        
        for i in self.dictionary:
            if(i in other.get_map()):
                raise ValueError
        
        new_dictionary = dict()
        new_list = []
        
        for i in self.dictionary:
            new_dictionary[i] = self.dictionary[i].copy()
        
        for j in other.get_map():
            new_dictionary[j] = other.get_map()[j].copy()
            
        for i in self.unused_list:
            if(i not in new_dictionary[len(i)]):
                new_list.append(i)
        
        for j in other.get_unused_list():
            if(j not in new_dictionary[len(j)]):
                new_list.append(j)
        
        new_list.sort()
        
        #very sacreligious
        answer = Map([], [])
        answer.dictionary = new_dictionary
        answer.unused_list = new_list
        
        return answer
    
a = Map([1,2,3], ["abc", "def", 'z', 'nmop'])
print(a.get_map())  # prints {1: ['z'], 2: [], 3: ['abc', 'def']}
print(a.get_unused_list())  # ['nmop']


b = Map([4], ["abc", "xyz", 'z', 'nmop', 'abcd'])
c = a+b
print(c.get_map())  # prints {1: ['z'], 2: [], 3: ['abc', 'def'], 4: ['abcd', 'nmop']}
print(c.get_unused_list())  # prints ['xyz']

d = Map([4], ['lmao'])
e = b + d