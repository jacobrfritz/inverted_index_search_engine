import re

from inverted_index_search_engine.interfaces import File
from inverted_index_search_engine.stop_words import STOP_WORDS


""" 
receives the corpus, removes stop words, 
"""

class Tokenizer:
    def __init__(self, files: list[File]):
        self.files = files

    def _get_word_count(self, word:str, f:File):
        return len([word['token'] for word in f.tokenized_text if word['token'] == word])
    
    def tokenize(self) -> list[File]:
        out = list()
        
        word_pattern = re.compile(r"[a-zA-Z]+")

        for f in self.files:
            token_mappings = []
            
            for match in word_pattern.finditer(f.raw_text):
                word = match.group().lower()
                
                if word not in STOP_WORDS:
                    token_mappings.append({
                        "token": word.lower(),
                        "start": match.start(),  
                        "end": match.end(),
                        "word_count": self._get_word_count(word, f)
                    })
            
            f.tokenized_text = token_mappings
            out.append(f)
            
        return out