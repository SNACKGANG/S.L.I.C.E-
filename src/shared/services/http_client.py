from abc import ABC, abstractmethod

import aiohttp


class HttpClient(ABC):
    """
    Abstract base class for HTTP clients to ensure flexibility.
    Allows swapping out the HTTP client implementation.
    """

    @abstractmethod
    async def get(self, url: str, headers: dict, params: dict) -> dict:
        pass

    @abstractmethod
    async def post(self, url: str, headers: dict, data: dict) -> dict:
        pass


class AioHttpClient(HttpClient):
    """
    A concrete implementation of HttpClient using aiohttp.
    """

    async def get(self, url: str, headers: dict, params: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                response.raise_for_status()
                return await response.json()

    async def post(self, url: str, headers: dict, data: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.json()
