import discord
from loguru import logger

from ..models.captcha_config_model import CaptchaConfig
from ..services.captcha_embed_service import CaptchaEmbedService


class CaptchaGenerateUseCase:
    """Handles the generation and distribution of captchas for user verification."""

    def __init__(
        self,
        verification_repository: "CaptchaRepository",
        captcha_service: "CaptchaService",
        captcha_embed_service: "CaptchaEmbedService",
    ):
        self.verification_repository = verification_repository
        self.captcha_service = captcha_service
        self.captcha_embed_service = captcha_embed_service

    async def execute(self, user: discord.Member, guild_id: int):
        """
        Generates a captcha, saves it, and creates an embed for user verification.
        """
        try:
            config = await CaptchaConfig.get_or_none(guild_id=guild_id)
            if not config:
                logger.error(
                    f"Verification configuration not found for guild {guild_id}"
                )
                raise ValueError(
                    "Verification configuration not found for this server."
                )

            (
                captcha_text,
                captcha_image_url,
            ) = await self.captcha_service.generate_captcha()
            logger.info(f"Captcha generated for user {user.id} in guild {guild_id}")

            is_saved = await self.verification_repository.save(
                user.id, captcha_text, guild_id
            )

            if is_saved:
                logger.success(f"Captcha saved for user {user.id} in guild {guild_id}")

            embed_message = await self.captcha_embed_service.create_verification_embed(
                captcha_image_url
            )
            logger.info(f"Verification embed created for user {user.id}")

            return embed_message
        except Exception as e:
            logger.error(f"Error in execute: {e}")
            raise
