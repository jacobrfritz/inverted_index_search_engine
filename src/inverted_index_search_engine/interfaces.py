from pathlib import Path



class File:
    def __init__(self, path:Path, text:str):
        self.path = path
        self.text = text
        self.tokenized_text:list[str] = []
        self.token_map:dict
        
    def __repr__(self):
        return f"""
        File Name: {self.path.name}\n
        Tokens: {len(self.tokenized_text)}
    """
    