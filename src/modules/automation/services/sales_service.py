from datetime import datetime, timezone
from typing import List

from loguru import logger

from ..models.sales_entity import Sale


class SalesService:
    """
    Service responsible for fetching and processing sales data.
    """

    def __init__(self, reservoir_service):
        self.reservoir_service = reservoir_service
        self.last_timestamp = None

    async def get_new_sales(self, collection_contracts: List[str]) -> List[dict]:
        """
        Fetches and filters new sales for a list of collection contracts.
        """
        logger.info(f"Fetching sales for contracts: {collection_contracts}")

        sales_data = await self.reservoir_service.get_latest_sales(collection_contracts)
        logger.info(f"Fetched {len(sales_data)} sales records")

        new_sales = []

        for sale in sales_data:
            sale_time = datetime.fromtimestamp(sale["timestamp"], timezone.utc)

            if self.last_timestamp is None:
                self.last_timestamp = sale_time
                continue

            if sale_time > self.last_timestamp:
                new_sales.append(sale)

        if new_sales:
            self.last_timestamp = datetime.fromtimestamp(
                new_sales[0]["timestamp"], timezone.utc
            )
            logger.info(f"Found {len(new_sales)} new sales")
        else:
            logger.info("No new sales found")

        return new_sales

    async def get_sales_with_metadata(self, sales: List[dict]) -> List[Sale]:
        """
        Adds metadata to sales and converts them to Sale objects.
        """
        logger.info(f"Fetching metadata for {len(sales)} sales")
        sales_with_metadata = []
        try:
            for sale in sales:
                sale_contract = sale["token"]["contract"]
                token_metadata = await self.reservoir_service.get_token_details(
                    sale_contract, sale["token"]["tokenId"]
                )

                collection_data_response = (
                    await self.reservoir_service.get_collection_data(sale_contract)
                )
                collection_data = collection_data_response["collections"][0]

                if token_metadata:
                    sales_with_metadata.append(
                        Sale(
                            token_id=sale["token"]["tokenId"],
                            contract=sale["token"]["contract"],
                            price_native=sale["price"]["amount"]["native"],
                            price_usd=sale["price"]["amount"]["usd"],
                            timestamp=datetime.fromtimestamp(
                                sale["timestamp"], timezone.utc
                            ),
                            seller=sale["from"],
                            buyer=sale["to"],
                            name=token_metadata.get("name"),
                            image=token_metadata.get("image"),
                            collection_data={
                                "floor_price": collection_data["floorAsk"]["price"][
                                    "amount"
                                ]["native"],
                                "volume_1day": collection_data["volume"]["1day"],
                                "volume_change": collection_data["volumeChange"][
                                    "1day"
                                ],
                            },
                        )
                    )
            logger.info(f"Metadata added to {len(sales_with_metadata)} sales")
            return sales_with_metadata
        except Exception as e:
            logger.error(f"Error adding metadata to sales: {e}")
