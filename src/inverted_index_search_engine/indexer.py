from collections import defaultdict

from inverted_index_search_engine.interfaces import File


""" 
receives files and tokenized text and returns a dictionary mapping every word to the files and positions where it appears
"""


class Indexer:
    def __init__(self, files: list[File]):
        self.files = files

    def get_word_metadata(self)->dict[str,list[File]]:
        words = defaultdict(list)
        for f in self.files:
            for word in f.tokenized_text:
                if word['token'] not in words:
                    words[word['token']].append(f)
        return words