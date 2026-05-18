from pathlib import Path
from typing import Protocol

from inverted_index_search_engine.interfaces import File



""" 
Recursively search the directory for files of approved types and returns the text
"""

class FileType(Protocol):
    extension:str
    def get_text(self, file_name:Path)->str:...
    
    
class TextFile(FileType):
    extension=".txt"
    
    def get_text(self, file_name:Path)->str:
        with file_name.open('r', encoding="utf-8") as file:
            return file.read()


class FileSearcher:
    def __init__(self, base_path: str, file_types:list[FileType]):
        self.path = Path(base_path)
        self.file_types = file_types
        self.found_files = list()
        
    def get_files(self)->list[File]:
        for file_type in self.file_types:
            files = self.path.rglob('*'+file_type.extension)
            for f in files:
                text = file_type.get_text(f)
                found_file = File(
                    path=f,
                    text = text
                )
                self.found_files.append(found_file)
        return self.found_files