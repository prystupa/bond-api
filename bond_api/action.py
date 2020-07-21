"""Typed helpers for executable actions for Bond Local API."""

from enum import IntEnum
from typing import Any


class Direction(IntEnum):
    """Direction enumeration for supported fan directions."""
    FORWARD = 1
    REVERSE = -1


class Action:
    """Namespace for Bond API action helpers and constants."""

    # Power (generic devices, fans, fireplaces)
    TURN_ON = "TurnOn"
    TURN_OFF = "TurnOff"
    # Covers
    OPEN = "Open"
    CLOSE = "Close"
    HOLD = "Hold"
    # Fans
    SET_SPEED = "SetSpeed"
    SET_DIRECTION = "SetDirection"
    TURN_LIGHT_ON = "TurnLightOn"
    TURN_LIGHT_OFF = "TurnLightOff"
    # Fireplaces
    SET_FLAME = "SetFlame"

    def __init__(self, name: str, argument: Any = None):
        self._name = name
        self._argument = {} if not argument else {"argument": argument}

    @staticmethod
    def turn_on() -> 'Action':
        """Turn device on (usually power)."""
        return Action(Action.TURN_ON)

    @staticmethod
    def turn_off() -> 'Action':
        """Turn device off (usually power)."""
        return Action(Action.TURN_OFF)

    @staticmethod
    def open() -> 'Action':
        """Open cover."""
        return Action(Action.OPEN)

    @staticmethod
    def close() -> 'Action':
        """Close cover."""
        return Action(Action.CLOSE)

    @staticmethod
    def hold() -> 'Action':
        """Hold cover."""
        return Action(Action.HOLD)

    @staticmethod
    def set_speed(speed: int) -> 'Action':
        """Sets fan rotation to a provided speed."""
        return Action(Action.SET_SPEED, speed)

    @staticmethod
    def set_direction(direction: Direction) -> 'Action':
        """Sets fan rotation direction."""
        return Action(Action.SET_DIRECTION, direction.value)

    @staticmethod
    def turn_light_on() -> 'Action':
        """Turns on the fan light."""
        return Action(Action.TURN_LIGHT_ON)

    @staticmethod
    def turn_light_off() -> 'Action':
        """Turns off the fan light."""
        return Action(Action.TURN_LIGHT_OFF)

    @staticmethod
    def set_flame(flame: int) -> 'Action':
        """Sets the flame to given intensity in percent."""
        return Action(Action.SET_FLAME, flame)

    @property
    def name(self) -> str:
        """Return name of this action."""
        return self._name

    @property
    def argument(self) -> dict:
        """Return optional argument for this action."""
        return self._argument
