from datetime import datetime, timezone

from tortoise import fields, models


class Users(models.Model):
    """
    Model representing a user with virtual currency and wallet information.
    """

    user_id = fields.BigIntField(pk=True)
    guild_id = fields.BigIntField(null=True)
    created_at = fields.DatetimeField(
        default=datetime.now(timezone.utc), null=True, timezone=True
    )
    user_level = fields.IntField(null=True)
    wallet_address = fields.CharField(max_length=255, null=True)
    is_wallet_verified = fields.BooleanField(null=True)
    last_daily = fields.DatetimeField(null=True)
    daily_limit = fields.IntField(default=0)

    class Meta:
        table = "users"
        unique_together = ("user_id", "guild_id")
