from discord import TextChannel, Interaction
from ..usecases.thread_config_usecase import ThreadManagerUseCase


class ThreadManagerController:
    def __init__(self):
        self.usecase = ThreadManagerUseCase()

    async def add_thread_config(self, channel: TextChannel, name: str,
                                auto_archive_duration: int, reason: str = None) -> str:
        response = await self.usecase.add_thread_config(channel.id, name, auto_archive_duration, reason)
        return response

    async def remove_thread_config(self, channel: TextChannel) -> str:
        response = await self.usecase.remove_thread_config(channel.id)
        return response

    async def list_thread_configs(self, ) -> str:
        configs = await self.usecase.list_thread_configs()
        if configs:
            channel_mentions = [f"<#{channel_id}>" for channel_id in configs]
            return "Channels with auto-thread configuration: " + ", ".join(channel_mentions)
        return "No channel is configured for auto-thread."
