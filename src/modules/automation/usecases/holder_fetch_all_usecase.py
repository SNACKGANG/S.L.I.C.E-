import asyncio

from loguru import logger

from src.modules.automation.repositories.holder_user_role_repository import \
    HolderUserRoleRepository
from src.shared.services.discord_service import DiscordService


class HolderFetchAllUseCase:
    """
    Use case responsible for fetching and updating all holders' roles based on their NFTs.
    """

    def __init__(
        self,
        holder_service: "HolderVerificationService",
        holder_repository: "HolderVerificationRepository",
        config_repository: "HolderConfigRepository",
        bot: "discord.Client",
    ):
        self.holder_service = holder_service
        self.holder_repository = holder_repository
        self.holder_config_repository = config_repository
        self.bot = bot

    async def execute(self, guild_id: int) -> int:
        """
        Fetches all holders, checks their NFT amounts, and updates their roles accordingly.
        """
        try:
            collection_address = (
                await self.holder_config_repository.get_collection_address_by_guild_id(
                    guild_id
                )
            )

            if collection_address:
                holders_data = (
                    await self.holder_service.get_all_holders_for_verification(
                        collection_address
                    )
                )

                wallet_addresses = list(holders_data.keys())
                users = await self.holder_repository.get_all_users_by_wallet_addresses(
                    wallet_addresses, guild_id
                )
                user_dict = {user.wallet_address: user for user in users}

                semaphore = asyncio.Semaphore(100)
                tasks = [
                    self.update_user_role_semaphore(
                        wallet_address,
                        user.discord_user_id,
                        user.guild_id,
                        nft_count,
                        semaphore,
                    )
                    for wallet_address, nft_count in holders_data.items()
                    if (user := user_dict.get(wallet_address))
                ]

                completed_tasks = 0
                batch_size = 100

                for i in range(0, len(tasks), batch_size):
                    current_batch = tasks[i : i + batch_size]
                    await asyncio.gather(*current_batch)
                    completed_tasks += len(current_batch)

                logger.success("Batch verification and role updates completed.")
                return completed_tasks
            else:
                logger.error(f"No collection address found for guild {guild_id}")
                return 0
        except Exception as e:
            logger.error(f"Error during batch wallet verification: {e}")

    async def update_user_role_semaphore(
        self,
        wallet_address: str,
        user_id: int,
        guild_id: int,
        nft_count: int,
        semaphore: asyncio.Semaphore,
    ):
        async with semaphore:
            await self.update_user_role_based_on_nfts(
                wallet_address, user_id, guild_id, nft_count
            )

    async def update_user_role_based_on_nfts(
        self, wallet_address: str, user_id: int, guild_id: int, nft_count: int
    ):
        """
        Updates the role for a given wallet based on NFT count.
        """
        total_nft_count = await self.holder_repository.get_total_nfts_by_user(
            user_id, guild_id
        )
        new_role_id = await self.holder_config_repository.get_role_by_nft_amount(
            total_nft_count
        )

        if new_role_id is None:
            logger.warning(
                f"No role found for user {user_id} in guild {guild_id} with {total_nft_count} NFTs."
            )
            return

        current_role_id = await HolderUserRoleRepository.get_current_user_role(
            user_id, guild_id
        )

        user = self.bot.get_user(user_id)

        if not user:
            logger.warning(f"User with ID {user_id} not found in bot cache.")
            return

        if new_role_id != current_role_id:
            logger.info(
                f"Updating role for user {user_id} in guild {guild_id}: {current_role_id} -> {new_role_id}"
            )

            if current_role_id:
                await DiscordService.remove_role_from_user(user, current_role_id)

            await DiscordService.add_role_to_user(user, new_role_id)
            await HolderUserRoleRepository.update_user_role(
                user_id, guild_id, new_role_id
            )

        await self.holder_repository.upsert(
            wallet_address, user_id, guild_id, nft_count
        )
