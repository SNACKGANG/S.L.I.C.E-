import random

from eth_account.messages import encode_defunct
from hexbytes import HexBytes
from loguru import logger
from web3 import Web3

from ...infrastructure.settings import INFURA_PROJECT_ID


class WalletSignatureService:
    """
    Service to handle Ethereum wallet signature verification using Web3.
    """

    def __init__(self):
        self.w3 = Web3(
            Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}")
        )
        if self.w3.is_connected():
            logger.info("Successfully connected to Ethereum provider.")
        else:
            logger.error("Failed to connect to Ethereum provider.")

    @staticmethod
    def generate_nonce() -> str:
        """
        Generate a random nonce for wallet signature verification.
        """
        nonce = f"SNACKGANG-Verify-{random.randint(100000, 999999)}"
        logger.debug(f"Generated nonce: {nonce}")
        return nonce

    def verify_signature(self, nonce: str, signature: str, user_address: str) -> bool:
        """
        Verify if the given signature matches the provided Ethereum address.
        """
        try:
            logger.debug(f"Verifying signature for address: {user_address}")

            # Encode the message
            encoded_message = encode_defunct(text=nonce)

            # Recover the signing address
            signer = self.w3.eth.account.recover_message(
                encoded_message, signature=HexBytes(signature)
            )

            # Compare with the provided address
            if signer.lower() == user_address.lower():
                logger.info("Signature verification successful.")
                return True
            else:
                logger.warning("Signature verification failed: Address mismatch.")
                return False
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            return False
