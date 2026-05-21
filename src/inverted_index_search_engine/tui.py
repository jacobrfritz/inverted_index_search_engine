from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog, Input, ListView, ListItem, Label
from rich.table import Table
from inverted_index_search_engine.search_engine import SearchEngine

"""
textual tui that triggers the search engine service to a begin a search or switch to a new one
"""


class Tui(App):
    def __init__(self, search_engine: SearchEngine):
        super().__init__()
        self.search_engine = search_engine

    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Input()
        yield ListView(id="file_results")
        yield Footer()

    @work(thread=True, exclusive=True)
    def on_input_changed(self, event: Input.Changed) -> None:
        """Event handler called when a button is pressed."""
        
        results_list = self.query_one("#file_results", ListView)
        self.call_from_thread(results_list.clear)
        
        current_text = event.value.strip()
        if current_text:
            ranked_matches = self.search_engine.get_ranked_matches(current_text, 1)
            for word, item in ranked_matches.items():
                files = set(item['files'])
                self.call_from_thread(results_list.append, ListItem(Label(word)))
                for file in sorted(files, key=lambda f: f.path.name):
                    item_widget = ListItem(Label(file.path.name))
                    self.call_from_thread(results_list.append, item_widget)
