import discord

from discord.ext import commands
from discord import app_commands
from ..controllers.emoji_config_controller import EmojiManagerController


class EmojiManagerCog(commands.Cog):
    def __init__(self, bot: "discord.Bot"):
        self.bot = bot
        self.controller = EmojiManagerController()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Emoji Manager Cog Loaded")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        configs = await self.controller.usecase.get_configs_dict()
        if message.channel.id in configs:
            emojis = configs[message.channel.id]
            for emoji in emojis:
                try:
                    if emoji.isdigit():
                        emoji_obj = discord.utils.get(self.bot.emojis, id=int(emoji))
                        if emoji_obj:
                            await message.add_reaction(emoji_obj)
                        else:
                            await message.add_reaction(emoji)
                    else:
                        await message.add_reaction(emoji)
                except Exception as e:
                    print(f"Error reacting with emoji: {e}")

    @app_commands.command(name="emoji_config_add", description="Add emoji configuration for a channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add_emoji_config(self, interaction: discord.Interaction, channel: discord.TextChannel, emoji1: str, emoji2: str = None, emoji3: str = None, emoji4: str = None):
        emojis = [emoji for emoji in (emoji1, emoji2, emoji3, emoji4) if emoji is not None]
        response = await self.controller.add_emoji_config(channel, emojis)
        await interaction.response.send_message(response, ephemeral=True)

    @app_commands.command(name="emoji_config_remove", description="Remove emoji configuration from a channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def remove_emoji_config(self, interaction: discord.Interaction, channel: discord.TextChannel):
        response = await self.controller.remove_emoji_config(channel)
        await interaction.response.send_message(response, ephemeral=True)

    @app_commands.command(name="emoji_config_list", description="List channels with emoji configuration")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def list_emoji_config(self, interaction: discord.Interaction):
        response = await self.controller.list_emoji_configs()
        await interaction.response.send_message(response, ephemeral=True)
