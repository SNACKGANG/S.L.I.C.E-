from tortoise.models import Model
from tortoise import fields


class Rewards(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    value = fields.CharField(max_length=255)
    chance = fields.IntField()
    limit = fields.IntField(default=0)
    opened_this_month = fields.IntField(default=0)
    color = fields.CharField(max_length=10, default="0xFFFFFF")
    image_url = fields.CharField(max_length=255, null=True)
    mystery_boxes = fields.ManyToManyField(
        "models.MysteryBox", related_name="rewards_linked_to_box"
    )
    currency_id = fields.IntField(null=True)

    class Meta:
        table = "rewards"
        dependencies = ["models.MysteryBox"]
