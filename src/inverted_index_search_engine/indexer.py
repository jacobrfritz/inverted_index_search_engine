from dataclasses import dataclass
from collections import defaultdict

from inverted_index_search_engine.interfaces import File


""" 
receives files and tokenized text and returns a dictionary mapping every word to the files and positions where it appears
"""


@dataclass
class Word:
    files: list[File]
    positions: list[int]


class Indexer:
    def __init__(self, files: list[File]):
        self.files = files

    def get_word_metadata(self):
        corpus = list({word for f in self.files for word in f.tokenized_text})
        words = {word: defaultdict(list) for word in corpus}
        for f in self.files:
            for i, word in enumerate(f.tokenized_text):
                words[word]["files"].append(f)
                words[word]["positions"].append(i)
        return words
