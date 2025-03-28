from tortoise.models import Model
from tortoise import fields


class ThreadConfig(Model):
    id = fields.IntField(pk=True)
    channel_id = fields.BigIntField(unique=True)
    name = fields.CharField(max_length=255)
    auto_archive_duration = fields.IntField()
    reason = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "thread_configs"
