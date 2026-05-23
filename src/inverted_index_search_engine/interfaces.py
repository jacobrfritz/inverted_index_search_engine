from pathlib import Path


class File:
    def __init__(self, path: Path, text: str):
        self.path = path
        self.raw_text = text
        self.tokenized_text: list[dict] = []

    def get_word_count(self, input_word:str):
        return len([word for word in self.tokenized_text if word.get('token') == input_word.lower()])
        
    def __repr__(self):
        return f"""
        File Name: {self.path.name}
    """
