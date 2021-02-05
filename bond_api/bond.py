"""Bond Local API wrapper."""

import asyncio
import json
import time
from asyncio import transports
from typing import Any, Callable, List, Optional

from aiohttp import ClientSession, ClientTimeout

from .action import Action

BPUP_INIT_PUSH_MESSAGE = b"\n"
BPUP_PORT = 30007
BPUP_ALIVE_TIMEOUT = 70


class Bond:
    """Bond API."""

    def __init__(
        self,
        host: str,
        token: str,
        *,
        session: Optional[ClientSession] = None,
        timeout: Optional[ClientTimeout] = None,
    ):
        """Initialize Bond with provided host and token."""
        self._host = host
        self._api_kwargs = {"headers": {"BOND-Token": token}}
        if timeout:
            self._api_kwargs["timeout"] = timeout
        self._session = session

    async def version(self) -> dict:
        """Return the version of hub/bridge reported by API."""
        return await self.__get("/v2/sys/version")

    async def bridge(self) -> dict:
        """Return the name and location of the bridge."""
        return await self.__get("/v2/bridge")

    async def devices(self) -> List[str]:
        """Return the list of available device IDs reported by API."""
        json = await self.__get("/v2/devices")
        return [key for key in json if key != "_"]

    async def device(self, device_id: str) -> dict:
        """Return main device metadata reported by API."""
        return await self.__get(f"/v2/devices/{device_id}")

    async def device_properties(self, device_id: str) -> dict:
        """Return device properties reported by API."""
        return await self.__get(f"/v2/devices/{device_id}/properties")

    async def device_state(self, device_id: str) -> dict:
        """Return current device state reported by API."""
        return await self.__get(f"/v2/devices/{device_id}/state")

    async def action(self, device_id: str, action: Action) -> None:
        """Execute given action for a given device."""
        path = f"/v2/devices/{device_id}/actions/{action.name}"

        async def put(session: ClientSession) -> None:
            async with session.put(
                f"http://{self._host}{path}", **self._api_kwargs, json=action.argument
            ) as response:
                response.raise_for_status()

        await self.__call(put)

    async def __get(self, path) -> dict:
        async def get(session: ClientSession) -> dict:
            async with session.get(
                f"http://{self._host}{path}", **self._api_kwargs
            ) as response:
                response.raise_for_status()
                return await response.json()

        return await self.__call(get)

    async def __call(self, handler: Callable[[ClientSession], Any]):
        if not self._session:
            async with ClientSession() as request_session:
                return await handler(request_session)
        else:
            return await handler(self._session)


class BPUPSubscriptions:
    """Store BPUP subscriptions."""

    def __init__(self):
        """Init and store callbacks."""
        self._callbacks = {}
        self.last_message_time = 0

    @property
    def alive(self):
        return (time.time() - self.last_message_time) < BPUP_ALIVE_TIMEOUT

    def subscribe(self, device_id, callback):
        """Subscribe to BPUP updates."""
        self._callbacks.setdefault(device_id, []).append(callback)

    def unsubscribe(self, device_id, callback):
        """Unsubscribe from BPUP updates."""
        self._callbacks[device_id].remove(callback)

    def notify(self, json_msg):
        """Notify subscribers of an update."""
        self.last_message_time = time.time()

        if json_msg.get("s") != 200:
            return

        topic = json_msg["t"].split("/")
        device_id = topic[1]

        for callback in self._callbacks.get(device_id, []):
            callback(json_msg["b"])


class BPUProtocol:
    """Implements BPU Protocol."""

    def __init__(self, loop, bpup_subscriptions):
        """Create BPU Protocol."""
        self.loop = loop
        self.bpup_subscriptions = bpup_subscriptions
        self.transport = None
        self.keep_alive = None

    def connection_made(self, transport):
        """Connect or reconnect to the device."""
        self.transport = transport
        if self.keep_alive:
            self.keep_alive.cancel()
            self.keep_alive = None
        self.send_keep_alive()

    def send_keep_alive(self):
        """Send a keep alive every 60 seconds per the protocol."""
        self.transport.sendto(BPUP_INIT_PUSH_MESSAGE)
        self.keep_alive = self.loop.call_later(60, self.send_keep_alive)

    def datagram_received(self, data, addr):
        """Process incoming state changes."""
        self.bpup_subscriptions.notify(json.loads(data.decode()[:-1]))

    def error_received(self, exc):
        """Ignore errors."""
        return

    def connection_lost(self, exc):
        """Ignore connection lost."""
        return

    def stop(self):
        """Stop the client."""
        if self.transport:
            self.transport.close()


async def start_bpup(host_ip_addr, bpup_subscriptions):
    """Create the socket and protocol."""
    loop = asyncio.get_event_loop()

    _, protocol = await loop.create_datagram_endpoint(
        lambda: BPUProtocol(loop, bpup_subscriptions),
        remote_addr=(host_ip_addr, BPUP_PORT),
    )
    return protocol.stop
