from inverted_index_search_engine.file_search import FileSearcher, TextFile
from inverted_index_search_engine.tokenizer import Tokenizer
from inverted_index_search_engine.search_engine import SearchEngine
from inverted_index_search_engine.indexer import Indexer

from inverted_index_search_engine.tui import Tui


def run() -> None:
    fs = FileSearcher(
        base_path=r"/Users/jake/projects/ISYE6644", file_types=[TextFile()]
    )
    files = fs.get_files()
    tokenizer = Tokenizer(files)
    files = tokenizer.tokenize()
    indexer = Indexer(files) 
    word_metadata = indexer.get_word_metadata()
    search_engine = SearchEngine()
    app = Tui(search_engine, word_metadata)
    app.run()
    # matches = search_engine.get_ranked_matches('yoursearchword')
    # print('\n'.join([f'Match:  {match_name}\nDistance:  {inner_dict['distance']}\n' for match_name, inner_dict in matches.items()]))
