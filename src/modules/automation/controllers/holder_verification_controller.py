from loguru import logger

from ..usecases.holder_fetch_all_usecase import HolderFetchAllUseCase
from ..usecases.holder_verification_usecase import HolderVerificationUseCase


class HolderVerificationController:
    """
    Controller responsible for verifying holders and updating roles in the server.
    """

    def __init__(
        self,
        holder_verification_usecase: HolderVerificationUseCase,
        holder_fetch_all_usecase: HolderFetchAllUseCase,
    ):
        self.holder_verification_usecase = holder_verification_usecase
        self.holder_fetch_all_usecase = holder_fetch_all_usecase

    async def handle_individual_verification(
        self, wallet_address: str, user: "discord.Member"
    ):
        """
        Checks a single holder based on the wallet_address and updates the user’s role in Discord.
        """
        try:
            role_id = await self.holder_verification_usecase.execute(
                wallet_address, user
            )
            if role_id:
                logger.success(
                    f"Holder {user.id} verified and assigned to role {role_id}."
                )
                return role_id
            else:
                logger.warning(
                    f"User {user.id} with wallet {wallet_address} does not meet the NFT requirements for a role assignment."
                )
                return None
        except Exception as e:
            logger.error(
                f"Error verifying holder {user.id} with wallet {wallet_address}: {e}"
            )
            return None

    async def handle_periodic_verification(self, guild_id: int):
        """
        Periodically checks all holders and updates roles as needed.
        """
        try:
            updated_count = await self.holder_fetch_all_usecase.execute(guild_id)
            if updated_count == 0:
                logger.warning("No holders found for verification or no roles updated.")
            else:
                logger.success(
                    f"Successfully updated roles for {updated_count} holders."
                )
        except Exception as e:
            logger.error(f"Error in periodic holder verification: {e}")
