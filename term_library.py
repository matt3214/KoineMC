import csv
import random

r = random.Random()

default_lib_path= "res/term_library/term_library_unique.csv"

class TermLibrary:

    def __init__(self, library_path=default_lib_path):
        self.library_path=library_path
        self.library=list(csv.reader(open(self.library_path,"r",encoding="utf-8")))

    def __str__(self):
        lib_size=len(self.library)
        return f"Library Object containing: {lib_size} entries. library_path: '{self.library_path}'"

    def get_relevant(self,item,loose=True,threshold=0,sample_size=20):
        
        item=item.lower().replace('.',' ').replace('_',' ')
        
        if not loose:
            matches= [term for term in self.library if term[0] in item]
        else:
            # set based analysis determinant on threshold
            
            # removes high frequency words like conjunctions and definite articles
            def remove_common(words:set):
                return words.difference({'to','of','and','the','with','in','for','was','by','from'})
            
            item_components=remove_common(set(item.split(' ')))
            matches= [term for term in self.library if len(item_components.intersection(remove_common(set(term[0].split(' ')))))>threshold]
        
        return r.sample(matches,min(sample_size,len(matches)))
        