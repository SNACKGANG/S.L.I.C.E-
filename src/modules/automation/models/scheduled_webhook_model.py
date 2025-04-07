from tortoise.models import Model
from tortoise import fields
from datetime import datetime, timezone


class ScheduledWebhook(Model):
    id = fields.IntField(pk=True)
    channel_id = fields.BigIntField()
    json_data = fields.JSONField()
    schedule_time = fields.DatetimeField()
    sent = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(default=datetime.now(timezone.utc), timezone=True)

    class Meta:
        table = "scheduled_webhooks"
