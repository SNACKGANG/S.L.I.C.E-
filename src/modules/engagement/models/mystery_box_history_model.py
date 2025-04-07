from tortoise.models import Model
from tortoise import fields


class MysteryBoxHistory(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users", related_name="lootbox_history")
    lootbox_reward = fields.CharField(max_length=255)
    opened_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "mystery_box_history"
