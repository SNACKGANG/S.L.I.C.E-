from tortoise import fields, models


class SalesNftConfig(models.Model):
    """
    Model representing the NFT sales configuration for a Discord server.
    """

    id = fields.IntField(pk=True)
    guild_id = fields.BigIntField()
    channel_id = fields.BigIntField()
    contract_address = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "sales_nft_config"
