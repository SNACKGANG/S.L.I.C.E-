import discord
from discord.ui import Button, View
from loguru import logger


class CaptchaInputView(View):
    def __init__(
        self,
        verification_controller: "CaptchaController",
        verification_service: "VerificationService",
    ):
        super().__init__(timeout=60)
        self.user_input = ""
        self.embed_captcha_message = None
        self.embed_captcha_input_view = None

        # Adds number buttons (0-9)
        for i in range(10):
            self.add_item(self.NumberButton(str(i), verification_service))

        # Cancel Button
        self.add_item(self.CancelButton(verification_service))

        # Submit Button
        self.add_item(self.SubmitButton(verification_controller, verification_service))

    async def format_captcha_input(self):
        """
        Returns the field formatted for the embed of the captcha, ensuring a fixed size.
        """
        combined_input = f"{self.user_input}{' ' * (14 - len(self.user_input))}"
        return combined_input

    class NumberButton(Button):
        def __init__(self, number: str, verification_service: "VerificationService"):
            self.verification_service = verification_service
            super().__init__(
                label=number, style=discord.ButtonStyle.gray, custom_id=f"num_{number}"
            )

        async def callback(self, interaction: discord.Interaction):
            """
            Adds the number to the input field.
            """
            try:
                view: CaptchaInputView = self.view
                view.user_input += self.label
                logger.info(
                    f"User {interaction.user.id} added number {self.label} to captcha input"
                )
                embed_captcha_input_view = view.embed_captcha_input_view
                combined_input = await view.format_captcha_input()

                embed_captcha_input_view.description = f"```{combined_input}```"

                await interaction.response.edit_message(
                    embeds=[view.embed_captcha_message, embed_captcha_input_view],
                    view=view,
                )
            except Exception as e:
                logger.error(
                    f"Error in NumberButton.callback for user {interaction.user.id}: {e}"
                )

    class CancelButton(Button):
        def __init__(self, verification_service: "VerificationService"):
            self.verification_service = verification_service
            super().__init__(
                label="Cancel", style=discord.ButtonStyle.red, custom_id="cancel_button"
            )

        async def callback(self, interaction: discord.Interaction):
            """
            Clears the typing field one character at a time (simulating backspace).
            """
            try:
                view: CaptchaInputView = self.view

                if view.user_input:
                    view.user_input = view.user_input[:-1]
                    logger.info(
                        f"User {interaction.user.id} cleared last character from captcha input"
                    )

                embed_captcha_input_view = view.embed_captcha_input_view
                combined_input = await view.format_captcha_input()

                embed_captcha_input_view.description = f"```{combined_input}```"

                await interaction.response.edit_message(
                    embeds=[view.embed_captcha_message, embed_captcha_input_view],
                    view=view,
                )
            except Exception as e:
                logger.error(
                    f"Error in CancelButton.callback for user {interaction.user.id}: {e}"
                )

    class SubmitButton(Button):
        def __init__(
            self,
            verification_controller: "CaptchaController",
            verification_service: "VerificationService",
        ):
            self.verification_service = verification_service
            super().__init__(
                label="Send", style=discord.ButtonStyle.green, custom_id="submit_button"
            )
            self.verification_controller = verification_controller

        async def callback(self, interaction: discord.Interaction):
            """
            Sends the response for validation.
            """
            try:
                view: CaptchaInputView = self.view
                logger.info(
                    f"User {interaction.user.id} submitted captcha input: {view.user_input}"
                )
                is_valid = await self.verification_controller.verify_captcha(
                    interaction.user, view.user_input
                )
                if is_valid:
                    logger.success(
                        f"Captcha validated successfully for user {interaction.user.id}"
                    )
                    catpcha_correct_embed = (
                        await self.verification_service.create_captcha_sucess_embed()
                    )
                    await interaction.response.edit_message(
                        embed=catpcha_correct_embed, view=None
                    )
                else:
                    logger.warning(
                        f"Invalid captcha input for user {interaction.user.id}"
                    )
                    captcha_incorrect_embed = (
                        await self.verification_service.create_captcha_invalid_embed()
                    )
                    await interaction.response.edit_message(
                        embed=captcha_incorrect_embed, view=None
                    )
            except Exception as e:
                logger.error(
                    f"Error in SubmitButton.callback for user {interaction.user.id}: {e}"
                )
                await interaction.response.edit_message(
                    content="An error occurred while verifying the captcha. Please try again.",
                    embed=None,
                    view=None,
                )
