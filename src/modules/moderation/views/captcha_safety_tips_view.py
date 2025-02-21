import discord
from discord.ui import Button, View
from loguru import logger

from src.modules.moderation.views.captcha_rules_view import CaptchaRulesView


class CaptchaSafetyTipsView(View):
    """
    View that provides safety tips during the verification process.
    """

    def __init__(
        self,
        verification_controller: "CaptchaController",
        verification_service: "VerificationService",
    ):
        super().__init__(timeout=None)
        self.add_item(
            self.CaptchaSafetyTipsButton(verification_controller, verification_service)
        )

    class CaptchaSafetyTipsButton(Button):
        """
        Button to continue to the next step after reading safety tips.
        """

        def __init__(
            self,
            verification_controller: "CaptchaController",
            verification_service: "VerificationService",
        ):
            """
            Initializes the continue button after reading safety tips.
            """
            self.verification_controller = verification_controller
            self.verification_service = verification_service
            super().__init__(
                label="Continue",
                style=discord.ButtonStyle.primary,
                custom_id="safety_tips_button",
            )

        async def callback(self, interaction: discord.Interaction):
            """
            Callback for the safety tips button. Moves to the rules step of the verification.
            """
            try:
                logger.info(
                    f"Safety tips read by user {interaction.user.id} in guild {interaction.guild_id} - Verification step 1"
                )
                view = CaptchaRulesView(
                    self.verification_controller, self.verification_service
                )
                embed = await self.verification_service.create_rules_embed()

                await interaction.response.edit_message(embed=embed, view=view)
                logger.success(f"Rules message sent to user {interaction.user.id}")
            except Exception as e:
                logger.error(
                    f"Error in CaptchaSafetyTipsButton callback for user {interaction.user.id}: {e}"
                )
                await interaction.response.send_message(
                    "An error occurred in step 1 of user verification. Please try again.",
                    ephemeral=True,
                )
