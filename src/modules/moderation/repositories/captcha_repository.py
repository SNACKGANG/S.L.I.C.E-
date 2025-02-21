from datetime import datetime, timedelta, timezone
from typing import Optional

import discord
from loguru import logger
from tortoise.exceptions import DoesNotExist

from ...administration.models.users_model import Users
from ...administration.repositories.user_repository import UserRepository
from ..models.captcha_config_model import CaptchaConfig
from ..models.captcha_users_model import CaptchaUsers


class CaptchaRepository:
    @staticmethod
    async def save(user_id: int, captcha_text: str, guild_id: int):
        """
        Saves a new captcha entry in the database.
        """
        try:
            existing_user = await Users.filter(user_id=user_id).first()
            if not existing_user:
                logger.info(f"User {user_id} not found. Adding to the database.")
                await UserRepository.add_user(user_id)

            existing_verified_captcha = await CaptchaUsers.filter(
                user_id=user_id,
                guild_id=guild_id,
                is_verified=True,
            ).first()

            if existing_verified_captcha:
                logger.info(f"User {user_id} is already verified on server {guild_id}.")
                return False
            else:
                expires_at = datetime.now(timezone.utc) + timedelta(minutes=1)
                await CaptchaUsers.create(
                    user_id=user_id,
                    captcha_text=captcha_text,
                    guild_id=guild_id,
                    expires_at=expires_at,
                )
                logger.success(
                    f"Captcha saved for user {user_id} on the server {guild_id}"
                )
                return True
        except Exception as e:
            logger.error(f"Error saving captcha for user{user_id}: {e}")
            return False

    @staticmethod
    async def find_by_user_id(user: discord.Member) -> Optional[CaptchaUsers]:
        """
        Finds a captcha entry by user ID.
        """
        try:
            captcha = (
                await CaptchaUsers.filter(user_id=user.id, guild_id=user.guild.id)
                .order_by("-created_at")
                .first()
            )
            if captcha:
                logger.info(f"Captcha found for the user {user.id}")
            else:
                logger.warning(f"Captcha not found for user {user.id}")
            return captcha
        except DoesNotExist:
            logger.warning(f"Captcha not found for user {user.id}")
            return None

    @staticmethod
    async def is_user_verified(user_id: int, guild_id: int) -> bool:
        """
        Checks if the user is already verified on the server.
        Returns True if the user is verified, False otherwise.
        """
        try:
            existing_verified_captcha = await CaptchaUsers.filter(
                user_id=user_id,
                guild_id=guild_id,
                is_verified=True,
            ).first()

            if existing_verified_captcha:
                logger.info(f"User {user_id} is already verified on server {guild_id}.")
                return True
            else:
                logger.info(f"User {user_id} is not verified on server {guild_id}.")
                return False
        except Exception as e:
            logger.error(f"Error checking verification status for user {user_id}: {e}")
            return False

    async def mark_as_verified(self, user: "discord.Member"):
        """
        Marks a captcha as verified.
        """
        try:
            captcha = await self.find_by_user_id(user)
            if captcha:
                await CaptchaUsers.filter(captcha_id=captcha.captcha_id).update(
                    is_verified=True
                )
                logger.success(
                    f"Captcha {captcha.captcha_id} marked as verified for user {user.id}"
                )
            else:
                logger.warning(f"No active captcha found for user {user.id}")
        except Exception as e:
            logger.error(f"Error marking captcha as verified for user {user.id}:{e}")

    @staticmethod
    async def delete_expired_captchas():
        """
        Deletes expired captchas from the database.
        """
        try:
            deleted_count = await CaptchaUsers.filter(
                expires_at__lt=datetime.now(timezone.utc)
            ).delete()
            logger.info(f"{deleted_count} expired captchas deleted")
        except Exception as e:
            logger.error(f"Error deleting expired captchas: {e}")

    @staticmethod
    async def save_verification_channel(guild_id: int, channel_id: int, role_id: int):
        """
        Saves the verification channel in the database.
        """
        try:
            existing_config = await CaptchaConfig.filter(guild_id=guild_id).first()
            if existing_config:
                existing_config.channel_id = channel_id
                await existing_config.save()
                logger.info(f"Updated verification channel for the server {guild_id}")
            else:
                await CaptchaConfig.create(
                    guild_id=guild_id, channel_id=channel_id, role_id=role_id
                )
                logger.success(f"Verification channel saved for the server{guild_id}")
        except Exception as e:
            logger.error(
                f"Error saving verification channel to server  {guild_id}: {e}"
            )

    @staticmethod
    async def get_verification_channel(guild_id: int) -> int:
        """
        Returns the server's verification channel ID.
        """
        try:
            config = await CaptchaConfig.filter(guild_id=guild_id).first()
            if config:
                logger.info(f"Verification channel found for the server  {guild_id}")
            else:
                logger.warning(
                    f"Verification channel not found for the server  {guild_id}"
                )
            return config.channel_id if config else None
        except Exception as e:
            logger.error(
                f"Error when searching for verification channel for the server  {guild_id}: {e}"
            )
            return None

    @staticmethod
    async def delete_user_captcha(user_id: int, guild_id: int):
        """
        Deletes all captchas for a user when they leave the server.
        """
        try:
            deleted_count = await CaptchaUsers.filter(
                user_id=user_id,
                guild_id=guild_id,
            ).delete()
            logger.info(
                f"Deleted {deleted_count} captchas for user {user_id} on server {guild_id}"
            )
        except Exception as e:
            logger.error(f"Error deleting captchas for user {user_id}: {e}")
