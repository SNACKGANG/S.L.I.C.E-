import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger

from src.modules.moderation.repositories.captcha_repository import \
    CaptchaRepository
from src.modules.moderation.services.captcha_embed_service import \
    CaptchaEmbedService
from src.modules.moderation.views.captcha_button_view import \
    VerificationButtonView
from src.shared.services.discord_service import DiscordService


class CaptchaConfigCog(commands.Cog):
    def __init__(self, bot, verification_controller):
        self.bot = bot
        self.verification_controller = verification_controller
        self.captcha_embed_service = CaptchaEmbedService()

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """
        Event triggered when a member leaves the server.
        """
        try:
            # Delete the captcha associated with the user who left
            await CaptchaRepository.delete_user_captcha(member.id, member.guild.id)
            logger.info(
                f"Captchas for user {member.id} deleted after leaving the server."
            )
        except Exception as e:
            logger.error(f"Error deleting captchas for user {member.id}: {e}")

    @app_commands.command(
        name="captcha_verification_config",
        description="Configure the channel for captcha verification.",
    )
    @app_commands.describe(
        channel="Channel where the verification message will be sent"
    )
    @app_commands.default_permissions(administrator=True)
    async def captcha_verification_config(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        role: discord.Role,
    ):
        """
        Command to configure the scan channel and post the fixed message with the buttons.
        Only administrators can use this command.
        """
        try:
            if not interaction.user.guild_permissions.administrator:
                logger.warning(
                    f"User {interaction.user.id} tried to configure captcha without administrator permissions"
                )
                await interaction.response.send_message(
                    "You need to be an administrator to use this command!",
                    ephemeral=True,
                )
                return

            logger.info(
                f"Configuring captcha verification for guild {interaction.guild.id} by user {interaction.user.id}"
            )
            await CaptchaRepository.save_verification_channel(
                interaction.guild.id, channel.id, role.id
            )
            logger.success(
                f"Verification channel set to {channel.id} and role set to {role.id} for guild {interaction.guild.id}"
            )

            welcome_embed = await self.captcha_embed_service.create_welcome_embed()
            welcome_view = VerificationButtonView(
                self.captcha_embed_service, self.verification_controller
            )

            discord_service = DiscordService(self.bot)
            await discord_service.send_message(
                embed=welcome_embed, view=welcome_view, channel_id=channel.id
            )
            logger.success(
                f"Welcome message and verification buttons sent to channel {channel.id}"
            )

            await interaction.response.send_message(
                f"The verification channel has been set to {channel.mention} "
                f"and the role has been assigned to <@&{role.id}>!",
                ephemeral=True,
            )
            logger.info(
                f"Configuration confirmation sent to user {interaction.user.id}"
            )
        except Exception as e:
            logger.error(
                f"Error in captcha_verification_config for guild {interaction.guild.id}: {e}"
            )
            await interaction.response.send_message(
                "An error occurred while configuring the verification channel. Please try again.",
                ephemeral=True,
            )


async def setup(bot, verification_controller):
    await bot.add_cog(CaptchaConfigCog(bot, verification_controller))
    logger.info("CaptchaConfigCog loaded successfully")
