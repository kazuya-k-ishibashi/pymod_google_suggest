from typing import List
from .keyword import Keyword


class Suggestion:

    def __init__(self, keyword: Keyword, words: List[str]):
        self.keyword = keyword
        self.words = words


