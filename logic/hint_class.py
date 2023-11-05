from .text import Text


class Hint:
    def __init__(self) -> None:
        self.type: str = "None"
        self.text: Text = Text()

    def __str__(self) -> str:
        return f"{self.text}"
