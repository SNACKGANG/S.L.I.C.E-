from collections import defaultdict
from typing import List

from loguru import logger

from ..models.sales_entity import Sale
from ..services.sales_service import SalesService


class SalesFetchUseCase:
    """
    Use case responsible for fetching new sales for a list of collection contracts.
    """

    def __init__(self, sales_service: SalesService):
        self.sales_service = sales_service

    async def execute(self, tracked_contracts: List["TrackedContract"]) -> List[Sale]:
        """
        Fetches new sales for a list of tracked contracts and assigns channel_ids.
        """
        try:
            contracts = list({tc.contract_address for tc in tracked_contracts})
            raw_sales = await self.sales_service.get_new_sales(contracts)

            if not raw_sales:
                return None

            sales = await self.sales_service.get_sales_with_metadata(raw_sales)

            self._assign_channel_ids_to_sales(sales, tracked_contracts)

            return sales

        except Exception as e:
            logger.error(f"SalesFetch error: {e}")
            return []

    @staticmethod
    def _assign_channel_ids_to_sales(
        sales: List[Sale], tracked_contracts: List["TrackedContract"]
    ):
        """Assign channel IDs to sales based on contract address."""
        contract_to_channels = defaultdict(list)
        for tc in tracked_contracts:
            normalized_contract = tc.contract_address.strip().lower()
            contract_to_channels[normalized_contract].append(tc.channel_id)

        for sale in sales:
            normalized_sale_contract = sale.contract.strip().lower()
            sale.channel_ids = contract_to_channels[normalized_sale_contract]
