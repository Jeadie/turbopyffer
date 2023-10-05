class TurboPufferError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message=message)

    def __str__(self) -> str:
        return f"TurboPufferError error: {self.message}"
