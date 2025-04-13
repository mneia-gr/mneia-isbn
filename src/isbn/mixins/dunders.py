class DundersMixin:
    """
    Dunder methods for ISBN.
    """

    source: str

    def __str__(self) -> str:
        return self.source

    def __repr__(self) -> str:
        return f"<ISBN: {self.source}>"

    def __len__(self) -> int:
        return len(self.source)
