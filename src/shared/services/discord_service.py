import discord
from loguru import logger


class DiscordService:
    def __init__(self, client: discord.Client):
        """
        DiscordService provides utility methods for interacting with Discord members, roles, and channels.
        """
        self.client = client

    async def send_message(self, channel_id: int, content=None, embed=None, view=None):
        """
        Sends a message to Discord. Can include a plain text message, an embed, or both, along with a view (e.g., buttons).
        """
        try:
            channel = self.client.get_channel(channel_id)
            if channel is None:
                logger.error("ERROR: Channel not found! Check that the CHANNEL_ID is correct.")
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

    async def get_discord_member(self, member_id: int, guild_id: int):
        """
        Fetches a Discord member by their ID. If the member is not cached, attempts to fetch them from the guild.
        """
        guild = self.client.get_guild(guild_id)
        if guild is None:
            logger.warning(f"Guild with ID {guild_id} not found.")
            return None

        member = guild.get_member(member_id)
        if member is None:
            # If the member is not cached, attempt to fetch them from Discord
            try:
                member = await guild.fetch_member(member_id)
            except discord.NotFound:
                logger.warning(f"Member with ID {member_id} not found in guild {guild_id}.")
                return None

        return member

    async def member_has_role(self, member_id: int, role_id: int, guild_id: int) -> bool:
        """
        Checks if a member has a specific role by ID.
        """
        member = await self.get_discord_member(member_id, guild_id)
        if member is None:
            logger.warning(f"Unable to fetch member with ID {member_id}.")
            return False

        # Verify if the member has the specified role
        return role_id in [role.id for role in member.roles]

    @staticmethod
    async def add_role_to_user(user: discord.Member, role_id: int) -> bool:
        """
        Adds a role to the user if the role exists in the guild.
        """
        try:
            role = user.guild.get_role(role_id)
            if role:
                await user.add_roles(role)
                logger.success(f"Role {role.name} (ID: {role_id}) added to user {user.id}")
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
                logger.success(f"Role {role.name} (ID: {role_id}) removed from user {user.id}")
                return True
            logger.warning(f"Role with ID {role_id} not found in guild {user.guild.id}")
            return False
        except Exception as e:
            logger.error(f"Error removing role from user {user.id}: {e}")
            return False

    @staticmethod
    async def has_required_role(user: discord.Member, role_id: int) -> bool:
        """
        Checks whether a user has the required role by ID.
        """
        allowed_role = discord.utils.get(user.roles, id=role_id)
        return allowed_role is not None

    @staticmethod
    async def check_permission_user(user: discord.Member, allowed_role_id: int) -> bool:
        """
        Checks if a user has permission to interact based on a required role.
        """
        if allowed_role_id:
            return await DiscordService.has_required_role(user, allowed_role_id)
        return True
