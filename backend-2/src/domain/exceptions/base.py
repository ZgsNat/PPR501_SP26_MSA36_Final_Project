"""Base domain exceptions."""

class DomainException(Exception):
    """Base exception for all domain errors."""
    def __init__(self, message: str = None):
        self.message = message or self.__class__.__name__
        super().__init__(self.message)