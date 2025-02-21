from loguru import logger
from tortoise.expressions import Q
from tortoise.functions import Sum

from src.modules.automation.models.holder_verification_model import \
    HolderVerificationModel


class HolderVerificationRepository:
    """
    Repository class responsible for managing wallet verification statuses in the database.
    """

    @staticmethod
    async def get_all_users_by_wallet_addresses(wallet_addresses: list, guild_id: int):
        """
        Retrieves the verification records for a list of wallet addresses in a given guild.
        """
        try:
            wallet_addresses = [address.lower() for address in wallet_addresses]

            return await HolderVerificationModel.filter(
                Q(wallet_address__in=wallet_addresses), guild_id=guild_id
            ).all()
        except Exception as e:
            logger.error(
                f"Error retrieving verifications for wallet addresses in guild {guild_id}: {e}"
            )
            return

    @staticmethod
    async def upsert(
        wallet_address: str, discord_user_id: int, guild_id: int, nft_count: int
    ):
        """
        Inserts or updates the verification record for a wallet address and guild.
        """
        try:
            verification, created = await HolderVerificationModel.get_or_create(
                wallet_address=wallet_address.lower(),
                discord_user_id=discord_user_id,
                guild_id=guild_id,
                defaults={"nft_count": nft_count},
            )

            if not created:
                verification.nft_count = nft_count
                await verification.save()

            logger.info(
                f"Verification updated for {wallet_address} in guild {guild_id}: {nft_count} NFTs assigned to {discord_user_id}"
            )
        except Exception as e:
            logger.error(
                f"Error updating verification for {wallet_address} in guild {guild_id}: {e}"
            )

    @staticmethod
    async def get_total_nfts_by_user(discord_user_id: int, guild_id: int) -> int:
        """
        Fetches the total NFT count across all wallets linked to a user in a guild.
        """
        try:
            result = (
                await HolderVerificationModel.filter(
                    discord_user_id=discord_user_id, guild_id=guild_id
                )
                .annotate(total_nfts=Sum("nft_count"))
                .values("total_nfts")
            )

            return result[0]["total_nfts"] if result and result[0]["total_nfts"] else 0
        except Exception as e:
            logger.error(
                f"Error retrieving total NFTs for user {discord_user_id} in guild {guild_id}: {e}"
            )
            return 0
