"""Unit tests for Bond API wrapper."""

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses, CallbackResult

from bond_api import Bond, Action, Direction


@pytest.fixture(name="bond")
def bond_fixture():
    """Creates Bond fixture."""
    return Bond("test-host", "test-token")


@pytest.mark.asyncio
async def test_external_session():
    """Tests using external session."""
    async with ClientSession() as session:
        bond: Bond = Bond("test-host", "test-token", session=session)
        with aioresponses() as response:
            response.get(
                "http://test-host/v2/sys/version",
                payload={"some": "version"}
            )
            actual = await bond.version()
            assert actual == {"some": "version"}


@pytest.mark.asyncio
async def test_version(bond: Bond):
    """Tests version API."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/sys/version",
            payload={"some": "version"}
        )
        actual = await bond.version()
        assert actual == {"some": "version"}


@pytest.mark.asyncio
async def test_devices(bond: Bond):
    """Tests API to get a list of device IDs."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/devices",
            payload={"_": "some-hash", "device-1": "some-device-1", "device-2": "some-device-2"}
        )
        actual = await bond.devices()
        assert actual == ["device-1", "device-2"]


@pytest.mark.asyncio
async def test_device(bond: Bond):
    """Tests API to get device details."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/devices/device-1",
            payload={"some": "device details"}
        )
        actual = await bond.device("device-1")
        assert actual == {"some": "device details"}


@pytest.mark.asyncio
async def test_device_properties(bond: Bond):
    """Tests API to get device properties."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/devices/device-1/properties",
            payload={"some": "device properties"}
        )
        actual = await bond.device_properties("device-1")
        assert actual == {"some": "device properties"}


@pytest.mark.asyncio
async def test_device_state(bond: Bond):
    """Tests API to get device state."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/devices/device-1/state",
            payload={"some": "device state"}
        )
        actual = await bond.device_state("device-1")
        assert actual == {"some": "device state"}


@pytest.mark.asyncio
async def test_turn_on(bond: Bond):
    """Tests turn_on action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/TurnOn",
            callback=callback
        )
        await bond.action("test-device-id", Action.turn_on())


@pytest.mark.asyncio
async def test_turn_off(bond: Bond):
    """Tests turn_off action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/TurnOff",
            callback=callback
        )
        await bond.action("test-device-id", Action.turn_off())


@pytest.mark.asyncio
async def test_open(bond: Bond):
    """Tests open action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/Open",
            callback=callback
        )
        await bond.action("test-device-id", Action.open())


@pytest.mark.asyncio
async def test_close(bond: Bond):
    """Tests close action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/Close",
            callback=callback
        )
        await bond.action("test-device-id", Action.close())


@pytest.mark.asyncio
async def test_hold(bond: Bond):
    """Tests hold action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/Hold",
            callback=callback
        )
        await bond.action("test-device-id", Action.hold())


@pytest.mark.asyncio
async def test_set_speed(bond: Bond):
    """Tests set_speed action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 2}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/SetSpeed",
            callback=callback
        )
        await bond.action("test-device-id", Action.set_speed(2))


@pytest.mark.asyncio
async def test_turn_light_on(bond: Bond):
    """Tests turn_light_on action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/TurnLightOn",
            callback=callback
        )
        await bond.action("test-device-id", Action.turn_light_on())


@pytest.mark.asyncio
async def test_turn_light_off(bond: Bond):
    """Tests turn_light_off action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/TurnLightOff",
            callback=callback
        )
        await bond.action("test-device-id", Action.turn_light_off())


@pytest.mark.asyncio
async def test_set_direction_forward(bond: Bond):
    """Tests set_direction action delegates to API with correct value for forward."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 1}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/SetDirection",
            callback=callback
        )
        await bond.action("test-device-id", Action.set_direction(Direction.FORWARD))


@pytest.mark.asyncio
async def test_set_direction_reverse(bond: Bond):
    """Tests set_direction action delegates to API with correct value for reverse."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": -1}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/SetDirection",
            callback=callback
        )
        await bond.action("test-device-id", Action.set_direction(Direction.REVERSE))


@pytest.mark.asyncio
async def test_set_flame(bond: Bond):
    """Tests set_flame action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 50}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/SetFlame",
            callback=callback
        )
        await bond.action("test-device-id", Action.set_flame(50))
