import asyncio
import aiohttp

from datetime import datetime, timezone
from ..repositories.scheduled_webhook_repository import ScheduledWebhookRepository


class ScheduledWebhookUseCase:
    def __init__(self, discord_service: "Discord_Service", check_interval: int = 60):
        """
        check_interval: Interval in seconds to check for pending webhooks
        """
        self.check_interval = check_interval
        self.running = False
        self.discord_service = discord_service

    @staticmethod
    async def schedule_webhook(channel_id: int, json_data: dict, schedule_time: datetime):
        return await ScheduledWebhookRepository.add_webhook(channel_id, json_data, schedule_time)

    async def process_due_webhooks(self):
        """
        Checks periodically (every check_interval) and fires webhooks whose time has passed.
        """
        while True:
            now = datetime.now(timezone.utc)
            due_webhooks = await ScheduledWebhookRepository.get_due_webhooks(now)

            if due_webhooks:
                for webhook in due_webhooks:
                    webhook_url = await self.discord_service.get_webhook_url(webhook.channel_id)

                    async with aiohttp.ClientSession() as session:
                        try:
                            async with session.post(webhook_url, json=webhook.json_data) as response:
                                if response.status not in [200, 204]:
                                    print(f"Webhook {webhook.id} failed to execute: {response.status}")

                                else:
                                    print(f"Webhook {webhook.id} executed successfully.")
                                    await ScheduledWebhookRepository.mark_as_sent(webhook.id)
                        except Exception as e:
                            print(f"Error executing webhook {webhook.id}: {e}")

            await asyncio.sleep(self.check_interval)

    def start(self):
        """
        Starts the webhook verification loop.
        """
        if not self.running:
            self.running = True
            asyncio.create_task(self.process_due_webhooks())
