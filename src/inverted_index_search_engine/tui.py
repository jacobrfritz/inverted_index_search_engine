from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, ListView, ListItem, Label
from textual.suggester import SuggestFromList
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
        yield Input(
            placeholder="Type a search query...",
            id="search_input"  # Added an ID so we can easily query it
        )
        yield ListView(id="file_results")
        yield Footer()

    @work(thread=True, exclusive=True)
    def on_input_changed(self, event: Input.Changed) -> None:
        """Event handler called when the input text changes."""
        
        results_list = self.query_one("#file_results", ListView)
        search_input = self.query_one("#search_input", Input)
        
        # Clear previous results safely from the thread
        self.call_from_thread(results_list.clear)
        
        current_text = event.value.strip()
        print(current_text)
        if current_text:
            ranked_matches = self.search_engine.get_ranked_matches(current_text, 10)
            
            new_suggestions = [file.path.name for file in ranked_matches]
            print(new_suggestions)
            if new_suggestions:
                self.call_from_thread(
                    lambda: setattr(
                        search_input, 
                        "suggester", 
                        SuggestFromList(new_suggestions, case_sensitive=False)
                    )
                )
            else:
                self.call_from_thread(lambda: setattr(search_input, "suggester", None))

            for file in ranked_matches:
                item_widget = ListItem(Label(file.path.name))
                self.call_from_thread(results_list.append, item_widget)
        else:
            self.call_from_thread(lambda: setattr(search_input, "suggester", None))