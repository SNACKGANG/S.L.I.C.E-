from tortoise import fields, models


class CaptchaConfig(models.Model):
    """Represents the captcha configuration for a guild."""

    id = fields.IntField(pk=True, generated=True)
    guild_id = fields.BigIntField(unique=True)
    channel_id = fields.BigIntField()
    role_id = fields.BigIntField()

    class Meta:
        table = "captcha_config"
