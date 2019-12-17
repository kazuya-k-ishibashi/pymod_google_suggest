

class Keyword:

    def __init__(self, original: str, additional: str = None):
        self.original = original
        self.additional = additional


    def to_str(self) -> str:
        return self.original if self.additional == None else ' '.join([ self.original, self.additional ])


