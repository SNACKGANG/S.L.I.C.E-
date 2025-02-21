from loguru import logger

from ..models.holder_user_role_model import HolderUserRoleModel


class HolderUserRoleRepository:
    @staticmethod
    async def update_user_role(discord_user_id: int, guild_id: int, role_id: int):
        """
        Updates or inserts the user's role in the HolderRoleUserModel.
        """
        try:
            role_entry, created = await HolderUserRoleModel.get_or_create(
                discord_user_id=discord_user_id,
                guild_id=guild_id,
                defaults={"role_id": role_id},
            )

            if not created:
                role_entry.role_id = role_id
                await role_entry.save()

            logger.info(
                f"User {discord_user_id} role updated to {role_id} in guild {guild_id}"
            )

        except Exception as e:
            logger.error(
                f"Error updating role for {discord_user_id} in guild {guild_id}: {e}"
            )

    @staticmethod
    async def get_current_user_role(discord_user_id: int, guild_id: int):
        """
        Retrieves the current role ID assigned to the user.
        """
        try:
            user_role = await HolderUserRoleModel.filter(
                discord_user_id=discord_user_id, guild_id=guild_id
            ).first()
            return user_role.role_id if user_role else None
        except Exception as e:
            logger.error(
                f"Error retrieving current role for user {discord_user_id} in guild {guild_id}: {e}"
            )
            return None
