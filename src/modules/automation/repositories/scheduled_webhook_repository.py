from ..models.scheduled_webhook_model import ScheduledWebhook


class ScheduledWebhookRepository:
    @staticmethod
    async def add_webhook(channel_id: int, json_data: dict, schedule_time):
        """
        Added a new schedule for the webhook.
        """
        return await ScheduledWebhook.create(
            channel_id=channel_id,
            json_data=json_data,
            schedule_time=schedule_time
        )

    @staticmethod
    async def remove_webhook(webhook_id: int):
        """
        Removes webhook scheduling.
        """
        webhook = await ScheduledWebhook.filter(id=webhook_id).first()
        if webhook:
            await webhook.delete()
            return True
        return False

    @staticmethod
    async def get_due_webhooks(current_time):
        """
        Returns all webhooks that are scheduled for a time earlier than or equal to the current time.
        """
        return await ScheduledWebhook.filter(schedule_time__lte=current_time, sent=False).all()

    @staticmethod
    async def mark_as_sent(webhook_id: int):
        """
        Marks a webhook as sent.
        """
        webhook = await ScheduledWebhook.filter(id=webhook_id).first()
        if webhook:
            webhook.sent = True
            await webhook.save()
            return True
        return False
