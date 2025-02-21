import discord
from discord import app_commands
from discord.ext import commands, tasks
from loguru import logger

from src.modules.automation.services.holder_verification_service import \
    HolderVerificationService
from src.modules.automation.views.holder_verification_view import \
    HolderVerificationButtonView


class HolderVerificationCog(commands.Cog):
    """
    Cog responsible for handling holder verification commands and configurations.
    """

    def __init__(
        self,
        bot,
        holder_verification_controller: "HolderVerificationController",
        holder_verification_config_repository: "HolderConfigRepository",
    ):
        self.bot = bot
        self.holder_config_repository = holder_verification_config_repository
        self.holder_verification_controller = holder_verification_controller

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.all_holders_periodic_verification.start()

    @tasks.loop(minutes=10)
    async def all_holders_periodic_verification(self):
        guild_ids = [guild.id for guild in self.bot.guilds]

        for guild_id in guild_ids:
            await self.holder_verification_controller.handle_periodic_verification(
                guild_id
            )

    @app_commands.command(
        name="holder_verification_config",
        description="Configure NFT-based role assignment.",
    )
    @app_commands.default_permissions(administrator=True)
    async def holder_verification_config(
        self,
        interaction: discord.Interaction,
        collection_address: str,
        min1: int,
        max1: int | None,
        role1: discord.Role,
        min2: int = None,
        max2: int | None = None,
        role2: discord.Role = None,
        min3: int = None,
        max3: int | None = None,
        role3: discord.Role = None,
        min4: int = None,
        max4: int | None = None,
        role4: discord.Role = None,
    ):
        """
        Configura a verificação de holders com intervalos personalizados.
        """
        try:
            roles_data = [(min1, max1, role1.id)]

            if min2 and role2:
                roles_data.append((min2, max2, role2.id))
            if min3 and role3:
                roles_data.append((min3, max3, role3.id))
            if min4 and role4:
                roles_data.append((min4, max4, role4.id))

            # Save configuration in database
            save_control = await self.holder_config_repository.save_config(
                interaction.guild_id, collection_address, roles_data
            )
            if not save_control:
                return

            embed = await HolderVerificationService.create_configuration_embed(
                collection_address, roles_data
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

            embed_verification = (
                await HolderVerificationService.create_verification_embed(interaction)
            )
            view = HolderVerificationButtonView(self.holder_verification_controller)
            channel = self.bot.get_channel(interaction.channel_id)

            await channel.send(embed=embed_verification, view=view)

        except Exception as e:
            logger.error(f"Error saving holder verification config: {e}")
            await interaction.response.send_message(
                "**Failed to save the configuration.**", ephemeral=True
            )
