import io
import random
from typing import Tuple

import discord
from captcha.image import ImageCaptcha
from loguru import logger

from src.shared.services.http_client import AioHttpClient
from src.shared.services.imgbb_service import ImgBBService


class CaptchaService:
    def __init__(self, bot: "discord.Client") -> None:
        self.bot = bot

    @staticmethod
    async def generate_captcha() -> Tuple[str, str]:
        """
        Generates a captcha and returns the text and image URL.
        """
        try:
            captcha_text = "".join(random.choices("0123456789", k=6))
            logger.info(f"Captcha generated: {captcha_text}")

            image = ImageCaptcha(width=200, height=90)
            img_bytes = io.BytesIO()
            image.write(captcha_text, img_bytes, format="PNG")
            img_bytes.seek(0)

            imgur_service = ImgBBService(http_client=AioHttpClient())
            img_url = await imgur_service.upload_image(img_bytes.getvalue())
            logger.success(f"Captcha uploaded to Imgur: {img_url}")

            return captcha_text, img_url
        except Exception as e:
            logger.error(f"Error generating captcha: {e}")
            raise

    @staticmethod
    async def validate_captcha(user_input: str, captcha_text: str) -> bool:
        """
        Validates the user's input against the captcha text.
        """
        try:
            result = user_input == captcha_text
            if result:
                logger.success(f"Captcha successfully validated: {captcha_text}")
            else:
                logger.warning(
                    f"Invalid captcha: expected {captcha_text}, received {user_input}"
                )
            return result
        except Exception as e:
            logger.error(f"Error validating captcha: {e}")
            raise
