from typing import List, Tuple

from loguru import logger

from src.modules.automation.models.sales_nft_config_model import SalesNftConfig


class SalesConfigRepository:
    """
    Repository class for managing NFT sales configurations in the database.
    """

    @staticmethod
    async def add_config(guild_id: int, channel_id: int, contract_address: str):
        """
        Adds a new NFT sales configuration for a given guild.
        """
        try:
            config = await SalesNftConfig.create(
                guild_id=guild_id,
                channel_id=channel_id,
                contract_address=contract_address,
            )
            logger.success(f"Added new sales configuration for guild {guild_id}.")
            return config
        except Exception as e:
            logger.error(f"Error adding sales configuration for guild {guild_id}: {e}")
            raise

    @staticmethod
    async def delete_by_id(config_id: int) -> bool:
        """
        Removes an NFT sales configuration.
        """
        try:
            deleted_count = await SalesNftConfig.filter(id=config_id).delete()

            if deleted_count > 0:
                logger.success(f"Deleted sales configuration {config_id}.")
                return True
            logger.warning(f"Failed to delete sales configuration {config_id}.")
            return False
        except Exception as e:
            logger.error(f"Error removing sales configuration for {config_id}: {e}")
            return False

    @staticmethod
    async def get_configs_by_guild(guild_id: int):
        """
        Retrieves all NFT sales configurations for a given guild.
        """
        try:
            configs = await SalesNftConfig.filter(guild_id=guild_id).all()
            logger.info(
                f"Retrieved {len(configs)} sales configurations for guild {guild_id}."
            )
            return configs
        except Exception as e:
            logger.error(
                f"Error retrieving sales configurations for guild {guild_id}: {e}"
            )
            return []

    @staticmethod
    async def get_active_configs() -> List[Tuple[int, str]]:
        """
        Returns a list of tuples containing (channel_id, contract_address)
        for all active sales configurations.
        """
        try:
            configs = await SalesNftConfig.filter(is_active=True).values_list(
                "channel_id", "contract_address"
            )
            logger.info(f"Retrieved {len(configs)} active sales configurations.")
            return configs
        except Exception as e:
            logger.error(f"Error retrieving active sales configurations: {e}")
            return []
