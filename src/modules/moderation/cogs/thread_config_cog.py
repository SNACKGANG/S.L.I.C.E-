import discord

from discord.app_commands import Choice
from discord.ext import commands
from discord import app_commands
from ..controllers.thread_config_controller import ThreadManagerController


class ThreadManagerCog(commands.Cog):
    def __init__(self, bot: "discord.Bot"):
        self.bot = bot
        self.controller = ThreadManagerController()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Thread Manager Cog Loaded")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            configs = await self.controller.usecase.get_config_dict()
            if message.channel.id in configs:
                config = configs[message.channel.id]
                await message.create_thread(
                    name=config.name,
                    auto_archive_duration=config.auto_archive_duration,
                    reason=config.reason
                )
        except Exception as e:
            print(e)

    @app_commands.command(name="thread_config_add", description="Add auto-thread configuration to a channel")
    @app_commands.choices(auto_archive_duration=[
        Choice(name="7 Days", value=10080),
        Choice(name="3 Days", value=4320),
        Choice(name="1 Day", value=1440),
    ])
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add_thread_config(self, interaction: discord.Interaction, channel: discord.TextChannel, name: str,
                                auto_archive_duration: app_commands.Choice[int], reason: str = None):
        try:
            response = await self.controller.add_thread_config(channel, name, auto_archive_duration.value, reason)
            await interaction.response.send_message(response, ephemeral=True)
        except Exception as e:
            print(e)

    @app_commands.command(name="thread_config_remove", description="Remove auto-thread configuration from a channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def remove_thread_config(self, interaction: discord.Interaction, channel: discord.TextChannel):
        response = await self.controller.remove_thread_config(channel)
        await interaction.response.send_message(response, ephemeral=True)

    @app_commands.command(name="thread_config_list", description="List channels with auto-thread configuration")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def list_thread_config(self, interaction: discord.Interaction):
        response = await self.controller.list_thread_configs()
        await interaction.response.send_message(response, ephemeral=True)
