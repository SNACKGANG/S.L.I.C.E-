from tortoise import fields, models


class HolderVerificationModel(models.Model):
    """
    Model representing a holder verification record.
    """

    id = fields.IntField(pk=True)
    wallet_address = fields.CharField(max_length=255)
    discord_user_id = fields.BigIntField()
    guild_id = fields.BigIntField()
    nft_count = fields.IntField(default=0)

    class Meta:
        table = "holder_verification"
