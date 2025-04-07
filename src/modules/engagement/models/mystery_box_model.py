from tortoise.models import Model
from tortoise import fields


class MysteryBox(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    channel_id = fields.BigIntField(unique=True)
    rewards = fields.ManyToManyField(
        "models.Rewards", related_name="boxes_linked_to_rewards"
    )

    class Meta:
        table = "mystery_box"
