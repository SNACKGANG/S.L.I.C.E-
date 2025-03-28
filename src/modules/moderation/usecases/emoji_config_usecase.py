from ..repositories.emoji_config_repository import EmojiConfigRepository


class EmojiManagerUseCase:
    @staticmethod
    async def get_configs_dict() -> dict:
        """
        Returns a dictionary mapping channel_id to EmojiConfig.
        """
        configs = await EmojiConfigRepository.get_all_configs()
        config_dict = {}
        for config in configs:
            values = config.emojis.split(",")
            config_dict[config.channel_id] = values
        return config_dict

    @staticmethod
    async def add_emoji_config(channel_id: int, emojis: list[str]) -> str:
        """
        Adds an emoji setting to the channel if it doesn't already exist.
        """
        existing = await EmojiConfigRepository.get_config_by_channel(channel_id)
        if existing:
            return "Channel already configured for emojis."
        await EmojiConfigRepository.add_config(channel_id, emojis)
        return "Emoji configuration added successfully!"

    @staticmethod
    async def remove_emoji_config(channel_id: int) -> str:
        """
        Removes the emoji setting for a channel.
        """
        existing = await EmojiConfigRepository.get_config_by_channel(channel_id)
        if not existing:
            return "No emoji configuration found for this channel."
        await EmojiConfigRepository.remove_config(channel_id)
        return "Emoji configuration removed successfully!"

    @staticmethod
    async def list_emoji_configs() -> list:
        """
        Returns a list of channel IDs that have emoji configuration.
        """
        configs = await EmojiConfigRepository.get_all_configs()
        return [config.channel_id for config in configs]
