from tortoise.models import Model
from tortoise import fields


class CurrencyType(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    description = fields.TextField(null=True)

    class Meta:
        table = "currency_types"
