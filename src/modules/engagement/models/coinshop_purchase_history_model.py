from tortoise.models import Model
from tortoise import fields


class PurchaseHistory(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()  
    shop = fields.ForeignKeyField("models.Shop", related_name="purchases")
    item = fields.ForeignKeyField("models.Item", related_name="purchases")
    quantity = fields.IntField()
    total_price = fields.FloatField()
    purchase_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "purchase_history"
