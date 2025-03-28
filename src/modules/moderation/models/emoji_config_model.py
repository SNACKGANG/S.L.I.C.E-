from tortoise.models import Model
from tortoise import fields


class EmojiConfig(Model):
    id = fields.IntField(pk=True)
    channel_id = fields.BigIntField(unique=True)
    emojis = fields.CharField(max_length=255)

    class Meta:
        table = "emoji_configs"
