from loguru import logger
from tortoise.exceptions import IntegrityError

from src.modules.administration.models.guild_config_model import GuildConfig


class GuildConfigRepository:
    """
    Repository for handling guild configuration database operations.
    """

    @staticmethod
    async def add_guild(guild_id: int, guild_name: str):
        """
        Adds a guild to the bank if it doesn't exist.
        """
        try:
            existing_guild = await GuildConfig.get_or_none(guild_id=guild_id)
            if not existing_guild:
                await GuildConfig.create(
                    guild_id=guild_id,
                    guild_name=guild_name,
                )
            logger.success(f"Guild {guild_name} (ID: {guild_id}) added successfully.")
        except IntegrityError as e:
            logger.error(f"Integrity error when adding guild {guild_id}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error when adding guild {guild_id}: {e}")
