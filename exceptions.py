class HCError(Exception):
    """Vague error format"""

    def __init__(self, message="An error occoured :D", *args: object) -> None:
        super().__init__(*args)
        self.message = message

    def __str__(self) -> str:
        return self.message