import discord
from discord.ui import Button, Modal, TextInput, View
from loguru import logger


class SignatureButtonView(View):
    """
    View containing the button to submit the wallet signature.
    """

    def __init__(self, verification_controller, wallet_service, wallet, nonce):
        super().__init__(timeout=None)
        self.verification_controller = verification_controller
        self.wallet_service = wallet_service
        self.wallet = wallet
        self.nonce = nonce

        self.add_item(
            self.SignatureButton(
                self.verification_controller,
                self.wallet_service,
                self.wallet,
                self.nonce,
            )
        )

    class SignatureButton(Button):
        """
        Button to submit the signed message for verification.
        """

        def __init__(self, verification_controller, wallet_service, wallet, nonce):
            super().__init__(
                label="Send Signature",
                style=discord.ButtonStyle.blurple,
                custom_id="submit_signature_button",
            )
            self.verification_controller = verification_controller
            self.wallet_service = wallet_service
            self.wallet = wallet
            self.nonce = nonce

        async def callback(self, interaction: discord.Interaction):
            """
            Opens the modal for users to input their signature.
            """
            await interaction.response.send_modal(
                SignatureVerificationModal(
                    self.verification_controller,
                    self.wallet_service,
                    self.wallet,
                    self.nonce,
                )
            )


class SignatureVerificationModal(Modal):
    """
    Modal for users to submit their signature for verification.
    """

    def __init__(
        self,
        verification_controller: "HolderVerificationController",
        wallet_service: "WalletSignatureService",
        wallet_address: str,
        nonce: str,
    ):
        super().__init__(title="Signature of the Wallet")
        self.verification_controller = verification_controller
        self.wallet_service = wallet_service
        self.nonce = nonce

        self.wallet_address = wallet_address
        self.signature = TextInput(
            label="Paste your signature here", placeholder="0x...", max_length=255
        )

        self.add_item(self.signature)

    async def on_submit(self, interaction: discord.Interaction):
        """
        Processes and verifies the submitted signature.
        """
        try:
            signature = self.signature.value

            logger.info(f"Signature received for {self.wallet_address}: {signature}")

            is_valid = self.wallet_service.verify_signature(
                self.nonce, signature, self.wallet_address
            )

            if not is_valid:
                await interaction.response.send_message(
                    "Invalid signature! Make sure you signed correctly.", ephemeral=True
                )
                return

            logger.info(f"Signature validated for {self.wallet_address}")

            result = await self.verification_controller.handle_individual_verification(
                self.wallet_address,
                interaction.user,
            )

            if result:
                await interaction.response.send_message(
                    "Your wallet has been successfully verified!", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "You do not have enough NFTs to be given a role.",
                    ephemeral=True,
                )
        except Exception as e:
            logger.error(f"Error processing signature: {e}")
