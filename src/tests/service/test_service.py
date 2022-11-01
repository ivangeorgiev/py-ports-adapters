from unittest.mock import Mock

import pytest

from myapp.service import Command, CommandBus, HandlerMap
from myapp.service._command import CommandHandlerMap


class FakeCommand(Command):
    pass


class TestCommandHandlerMap:
    @pytest.fixture(name="command_handler_map")
    def given_command_handler_map(self):
        return CommandHandlerMap()

    @pytest.fixture(name="command_type")
    def given_command_type(self):
        return FakeCommand

    @pytest.fixture(name="handler")
    def given_handler(self):
        return Mock()

    @pytest.fixture(name="other_handler")
    def given_other_handler(self):
        return Mock()

    def test_can_put_new_handler(
        self, command_handler_map: CommandHandlerMap, command_type, handler: Mock
    ):
        command_handler_map.put(command_type, handler)
        assert command_handler_map._map[command_type] is handler

    def test_can_replace_handler(
        self,
        command_handler_map: CommandHandlerMap,
        command_type,
        handler: Mock,
        other_handler: Mock,
    ):
        command_handler_map.put(command_type, handler)
        command_handler_map.put(command_type, other_handler)
        assert command_handler_map._map[command_type] is other_handler

    def test_can_get_handler_by_type(
        self, command_handler_map: CommandHandlerMap, command_type, handler: Mock
    ):
        command_handler_map._map[command_type] = handler
        assert command_handler_map.get(command_type) is handler

    def test_can_set_handler_by_type_using_dictionary_access(
        self, command_handler_map: CommandHandlerMap, command_type, handler: Mock
    ):
        command_handler_map[command_type] = handler
        assert command_handler_map._map[command_type] is handler

    def test_can_get_handler_by_type_using_dictionary_access(
        self, command_handler_map: CommandHandlerMap, command_type, handler: Mock
    ):
        command_handler_map._map[command_type] = handler
        assert command_handler_map[command_type] is handler

    def test_get_handler_for_non_registered_type_raises_keyeror(
        self, command_handler_map: CommandHandlerMap, command_type
    ):
        with pytest.raises(KeyError):
            command_handler_map[command_type]


class TestCommandBus:
    @pytest.fixture(name="handler_map")
    def given_handler_map(self):
        return CommandHandlerMap()

    @pytest.fixture(name="command_bus")
    def given_command_bus(self, handler_map):
        return CommandBus(handler_map)

    @pytest.fixture(name="handler")
    def given_handler(self):
        return Mock()

    @pytest.fixture(name="command_type")
    def given_command_type(self):
        return FakeCommand

    @pytest.fixture(name="command")
    def given_command(self, command_type):
        return command_type()

    def test_handler_map_is_set_by_default(self, command_bus: CommandBus):
        command_bus = CommandBus()
        assert isinstance(command_bus._handler_map, HandlerMap)

    def test_handler_map_is_set_to_passed_instance(
        self, command_bus: CommandBus, handler_map
    ):
        assert command_bus._handler_map is handler_map

    def test_handler_map_property_returns_handler_map(
        self, command_bus: CommandBus, handler_map
    ):
        assert command_bus.handler_map is handler_map

    def test_call_the_bus_calls_registered_handler(
        self, command_bus: CommandBus, command, command_type, handler: Mock
    ):
        command_bus._handler_map[command_type] = handler
        result = command_bus(command)
        handler.assert_called_once_with(command)
        assert result is handler.return_value

    def test_handle_registered_command(
        self, command_bus: CommandBus, command, command_type, handler: Mock
    ):
        command_bus._handler_map[command_type] = handler
        result = command_bus.handle(command)
        handler.assert_called_once_with(command)
        assert result is handler.return_value

    def test_call_the_bus_raises_keyerror_unregistered_handler(
        self, command_bus: CommandBus, command
    ):
        with pytest.raises(KeyError):
            command_bus(command)
