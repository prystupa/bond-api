"""Bond Local API wrapper."""

from typing import List

import aiohttp

from .action import Action


class Bond:
    """Bond API."""

    def __init__(self, host: str, token: str):
        """Initialize Bond with provided host and token."""
        self._host = host
        self._headers = {'BOND-Token': token}

    async def version(self) -> dict:
        """Return the version of hub/bridge reported by API."""
        return await self._get("/v2/sys/version")

    async def devices(self) -> List[str]:
        """Return the list of available device IDs reported by API."""
        json = await self._get("/v2/devices")
        return [key for key in json if key != '_']

    async def device(self, device_id: str) -> dict:
        """Return main device metadata reported by API."""
        return await self._get(f"/v2/devices/{device_id}")

    async def device_properties(self, device_id: str) -> dict:
        """Return device properties reported by API."""
        return await self._get(f"/v2/devices/{device_id}/properties")

    async def device_state(self, device_id: str) -> dict:
        """Return current device state reported by API."""
        return await self._get(f"/v2/devices/{device_id}/state")

    async def action(self, device_id: str, action: Action) -> None:
        """Execute given action for a given device."""
        path = f"/v2/devices/{device_id}/actions/{action.name}"
        async with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.put(f"http://{self._host}{path}", json=action.argument) as response:
                response.raise_for_status()

    async def _get(self, path) -> dict:
        async with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.get(f"http://{self._host}{path}") as response:
                response.raise_for_status()
                return await response.json()
