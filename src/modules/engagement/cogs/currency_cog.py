from typing import List

import discord

from discord.ext import commands
from discord import app_commands
from loguru import logger


class CurrencyCog(commands.Cog):
    def __init__(self, bot: commands.Bot, controller: "CurrencyController"):
        self.bot = bot
        self.controller = controller

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Currency Cog Loaded")

    async def coin_autocomplete(self, interaction: discord.Interaction, current: str
                                ) -> List[discord.app_commands.Choice[str]]:

        currencies = await self.controller.get_available_currencies()
        return [
            app_commands.Choice(name=currency["name"], value=str(currency["id"]))
            for currency in currencies]

    @app_commands.command(name="coins_add_user", description="Add currency to a user")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.autocomplete(coin=coin_autocomplete)
    async def add_coins(self, interaction: discord.Interaction, user: discord.User, coin: str, quantity: int):
        try:
            await self.controller.add_coins(interaction.user.id, user.id, int(coin), quantity)
            await interaction.response.send_message(f"{quantity} {coin} added to <@{user.id}>.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error adding coins: {e}")
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="coins_remove_user", description="Remove currency from a user")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.autocomplete(coin=coin_autocomplete)
    async def remove_coins(self, interaction: discord.Interaction, user: discord.User, coin: str,
                           quantity: int):
        try:
            await self.controller.remove_coins(interaction.user.id, user.id, int(coin), quantity)
            await interaction.response.send_message(f"{quantity} removed from <@{user.id}>.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error removing coins: {e}")
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="coins_check_balance", description="Check your balance for a coin")
    @app_commands.autocomplete(coin=coin_autocomplete)
    async def show_currencies(self, interaction: discord.Interaction, coin: str):
        try:
            balance = await self.controller.get_balance(interaction.user.id, int(coin))
            await interaction.response.send_message(f"<@{interaction.user.id}> has {balance}.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error retrieving balance: {e}")
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="add_coin", description="Create a new currency type")
    @commands.has_permissions(administrator=True)
    async def add_currency_type(self, interaction: discord.Interaction, name: str, description: str = None):
        try:
            await self.controller.create_currency_type(name, description)
            await interaction.response.send_message(f"Currency {name} created successfully!", ephemeral=True)
        except Exception as e:
            logger.error(f"Error creating currency type: {e}")
