from typing import List

from loguru import logger

from src.shared.services.discord_service import DiscordService

from ..models.sales_entity import Sale
from ..services.sales_notification_service import SalesNotificationService


class SalesSendUseCase:
    """
    Use case responsible for sending sales data to Discord.
    """

    def __init__(
        self,
        discord_service: DiscordService,
        sales_notification_service: SalesNotificationService,
    ):
        self.discord_service = discord_service
        self.sales_notification_service = sales_notification_service

    async def execute(self, sales: List[Sale]):
        """
        Sends sales to the respective channels on Discord.
        """
        logger.info("Starting execution of SalesSendUseCase.")
        logger.info(f"Received {len(sales)} sales to process.")

        try:
            for sale in reversed(sales):
                logger.info(f"Creating embed for sale: {sale.contract}")
                embed = await self.sales_notification_service.format_sale_embed(sale)
                for channel_id in sale.channel_ids:
                    try:
                        if channel_id:
                            await self.discord_service.send_message(
                                channel_id, embed=embed
                            )
                            logger.info(
                                f"Successfully sent sale {sale.contract} to channel ID: {channel_id}"
                            )
                        else:
                            logger.warning(f"Channel id not being processed")
                    except Exception as e:
                        logger.error(
                            f"Error processing sale {sale.contract}: {e}", exc_info=True
                        )

            logger.success("Finished execution of SalesSendUseCase.")
        except Exception as e:
            logger.error(f"Error in execute: {e}", exc_info=True)
