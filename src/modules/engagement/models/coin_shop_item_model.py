from tortoise.models import Model
from tortoise import fields


class Item(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    description = fields.TextField()
    category = fields.CharField(max_length=100, null=True)
    role_id = fields.BigIntField(null=True)

    class Meta:
        table = "items"

