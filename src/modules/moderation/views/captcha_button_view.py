import discord
from discord.ui import Button, View
from loguru import logger

from src.modules.moderation.repositories.captcha_repository import \
    CaptchaRepository
from src.modules.moderation.views.captcha_safety_tips_view import \
    CaptchaSafetyTipsView


class VerificationButtonView(View):
    """
    View that contains the verification and FAQ buttons.
    """

    def __init__(
        self,
        verification_service: "CaptchaEmbedService",
        verification_controller: "CaptchaController",
    ):
        """
        Initializes the verification and FAQ buttons.

        :param verification_service: Service used to create embeds.
        :param verification_controller: Controller that manages the verification process.
        """
        super().__init__(timeout=None)
        self.add_item(self.VerifyButton(verification_controller, verification_service))
        self.add_item(self.FAQButton(verification_service))

    class VerifyButton(Button):
        """
        Button to start the user verification process.
        """

        def __init__(
            self,
            verification_controller: "CaptchaController",
            verification_service: "VerificationService",
        ):
            self.verification_controller = verification_controller
            self.verification_service = verification_service
            super().__init__(
                label="Verify",
                style=discord.ButtonStyle.green,
                custom_id="verify_button",
            )

        async def callback(self, interaction: discord.Interaction):
            """
            Callback for the verification button. Starts the user's verification process.
            """
            try:
                logger.info(
                    f"Verification started for user {interaction.user.id} in guild {interaction.guild_id}"
                )
                is_verified = await CaptchaRepository.is_user_verified(
                    interaction.user.id, interaction.guild_id
                )

                if is_verified:
                    await interaction.response.send_message(
                        "You are already verified", ephemeral=True
                    )
                    logger.info(
                        f"User {interaction.user.id} in guild {interaction.guild_id} has already verified"
                    )
                    return

                view = CaptchaSafetyTipsView(
                    self.verification_controller, self.verification_service
                )
                embed = await self.verification_service.create_safety_tips_embed()

                await interaction.response.send_message(
                    embed=embed, view=view, ephemeral=True
                )
                logger.success(
                    f"Rules message sent to user {interaction.user.id} - Verification Step 1"
                )
            except Exception as e:
                logger.error(
                    f"Error in VerifyButton.callback for user {interaction.user.id}: {e}"
                )
                await interaction.response.send_message(
                    "An error occurred while starting verification. Please try again.",
                    ephemeral=True,
                )

    class FAQButton(Button):
        """
        Button to show the FAQ for the user.
        """

        def __init__(self, verification_service):
            super().__init__(
                label="FAQ", style=discord.ButtonStyle.blurple, custom_id="faq_button"
            )
            self.verification_service = verification_service

        async def callback(self, interaction: discord.Interaction):
            """
            Callback for the FAQ button. Sends the FAQ to the user.
            """
            try:
                logger.info(f"FAQ requested by user {interaction.user.id}")
                embed = await self.verification_service.create_faq_embed()
                await interaction.response.send_message(embed=embed, ephemeral=True)
                logger.success(f"FAQ sent to user {interaction.user.id}")
            except Exception as e:
                logger.error(
                    f"Error in FAQButton.callback for user {interaction.user.id}: {e}"
                )
                await interaction.response.send_message(
                    "An error occurred while fetching the FAQ. Please try again.",
                    ephemeral=True,
                )
