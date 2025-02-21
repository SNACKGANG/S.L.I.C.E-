from tortoise import fields, models


class HolderVerificationConfigModel(models.Model):
    """
    Model representing the holder verification configuration for a specific guild.
    """

    id = fields.IntField(pk=True)
    collection_address = fields.CharField(max_length=255)
    guild_id = fields.BigIntField()

    class Meta:
        table = "holder_verification_config"
        unique_together = ("guild_id", "collection_address")
