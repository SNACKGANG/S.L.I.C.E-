from tortoise import fields, models


class HolderRoleThresholdModel(models.Model):
    """
    Model representing the role assigned based on NFT item_quantity thresholds.
    """

    id = fields.IntField(pk=True)
    config = fields.ForeignKeyField(
        "models.HolderVerificationConfigModel", related_name="thresholds"
    )
    min_nft = fields.IntField()
    max_nft = fields.IntField(null=True)
    role_id = fields.BigIntField()

    class Meta:
        table = "holder_role_threshold"
