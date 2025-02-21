from tortoise import fields, models


class CaptchaUsers(models.Model):
    """Stores captcha data for users in a guild."""

    captcha_id = fields.IntField(pk=True, generated=True)
    user_id = fields.BigIntField()
    captcha_text = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True, timezone=True)
    expires_at = fields.DatetimeField(null=True, timezone=True)
    is_verified = fields.BooleanField(default=False)
    guild_id = fields.BigIntField()

    class Meta:
        table = "captcha_users"
