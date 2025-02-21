import asyncio

from loguru import logger

from src.modules.automation.repositories.holder_user_role_repository import \
    HolderUserRoleRepository
from src.shared.services.discord_service import DiscordService


class HolderVerificationUseCase:
    """
    Use case responsible for verifying if a wallet holds the required tokens.
    """

    def __init__(
        self,
        holder_service: "HolderVerificationService",
        holder_config_repository: "HolderConfigRepository",
        holder_verification_repository: "HolderVerificationRepository",
    ):
        self.holder_service = holder_service
        self.holder_config_repository = holder_config_repository
        self.holder_verification_repository = holder_verification_repository

    async def execute(self, wallet_address: str, user: "discord.Member"):
        """
        Executes the verification logic to check if the wallet address holds tokens.
        """
        try:
            verification_event = asyncio.Event()

            await self.holder_service.add_task_to_queue(
                wallet_address, verification_event
            )

            await verification_event.wait()

            nft_count = verification_event.result
            await self.holder_verification_repository.upsert(
                wallet_address, user.id, user.guild.id, nft_count
            )

            if nft_count == 0:
                logger.info(f"Wallet {wallet_address} has no tokens in the collection.")
                return False

            return await self._update_user_role(user)
        except Exception as e:
            logger.error(f"Error during wallet verification for {wallet_address}: {e}")

    async def _update_user_role(self, user: "discord.Member"):
        """
        Auxiliary method that updates the user role based on the amount of NFTs
        """
        user_id = user.id
        guild_id = user.guild.id

        total_nft_count = (
            await self.holder_verification_repository.get_total_nfts_by_user(
                user_id, guild_id
            )
        )
        new_role_id = await self.holder_config_repository.get_role_by_nft_amount(
            total_nft_count
        )

        if new_role_id:
            current_role_id = await HolderUserRoleRepository.get_current_user_role(
                user_id, guild_id
            )

            if new_role_id != current_role_id:
                if current_role_id:
                    await DiscordService.remove_role_from_user(user, current_role_id)
            await DiscordService.add_role_to_user(user, new_role_id)

            await HolderUserRoleRepository.update_user_role(
                user_id, guild_id, new_role_id
            )
            return True
        else:
            logger.warning(
                f"No role found for user {user_id} in guild {guild_id} with {total_nft_count} NFTs."
            )
            return False
