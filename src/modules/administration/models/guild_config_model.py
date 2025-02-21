from tortoise import fields, models


class GuildConfig(models.Model):
    """
    Model representing guild configurations.
    """

    guild_id = fields.BigIntField(pk=True)
    guild_name = fields.CharField(max_length=100, null=False)

    class Meta:
        table = "guild_config"
