from __future__ import annotations

from collections import defaultdict
from Levenshtein import jaro_winkler

from inverted_index_search_engine.interfaces import File

"""
receives text map and searches 
for word matches by leventhein distance 
and returns the top few results
"""


class SearchEngine:
    def calculate_distance(self, input_word:str, word:str)->float:
        return round(jaro_winkler(input_word, word), 3)
    
    def get_closest_word(self, input_string:str, words:dict[str, list[File]]):
        """
        receives input string
        returns closest word from corpus
        """
        word_distances = {word : self.calculate_distance(input_string, word) for word in words.keys()}
        closest_word = sorted(word_distances, key = lambda w: word_distances[w], reverse=True)[0]
        return closest_word
        
    def get_ranked_files(self, input_word:str, words:dict, max_num_matches: int = 7)-> list[File]:
        word_count_per_file = {file : file.get_word_count(input_word) for word in words.values() for file in word}
        ranked_files = sorted(word_count_per_file, key= lambda w: word_count_per_file[w], reverse = True)[:max_num_matches]
        return ranked_files 
    
    def get_ranked_snippets(self, word:str, f:File, max_snippets: int = 3)->list[str]:
        snippets = list()
        words_in_text = [token for token in f.tokenized_text if token.get('token') == word.lower()]
        for match in words_in_text:
            snippets.append(f.raw_text[match['start']-30:match['end']+30])
        return snippets[:max_snippets]