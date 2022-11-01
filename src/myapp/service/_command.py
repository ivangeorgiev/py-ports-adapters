from abc import ABC, abstractmethod


class Failure(Exception):
    pass


class Command(ABC):
    """Abstract command"""
    pass


class Response(ABC):
    """Abstract response"""
    pass


class Handler(ABC):
    """Abstract command handler."""

    def __call__(self, command: Command) -> Response:
        return self._handle(command)

    @abstractmethod
    def _handle(self, command: Command) -> Response:
        """
        Abstract command handling.
        
        Override this method to specify handling algorithm.
        """
        pass
