from tortoise.models import Model
from tortoise import fields


class Shop(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    description = fields.TextField()
    message_id = fields.BigIntField(null=True)
    channel_id = fields.BigIntField(null=True)

    class Meta:
        table = "shops"

