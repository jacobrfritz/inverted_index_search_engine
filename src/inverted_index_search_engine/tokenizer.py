import re

from inverted_index_search_engine.interfaces import File
from inverted_index_search_engine.stop_words import STOP_WORDS


""" 
receives the corpus, removes stop words, 
"""


class Tokenizer:
    def __init__(self, files: list[File]):
        self.files = files

    def extract_text(self, text: str):
        return re.sub(r"[^a-zA-Z\s]", "", text)

    def split_words(self, text: str) -> list[str]:
        single_space_text = " ".join(text.split())
        return single_space_text.split()

    def remove_stop_words(self, text: list[str]) -> list[str]:
        return [word for word in text if word not in STOP_WORDS]

    def tokenize(self) -> list[File]:
        out = list()
        for f in self.files:
            text_only = self.extract_text(f.text.lower())
            words = self.split_words(text_only)
            f.tokenized_text = self.remove_stop_words(words)
            out.append(f)
        return out
