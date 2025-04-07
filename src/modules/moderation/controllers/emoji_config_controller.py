from discord import TextChannel
from ..usecases.emoji_config_usecase import EmojiManagerUseCase


class EmojiManagerController:
    def __init__(self):
        self.usecase = EmojiManagerUseCase()

    async def add_emoji_config(self, channel: TextChannel, emojis: list[str]) -> str:
        response = await self.usecase.add_emoji_config(channel.id, emojis)
        return response

    async def remove_emoji_config(self, channel: TextChannel) -> str:
        response = await self.usecase.remove_emoji_config(channel.id)
        return response

    async def list_emoji_configs(self) -> str:
        channel_ids = await self.usecase.list_emoji_configs()
        if channel_ids:
            mentions = [f"<#{channel_id}>" for channel_id in channel_ids]
            return "Channels with emoji configuration: " + ", ".join(mentions)
        return "No channels configured for emojis."
