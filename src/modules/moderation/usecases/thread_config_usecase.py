from ..repositories.thread_config_repository import ThreadConfigRepository


class ThreadManagerUseCase:
    @staticmethod
    async def get_config_dict():
        """
        Returns a dictionary mapping channel IDs to their ThreadConfig objects.
        """
        configs = await ThreadConfigRepository.get_all_configs()
        return {config.channel_id: config for config in configs}

    @staticmethod
    async def add_thread_config(channel_id: int, name: str, auto_archive_duration: int, reason: str = None) -> str:
        """
        Adds a new thread configuration if none exists for the channel.
        """
        existing = await ThreadConfigRepository.get_config_by_channel(channel_id)
        if existing:
            return "Channel already configured for auto-thread."
        await ThreadConfigRepository.add_config(channel_id, name, auto_archive_duration, reason)
        return "Thread configuration added successfully!"

    @staticmethod
    async def remove_thread_config(channel_id: int) -> str:
        """
        Removes the thread configuration for the given channel.
        """
        existing = await ThreadConfigRepository.get_config_by_channel(channel_id)
        if not existing:
            return "No thread configuration found for this channel."
        await ThreadConfigRepository.remove_config(channel_id)
        return "Thread configuration removed successfully!"

    @staticmethod
    async def list_thread_configs() -> list:
        """
        Returns a list of channel IDs that have auto-thread configurations.
        """
        configs = await ThreadConfigRepository.get_all_configs()
        return [config.channel_id for config in configs]