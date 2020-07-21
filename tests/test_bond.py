import pytest
from aioresponses import aioresponses, CallbackResult

from bond_api import Bond, Action, Direction


@pytest.fixture
def bond():
    return Bond("test-host", "test-token")


@pytest.mark.asyncio
async def test_version(bond: Bond):
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/sys/version",
            payload={"some": "version"}
        )
        actual = await bond.version()
        assert actual == {"some": "version"}


@pytest.mark.asyncio
async def test_devices(bond: Bond):
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/devices",
            payload={"_": "some-hash", "device-1": "some-device-1", "device-2": "some-device-2"}
        )
        actual = await bond.devices()
        assert actual == ["device-1", "device-2"]


@pytest.mark.asyncio
async def test_device(bond: Bond):
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/devices/device-1",
            payload={"some": "device details"}
        )
        actual = await bond.device("device-1")
        assert actual == {"some": "device details"}


@pytest.mark.asyncio
async def test_device_properties(bond: Bond):
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/devices/device-1/properties",
            payload={"some": "device properties"}
        )
        actual = await bond.device_properties("device-1")
        assert actual == {"some": "device properties"}


@pytest.mark.asyncio
async def test_device_state(bond: Bond):
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/devices/device-1/state",
            payload={"some": "device state"}
        )
        actual = await bond.device_state("device-1")
        assert actual == {"some": "device state"}


@pytest.mark.asyncio
async def test_turn_on(bond: Bond):
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
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 50}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/SetFlame",
            callback=callback
        )
        await bond.action("test-device-id", Action.set_flame(50))
