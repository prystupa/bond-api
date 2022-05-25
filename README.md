# bond-async
Asynchronous Python wrapper library over Bond Local API

Forked from https://github.com/prystupa/bond-api
Thanks @prystupa for the great work!

## Installation

From PyPi:

```bash
pip3 install bond-async
```

## Library Usage
```python3
import asyncio

from aiohttp import ClientResponseError, ClientConnectorError

from bond_async import Bond, Action


async def main():
    """Example of library usage."""
    
    bond = Bond("[your ip or hostname here]", "[your bond API token here]")

    try:
        print("Version:")
        print(await bond.version())

        print("Device IDs:")
        device_ids = await bond.devices()
        print(device_ids)

        print("Devices:")
        devices = await asyncio.gather(*[bond.device(device_id) for device_id in device_ids])
        print(devices)

        print("Devices Properties:")
        properties = await asyncio.gather(*[bond.device_properties(device_id) for device_id in device_ids])
        print(properties)

        print("Devices State:")
        state = await asyncio.gather(*[bond.device_state(device_id) for device_id in device_ids])
        print(state)

        print("Turn on fan!")
        await bond.action("[your fan device ID here]", Action.turn_on())

        print("Change fan speed!")
        await bond.action("[your fan device ID here]", Action.set_speed(2))

        print("Turn off fan!")
        await bond.action("[your fan device ID here]", Action.turn_off())
        
    except ClientResponseError as x:
        print("Client response error: ", x)
    except ClientConnectorError as x:
        print("Client connector error: ", x)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```
