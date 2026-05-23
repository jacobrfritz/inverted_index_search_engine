import re

from inverted_index_search_engine.interfaces import File
from inverted_index_search_engine.stop_words import STOP_WORDS


""" 
receives the corpus, removes stop words, 
"""

class Tokenizer:
    def __init__(self, files: list[File]):
        self.files = files

    def tokenize(self) -> list[File]:
        out = list()
        
        word_pattern = re.compile(r"[a-zA-Z]+")

        for f in self.files:
            token_mappings = []
            raw_text = f.raw_text
            
            for match in word_pattern.finditer(raw_text):
                word = match.group().lower()
                
                if word not in STOP_WORDS:
                    token_mappings.append({
                        "token": word,
                        "start": match.start(),  
                        "end": match.end()  
                    })
            
            f.tokenized_text = token_mappings
            out.append(f)
            
        return out