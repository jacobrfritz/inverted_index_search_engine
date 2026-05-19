from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog, Input
from rich.table import Table
from inverted_index_search_engine.search_engine import SearchEngine

"""
textual tui that triggers the search engine service to a begin a search or switch to a new one
"""



class Tui(App):
    def __init__(self, search_engine:SearchEngine):
        super().__init__()
        self.search_engine = search_engine 

    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Input()
        yield RichLog()
        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Event handler called when a button is pressed."""
        current_text = event.value.strip()
        ranked_matches = self.search_engine.get_ranked_matches(current_text)
        text_log = self.query_one(RichLog)
        text_log.write(ranked_matches)