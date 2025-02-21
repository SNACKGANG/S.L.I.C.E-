from dataclasses import dataclass
from typing import List, Tuple

from loguru import logger

from ..usecases.sales_fetch_usecase import SalesFetchUseCase
from ..usecases.sales_send_usecase import SalesSendUseCase


@dataclass
class TrackedContract:
    channel_id: int
    contract_address: str


class SalesController:
    """
    Controller responsible for handling sales-related operations.
    """

    def __init__(
        self,
        fetch_sales_usecase: SalesFetchUseCase,
        send_sales_use_case: SalesSendUseCase,
    ):
        self.fetch_sales_usecase = fetch_sales_usecase
        self.send_sales_use_case = send_sales_use_case

    async def handle_sale(self, active_sales: List[Tuple[int, str]]):
        """
        Processes active sales and sends notifications.
        """
        try:
            tracked_contracts = [
                TrackedContract(channel_id=channel_id, contract_address=contract)
                for channel_id, contract in active_sales
            ]

            sales = await self.fetch_sales_usecase.execute(tracked_contracts)

            if sales:
                await self.send_sales_use_case.execute(sales)
                logger.success("Sales dispatched successfully")
        except Exception as e:
            logger.error(f"Controller error: {e}")
            raise
