from tortoise.models import Model
from tortoise import fields


class ShopItem(Model):
    id = fields.IntField(pk=True)
    shop = fields.ForeignKeyField("models.Shop", related_name="shop_items")
    item = fields.ForeignKeyField("models.Item", related_name="item_shops")
    price = fields.FloatField()
    stock = fields.IntField()
    restricted_role_id = fields.BigIntField(null=True)
    user_purchase_limit = fields.IntField(null=True)

    class Meta:
        table = "shop_items"
