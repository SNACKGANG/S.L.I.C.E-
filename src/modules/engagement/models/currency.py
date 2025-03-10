from tortoise import fields
from tortoise.models import Model


class Currency(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    currency_type = fields.ForeignKeyField("models.CurrencyType", related_name="currencies")
    amount = fields.IntField(default=0)

    class Meta:
        table = "currencies"
