from typing import List

import discord
from discord import app_commands
from discord.ext import commands, tasks
from loguru import logger

from src.modules.automation.models.sales_nft_config_model import SalesNftConfig
from src.modules.automation.repositories.sales_config_repository import \
    SalesConfigRepository


class SalesConfigCog(commands.Cog):
    def __init__(self, bot: "commands.Bot", sales_controller: "SalesController"):
        self.bot = bot
        self.sales_controller = sales_controller

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.check_sales.start()
        logger.info("SalesConfigCog is ready and the sales check task has started.")

    @tasks.loop(minutes=2)
    async def check_sales(self):
        """
        Task that checks sales periodically and sends them to Discord.
        """
        logger.info("Checking for new sales...")

        active_sales = await SalesConfigRepository.get_active_configs()

        if not active_sales:
            logger.info("No active sales found.")
            return

        await self.sales_controller.handle_sale(active_sales)
        logger.success("Sales check completed.")

    @app_commands.command(
        name="sales_config",
        description="Configure a channel to receive NFT sales notifications.",
    )
    @app_commands.default_permissions(administrator=True)
    async def configure_sales(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        contract: str,
    ):
        """
        Configures a channel to receive NFT sales and activates the system.
        """
        guild_id = interaction.guild_id
        await SalesConfigRepository.add_config(guild_id, channel.id, contract)
        logger.success(
            f"Sales activated in {channel.mention} for contract `{contract}`."
        )
        await interaction.response.send_message(
            f"Sales activated in {channel.mention} for contract `{contract}`.",
            ephemeral=True,
        )

    async def sales_toggle_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> List[discord.app_commands.Choice[int]]:
        """
        Provides autocomplete options for sales configurations in the guild.
        """
        try:
            configs = await SalesConfigRepository.get_configs_by_guild(
                interaction.guild_id
            )

            choices = [
                app_commands.Choice(
                    name=f"Channel: {config.channel_id} | Contract: {config.contract_address}",
                    value=config.id,
                )
                for config in configs
            ][:25]

            return choices
        except Exception as e:
            logger.error(f"Error in sales_toggle_autocomplete: {e}")
            return []

    @app_commands.command(
        name="sales_toggle", description="Toggle a specific sales configuration."
    )
    @app_commands.autocomplete(config_id=sales_toggle_autocomplete)
    @app_commands.default_permissions(administrator=True)
    async def toggle_sales(self, interaction: discord.Interaction, config_id: int):
        """
        Toggles a specific sales configuration on or off.
        """
        config = await SalesNftConfig.get_or_none(id=config_id)

        if not config:
            logger.warning(f"Configuration not found for ID: {config_id}")
            await interaction.response.send_message(
                "Configuration not found.", ephemeral=True
            )
            return

        config.is_active = not config.is_active
        await config.save()

        status = "enabled" if config.is_active else "disabled"
        logger.success(
            f"Sales configuration `{config.contract_address}` has been {status}."
        )
        await interaction.response.send_message(
            f"Sales configuration `{config.contract_address}` has been {status}.",
            ephemeral=True,
        )

    @app_commands.command(
        name="sales_remove",
        description="Disable NFT sales notifications for a specific configuration.",
    )
    @app_commands.autocomplete(config_id=sales_toggle_autocomplete)
    @app_commands.default_permissions(administrator=True)
    async def remove_sales(self, interaction: discord.Interaction, config_id: int):
        """
        Disables sales for a specific configuration.
        """
        try:
            control = await SalesConfigRepository.delete_by_id(config_id)
            if control:
                logger.success(f"Sales configuration {config_id} deleted successfully.")
                await interaction.response.send_message(
                    f"Sales for {config_id} deleted", ephemeral=True
                )
            else:
                logger.warning(f"Failed to delete sales configuration {config_id}.")
                await interaction.response.send_message(
                    f"Configuration for sales {config_id} has not been deleted. Try again.",
                    ephemeral=True,
                )
        except Exception as e:
            logger.error(f"Error removing sales configuration: {e}")
            await interaction.response.send_message(
                f"Error removing sales configuration: {e}"
            )
