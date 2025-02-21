import discord
from loguru import logger


class CaptchaController:
    """Manages the generation and verification of captchas for Discord users."""

    def __init__(self, generate_captcha_usecase, verify_captcha_usecase):
        self.generate_captcha_usecase = generate_captcha_usecase
        self.verify_captcha_usecase = verify_captcha_usecase

    async def start_verification(self, user: discord.Member, guild_id: int):
        """Starts the captcha verification process for a user."""
        try:
            embed = await self.generate_captcha_usecase.execute(user, guild_id)
            logger.success(f"Verification successfully started for user {user.id}")
            return embed
        except Exception as e:
            logger.error(f"Error starting verification for user {user.id}: {e}")
            raise

    async def verify_captcha(self, user: discord.Member, user_input: str) -> bool:
        """Verifies the user's captcha input."""
        try:
            result = await self.verify_captcha_usecase.execute(user, user_input)
            if result:
                logger.success(f"Captcha successfully validated for user {user.id}")
            else:
                logger.warning(f"Invalid captcha for user {user.id}")
            return result
        except Exception as e:
            logger.error(f"Error verifying captcha for user {user.id}: {e}")
            raise
