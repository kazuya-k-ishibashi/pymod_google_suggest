from typing import List
from .keyword import Keyword


class Suggestion:

    def __init__(self, keyword: Keyword, recurse_level, words: List[str]):
        self.keyword = keyword
        self.recurse_level = recurse_level
        self.words = words


