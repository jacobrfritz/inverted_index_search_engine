from Levenshtein import jaro_winkler

"""
receives text map and searches 
for word matches by leventhein distance 
and returns the top few results
"""


class SearchEngine:
    def __init__(self, text_map: dict):
        self.text_map = text_map

    def calculate_distance(self, input_word):
        for word in self.text_map.keys():
            self.text_map[word]["distance"] = round(jaro_winkler(input_word, word), 3)

    def get_ranked_matches(self, input_word, max_num_matches: int = 7):
        self.calculate_distance(input_word)

        sorted_matches = sorted(
            self.text_map.items(), key=lambda item: item[1]["distance"], reverse=True
        )
        return dict(sorted_matches[:max_num_matches])
