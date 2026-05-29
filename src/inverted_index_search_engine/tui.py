from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, ListView, ListItem, Label
from textual.suggester import Suggester
from rich.table import Table
from inverted_index_search_engine.search_engine import SearchEngine


class AsyncSearchSuggester(Suggester):
    """
    Natively hooks into Textual's input loop.
    Asks the search engine for a fresh suggestion on every single keystroke.
    """
    def __init__(self, search_engine: SearchEngine, word_metadata: dict):
        # use_cache=False prevents Textual from serving stale, old keystroke lookups
        super().__init__(use_cache=False)
        self.search_engine = search_engine
        self.word_metadata = word_metadata

    async def get_suggestion(self, value: str) -> str | None:
        current_text = value.strip()
        if not current_text:
            return None
            
        # Get the word completion from your search engine
        closest_word = self.search_engine.get_closest_word(current_text, self.word_metadata)
        
        # Return the word if it matches, otherwise returning None hides the grey text
        return closest_word if closest_word else None


class Tui(App):
    def __init__(self, search_engine: SearchEngine, word_metadata: dict):
        super().__init__()
        self.search_engine = search_engine
        self.word_metadata = word_metadata

    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Input(
            placeholder="Type a search query...",
            id="search_input",
            # Inject the custom suggester directly into the widget configuration
            suggester=AsyncSearchSuggester(self.search_engine, self.word_metadata)
        )
        yield ListView(id="file_results")
        yield Footer()

    @work(thread=True, exclusive=True)
    def on_input_changed(self, event: Input.Changed) -> None:
        """
        Event handler handles ONLY the heavy background file searching.
        It no longer touches or interferes with the input's suggester property.
        """
        results_list = self.query_one("#file_results", ListView)
        
        # Clear UI list state safely
        self.call_from_thread(results_list.clear)
        current_text = event.value.strip()
        
        if current_text:
            # Get closest word to find the files mapped to it
            closest_word = self.search_engine.get_closest_word(current_text, self.word_metadata)
            search_results = self.search_engine.get_ranked_files(closest_word, self.word_metadata, 3)
            
            for file in search_results:
                item_widget = ListItem(Label(file.path.name))
                self.call_from_thread(results_list.append, item_widget)