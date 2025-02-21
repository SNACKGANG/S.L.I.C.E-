import discord
from discord.ui import Button, Modal, TextInput, View
from loguru import logger

from src.shared.services.walletsignature_service import WalletSignatureService

from .holder_signature_view import SignatureButtonView


class HolderVerificationButtonView(View):
    """
    View containing the verification button for NFT holders.
    """

    def __init__(self, verification_controller: "HolderVerificationController"):
        super().__init__(timeout=None)
        self.verification_controller = verification_controller
        self.add_item(self.VerifyButton(self.verification_controller))

    class VerifyButton(Button):
        """
        Button to trigger the verification process.
        """

        def __init__(self, verification_controller: "HolderVerificationController"):
            super().__init__(
                label="Start Verification",
                style=discord.ButtonStyle.green,
                custom_id="holder_verify_button",
            )
            self.verification_controller = verification_controller

        async def callback(self, interaction: discord.Interaction):
            """
            Handles button click to open the verification modal.
            """
            try:
                logger.info(
                    f"Verification started by {interaction.user.id} on the server {interaction.guild_id}"
                )
                await interaction.response.send_modal(
                    HolderWalletModal(self.verification_controller)
                )
            except Exception as e:
                logger.error(f"Error starting scan: {e}")


class HolderWalletModal(Modal):
    """
    Modal for users to enter their NFT wallet address.
    """

    def __init__(self, verification_controller: "HolderVerificationController"):
        super().__init__(title="Verification of Holder")
        self.verification_controller = verification_controller
        self.wallet_service = WalletSignatureService()
        self.wallet_address = TextInput(
            label="Address of your NFT wallet", placeholder="0x...", max_length=255
        )
        self.add_item(self.wallet_address)

    async def on_submit(self, interaction: discord.Interaction):
        """
        Processes the wallet address and sends a nonce for signature verification.
        """
        try:
            wallet = self.wallet_address.value
            user_id = interaction.user.id
            guild_id = interaction.guild_id

            logger.info(f"Wallet received: {wallet} for user {user_id}")

            nonce = self.wallet_service.generate_nonce()

            view = SignatureButtonView(
                self.verification_controller, self.wallet_service, wallet, nonce
            )

            await interaction.response.send_message(
                f"To check your wallet, sign the following message in your wallet:\n\n```{nonce}```\n\n"
                "After signing, click the button below to send your signature.",
                view=view,
                ephemeral=True,
            )
        except Exception as e:
            logger.error(f"Error processing the check: {e}")
