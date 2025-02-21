import asyncio
from typing import Dict, List, Optional

from loguru import logger

from .http_client import AioHttpClient


class ReservoirService:
    """
    Repository responsible for fetching sales data and token metadata from the Reservoir API.
    """

    def __init__(self, api_key: str, http_client: "HttpClient"):
        self.api_key = api_key
        self.http_client = http_client

    async def _make_request(self, url: str, params: dict) -> dict:
        """
        Helper method to make API requests with error handling and logging.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            data = await self.http_client.get(url, headers=headers, params=params)
            return data
        except Exception as e:
            logger.error(f"Error making request to {url}: {e}")
            return {}

    async def get_latest_sales(self, collection_contracts: List[str]) -> List[dict]:
        """
        Fetches sales data for a list of collection contracts.
        """
        url = "https://api.reservoir.tools/sales/v5"
        params = {
            "contract": collection_contracts,
            "limit": 20,
            "orderBy": "updated_at",
            "sortDirection": "desc",
        }

        data = await self._make_request(url, params)
        if "sales" in data:
            logger.success(f"Fetched {len(data['sales'])} sales.")
            return data["sales"]
        return []

    async def get_token_details(self, contract: str, token_id: str) -> Optional[dict]:
        """
        Fetches metadata for a specific token.
        """
        url = "https://api.reservoir.tools/tokens/v7"
        params = {"tokens": [f"{contract}:{token_id}"]}

        data = await self._make_request(url, params)
        if "tokens" in data and len(data["tokens"]) > 0:
            logger.success(f"Fetched metadata for token {contract}:{token_id}.")
            return data["tokens"][0]["token"]
        return None

    async def get_collection_data(self, collection_contract: str) -> dict:
        """
        Fetches data for a specific collection.
        """
        url = "https://api.reservoir.tools/collections/v7"
        params = {"contract": collection_contract}

        data = await self._make_request(url, params)
        return data

    async def get_all_holders(self, collection_address: str) -> Dict[str, int]:
        """
        Fetches all holders for a given collection.
        """
        url = "https://api.reservoir.tools/owners/v2"
        all_holders = {}
        offset = 0
        limit = 500

        while True:
            params = {
                "collection": collection_address,
                "limit": limit,
                "offset": offset,
            }

            data = await self._make_request(url, params)
            if "owners" in data:
                new_holders = 0
                for owner in data["owners"]:
                    wallet = owner.get("address", "").lower()
                    ownership = owner.get("ownership", {})
                    raw_count = ownership.get("tokenCount")
                    try:
                        count = int(raw_count) if raw_count is not None else 0
                    except Exception as e:
                        logger.error(f"Error converting tokenCount: {e}")
                        count = 0

                    if wallet and count > 0:
                        all_holders[wallet] = count
                        new_holders += 1

                if len(data["owners"]) < limit:
                    logger.info(
                        f"End of data reached for collection {collection_address}."
                    )
                    break

                offset += limit
                logger.success(
                    f"Processed batch | New holders: {new_holders} | Total: {len(all_holders)}"
                )
            else:
                logger.error(f"Error fetching owners data for {collection_address}.")
                break

            await asyncio.sleep(5)

        return all_holders

    async def get_nft_ownership(
        self, wallet_address: str, collection_address: str
    ) -> Optional[int]:
        """
        Verifies the ownership of NFTs for a given wallet address and collection.
        """
        url = f"https://api.reservoir.tools/users/{wallet_address}/tokens/v10"
        params = {"collection": collection_address}

        data = await self._make_request(url, params)
        if "tokens" in data and len(data["tokens"]) > 0:
            logger.success(
                f"Wallet {wallet_address} owns {len(data['tokens'])} tokens in collection {collection_address}."
            )
            return len(data["tokens"])
        logger.warning(
            f"Wallet {wallet_address} does not own any tokens in collection {collection_address}."
        )
        return 0
