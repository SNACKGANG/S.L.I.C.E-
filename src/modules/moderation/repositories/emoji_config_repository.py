from ..models.emoji_config_model import EmojiConfig


class EmojiConfigRepository:
    @staticmethod
    async def get_all_configs():
        """
        Returns all emoji settings.
        """
        return await EmojiConfig.all()

    @staticmethod
    async def get_config_by_channel(channel_id: int):
        """
        Returns the emoji setting for a specific channel.
        """
        return await EmojiConfig.get_or_none(channel_id=channel_id)

    @staticmethod
    async def add_config(channel_id: int, emojis: list[str]):
        """
        Adds a new emoji configuration for a channel.

        Converts the emoji list to a comma-separated string.
        """
        emojis_str = ",".join(emojis)
        return await EmojiConfig.create(channel_id=channel_id, emojis=emojis_str)

    @staticmethod
    async def remove_config(channel_id: int):
        """
        Removes the emoji setting for a specific channel.
        """
        config = await EmojiConfig.get_or_none(channel_id=channel_id)
        if config:
            await config.delete()
        return config
    