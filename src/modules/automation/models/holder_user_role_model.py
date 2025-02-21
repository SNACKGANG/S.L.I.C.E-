from tortoise import fields, models


class HolderUserRoleModel(models.Model):
    """
    Model representing a user's role based on their total NFTs.
    """

    id = fields.IntField(pk=True)
    discord_user_id = fields.BigIntField()
    guild_id = fields.BigIntField()
    role_id = fields.BigIntField()

    class Meta:
        table = "holder_user_roles"
