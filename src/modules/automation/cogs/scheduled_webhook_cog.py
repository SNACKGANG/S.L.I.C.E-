import discord

from discord.ext import commands
from discord import app_commands
from ..controllers.scheduled_webhook_controller import ScheduledWebhookController


class ScheduledWebhookCog(commands.Cog):
    def __init__(self, bot, webhook_controller: ScheduledWebhookController):
        self.bot = bot
        self.controller = webhook_controller

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.controller.start()

    @app_commands.command(name="webhook_add", description="Schedule a webhook message using a JSON file and a schedule time.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add_webhook(self, interaction: discord.Interaction, channel: discord.TextChannel, schedule_time: str,
                          file: discord.Attachment):
        """
        Expects the user to attach a JSON file (generated externally) and provide the schedule time.
        The schedule_time should be in the format "YYYY-MM-DD HH:MM", assuming UTC.
        """
        if not file.filename.endswith('.json'):
            await interaction.response.send_message("Please attach a valid JSON file.", ephemeral=True)
            return

        try:
            import json
            file_bytes = await file.read()
            json_data = json.loads(file_bytes)
        except json.JSONDecodeError:
            await interaction.response.send_message("Invalid JSON file.", ephemeral=True)
            return

        response = await self.controller.add_scheduled_webhook(interaction, channel, json_data, schedule_time)
        await interaction.response.send_message(response, ephemeral=True)
