from __future__ import annotations

from Levenshtein import jaro_winkler

from inverted_index_search_engine.interfaces import File

"""
receives text map and searches 
for word matches by leventhein distance 
and returns the top few results
"""


class SearchEngine:
    def __init__(self, files:list[File]):
        self.files = files

    def calculate_distances(self, input_word:str, f:File):
        for word in f.tokenized_text:
            word['current_distance'] = round(jaro_winkler(input_word, word['token']), 3)
        return f

    def get_ranked_matches(self, input_word:str, max_num_matches: int = 7)-> list[File]:
        augmented_files = list() 
        for file in self.files:
            file_with_distance = self.calculate_distances(input_word, file)
            augmented_files.append(file_with_distance)

        ranked_augmented_files = sorted(augmented_files, key=lambda file: file.get_word_count(input_word), reverse=True)[:max_num_matches]
        return ranked_augmented_files