from discord import TextChannel, Interaction
from datetime import datetime
from ..usecases.scheduled_webhook_usecase import ScheduledWebhookUseCase


class ScheduledWebhookController:
    def __init__(self, webhook_usecase: ScheduledWebhookUseCase):
        self.webhook_usecase = webhook_usecase

    async def add_scheduled_webhook(self, interaction: Interaction, channel: TextChannel, json_data: dict, schedule_time_str: str) -> str:
        """
        Adds a scheduled webhook to the channel based on the provided JSON and date/time string.
        Date/time format: "YYYY-MM-DD HH:MM" in UTC, for example.
        """
        try:
            schedule_time = datetime.strptime(schedule_time_str, "%Y-%m-%d %H:%M")
            schedule_time = schedule_time.astimezone(datetime.now().astimezone().tzinfo)
            await self.webhook_usecase.schedule_webhook(channel.id, json_data, schedule_time)
            return "Webhook scheduled successfully."
        except Exception as e:
            print(f"Error scheduling webhook: {e}")
            return "Failed to schedule webhook. Please try again."

    def start(self):
        self.webhook_usecase.start()
