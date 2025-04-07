from ..models.thread_config_model import ThreadConfig


class ThreadConfigRepository:
    @staticmethod
    async def get_all_configs():
        """
        Returns a list of all thread configurations.
        """
        return await ThreadConfig.all()

    @staticmethod
    async def get_config_by_channel(channel_id: int):
        """
        Retrieves a thread configuration by its channel ID.
        """
        return await ThreadConfig.get_or_none(channel_id=channel_id)

    @staticmethod
    async def add_config(channel_id: int, name: str, auto_archive_duration: int, reason: str = None):
        """
        Inserts a new configuration for auto-thread creation.
        """
        return await ThreadConfig.create(
            channel_id=channel_id,
            name=name,
            auto_archive_duration=auto_archive_duration,
            reason=reason
        )

    @staticmethod
    async def remove_config(channel_id: int):
        """
        Removes the thread configuration for the given channel.
        """
        config = await ThreadConfig.get_or_none(channel_id=channel_id)
        if config:
            await config.delete()
        return config
