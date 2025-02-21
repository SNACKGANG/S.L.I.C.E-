import discord
from loguru import logger

from ..models.captcha_config_model import CaptchaConfig


class CaptchaVerifyUseCase:
    """Handles the verification of user-submitted captchas."""

    def __init__(
        self,
        verification_repository: "CaptchaRepository",
        captcha_service: "CaptchaService",
        discord_service: "DiscordService",
    ):
        self.verification_repository = verification_repository
        self.captcha_service = captcha_service
        self.discord_service = discord_service

    async def execute(self, user: discord.Member, user_input: str) -> bool:
        """
        Verifies the user's captcha input and assigns a role if successful.
        """
        try:
            captcha = await self.verification_repository.find_by_user_id(user)
            if not captcha:
                logger.warning(f"No captcha found for user {user.id}")
                return False

            is_valid = await self.captcha_service.validate_captcha(
                user_input, captcha.captcha_text
            )
            if not is_valid:
                logger.warning(f"Invalid captcha input for user {user.id}")
                return False

            await self.verification_repository.mark_as_verified(user)

            config = await CaptchaConfig.get_or_none(guild_id=user.guild.id)
            if config:
                await self.discord_service.add_role_to_user(user, config.role_id)
                logger.success(f"Role {config.role_id} added to user {user.id}")
                return True

            logger.warning(
                f"No verification configuration found for guild {user.guild.id}"
            )
            return False
        except Exception as e:
            logger.error(f"Error in .execute: {e}")
            raise
