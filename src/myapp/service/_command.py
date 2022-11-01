from abc import ABC, abstractmethod
from typing import Type


class Failure(Exception):
    """Base failure class"""


class Command(ABC):
    """Abstract command"""


class Response(ABC):
    """Abstract response"""


class Handler(ABC):
    """Abstract command handler."""

    def __call__(self, command: Command) -> Response:
        """Execute the handler algorithm and return the result. Same as handle() method"""
        return self._handle(command)

    def handle(self, command: Command) -> Response:
        """Execute the handler algorithm and return the result"""
        return self._handle(command)

    @abstractmethod
    def _handle(self, command: Command) -> Response:
        """Execute the handler algorithm implementation."""


class HandlerMap:
    def get(self, command_type: Type[Command]) -> Handler:
        return self._get(command_type)

    def put(self, command_type: Type[Command], handler: Handler):
        self._put(command_type, handler)

    def __setitem__(self, command_type: Type[Command], handler: Handler):
        self._put(command_type, handler)

    def __getitem__(self, command_type: Type[Command]) -> Handler:
        return self._get(command_type)

    @abstractmethod
    def _get(self, command_type: Type[Command]) -> Handler:
        """Get handler for a command type implementation"""

    @abstractmethod
    def _put(self, command_type: Type[Command], handler: Handler):
        """Put handler for a command type implementation"""


class CommandHandlerMap(HandlerMap):
    _map: dict

    def __init__(self):
        self._map = {}

    def _get(self, command_type: Type[Command]) -> Handler:
        return self._map[command_type]

    def _put(self, command_type: Type[Command], handler: Handler):
        self._map[command_type] = handler


class CommandBus(Handler):
    _handler_map: HandlerMap

    def __init__(self, handler_map: HandlerMap = None):
        self._handler_map = CommandHandlerMap() if handler_map is None else handler_map

    @property
    def handler_map(self) -> HandlerMap:
        return self._handler_map

    def _handle(self, command: Command) -> Response:
        """Handles the command and returns the response

        Could be overwritten to change the behavior.
        """
        handler = self._handler_map[type(command)]
        return handler(command)
