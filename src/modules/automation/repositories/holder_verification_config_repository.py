from loguru import logger

from src.modules.automation.models.holder_role_threshold_model import \
    HolderRoleThresholdModel
from src.modules.automation.models.holder_verification_config_model import \
    HolderVerificationConfigModel


class HolderConfigRepository:
    """
    Repository responsible for handling holder verification configurations.
    """

    @staticmethod
    async def get_role_by_nft_amount(nft_amount: int):
        """
        Fetch the corresponding role for a given NFT amount.
        """
        try:
            config = await HolderVerificationConfigModel.first()
            if not config:
                return None

            role_threshold = (
                await HolderRoleThresholdModel.filter(
                    config=config, min_nft__lte=nft_amount
                )
                .order_by("-min_nft")
                .first()
            )

            if role_threshold and (
                role_threshold.max_nft is None or nft_amount <= role_threshold.max_nft
            ):
                return role_threshold.role_id

            return None
        except Exception as e:
            logger.error(f"Error retrieving role for NFT amount {nft_amount}: {e}")
            return None

    @staticmethod
    async def get_collection_address_by_guild_id(guild_id: str):
        """
        Fetch the collection address for a specific guild.
        """
        try:
            config = await HolderVerificationConfigModel.get_or_none(guild_id=guild_id)

            if config:
                return config.collection_address
            else:
                return None
        except Exception as e:
            logger.error(f"Error fetching collection address for guild {guild_id}: {e}")
            return None

    @staticmethod
    async def save_config(
        guild_id: str,
        collection_address: str,
        roles_data: list[tuple[int, int | None, int]],
    ):
        """
        Save holder verification configuration for a specific guild and collection.
        """
        try:
            existing_config = await HolderVerificationConfigModel.get_or_none(
                guild_id=guild_id, collection_address=collection_address
            )

            if existing_config:
                await HolderRoleThresholdModel.filter(config=existing_config).delete()
                logger.info(
                    f"Old thresholds deleted for collection {collection_address} in guild {guild_id}"
                )
            else:
                existing_config = await HolderVerificationConfigModel.create(
                    guild_id=guild_id, collection_address=collection_address
                )

            for min_nft, max_nft, role_id in roles_data:
                await HolderRoleThresholdModel.create(
                    config=existing_config,
                    min_nft=min_nft,
                    max_nft=max_nft,
                    role_id=role_id,
                )

            logger.success(
                f"Holder verification config saved for collection {collection_address} in guild {guild_id}"
            )
            return True
        except Exception as e:
            logger.error(
                f"Error saving holder verification config for guild {guild_id} and collection {collection_address}: {e}"
            )
            return False
