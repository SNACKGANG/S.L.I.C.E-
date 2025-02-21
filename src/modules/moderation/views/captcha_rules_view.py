import discord
from discord.ui import Button, View
from loguru import logger

from src.modules.moderation.views.captcha_input_view import CaptchaInputView


class CaptchaRulesView(View):
    """
    View that shows the rules during the verification process.
    """

    def __init__(
        self,
        verification_controller: "CaptchaController",
        verification_service: "VerificationService",
    ):
        super().__init__(timeout=None)
        self.add_item(
            self.CaptchaRulesButton(verification_controller, verification_service)
        )

    class CaptchaRulesButton(Button):
        """
        Button to continue to the next step of the verification process.
        """

        def __init__(
            self,
            verification_controller: "CaptchaController",
            verification_service: "VerificationService",
        ):
            self.verification_controller = verification_controller
            self.verification_service = verification_service
            super().__init__(
                label="Continue",
                style=discord.ButtonStyle.primary,
                custom_id="rules_button",
            )

        async def callback(self, interaction: discord.Interaction):
            """
            Callback for the rules button. Starts the captcha verification.
            """
            try:
                logger.info(
                    f"Verification started for user {interaction.user.id} in guild {interaction.guild_id} - Verification step 2"
                )
                embed_captcha_message = (
                    await self.verification_controller.start_verification(
                        interaction.user, interaction.guild_id
                    )
                )
                embed_captcha_input_view = (
                    await self.verification_service.create_captcha_input_embed()
                )
                view = CaptchaInputView(
                    self.verification_controller, self.verification_service
                )

                view.embed_captcha_message = embed_captcha_message
                view.embed_captcha_input_view = embed_captcha_input_view

                await interaction.response.edit_message(
                    embeds=[embed_captcha_message, embed_captcha_input_view], view=view
                )
                logger.success(
                    f"Verification message sent to user {interaction.user.id}"
                )
            except Exception as e:
                logger.error(
                    f"Error in CaptchaRulesButton.callback for user {interaction.user.id}: {e}"
                )
                await interaction.response.send_message(
                    "An error occurred in step 2 of user verification. Please try again.",
                    ephemeral=True,
                )
