import discord
from loguru import logger


class DiscordService:
    def __init__(self, client: discord.Client):
        self.client = client

    async def send_message(self, channel_id: int, content=None, embed=None, view=None):
        """
        Sends a message to Discord. Can include a plain text message, an embed, or both, along with a view (e.g., buttons).
        """
        try:
            channel = self.client.get_channel(channel_id)
            if channel is None:
                logger.error(
                    "ERROR: Channel not found! Check that the CHANNEL_ID is correct."
                )
                return

            if content and embed and not view:
                await channel.send(content=content, embed=embed, view=view)
            elif embed and view:
                await channel.send(embed=embed, view=view)
            elif content:
                await channel.send(content=content, view=view)
            elif embed:
                await channel.send(embed=embed, view=view)
            elif view:
                await channel.send(view=view)

        except Exception as e:
            logger.error(f"Error sending message: {e}")

    @staticmethod
    async def add_role_to_user(user: discord.Member, role_id: int) -> bool:
        """
        Adds a role to the user if the role exists in the guild.
        """
        try:
            role = user.guild.get_role(role_id)
            if role:
                await user.add_roles(role)
                logger.success(
                    f"Role {role.name} (ID: {role_id}) added to user {user.id}"
                )
                return True
            logger.warning(f"Role with ID {role_id} not found in guild {user.guild.id}")
            return False
        except Exception as e:
            logger.error(f"Error adding role to user {user.id}: {e}")
            return False

    @staticmethod
    async def remove_role_from_user(user: discord.Member, role_id: int) -> bool:
        """
        Removes a role from the user if the role exists in the guild.
        """
        try:
            role = user.guild.get_role(role_id)
            if role:
                await user.remove_roles(role)
                logger.success(
                    f"Role {role.name} (ID: {role_id}) removed from user {user.id}"
                )
                return True
            logger.warning(f"Role with ID {role_id} not found in guild {user.guild.id}")
            return False
        except Exception as e:
            logger.error(f"Error removing role from user {user.id}: {e}")
            return False
