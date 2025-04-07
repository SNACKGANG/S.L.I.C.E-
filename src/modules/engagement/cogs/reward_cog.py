from typing import List

import discord

from discord.ext import commands
from discord import app_commands
from loguru import logger


class RewardCog(commands.Cog):
    def __init__(self, bot: commands.Bot, controller: "RewardController"):
        self.bot = bot
        self.controller = controller

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Reward Cog Loaded")

    async def coin_autocomplete(self, interaction: discord.Interaction, current: str) -> List[
                                discord.app_commands.Choice[str]]:
        currencies = await self.controller.get_available_currencies()
        return [
            app_commands.Choice(name=currency["name"], value=str(currency["id"]))
            for currency in currencies
        ]

    @app_commands.command(name="reward_create", description="Create a new reward.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.autocomplete(currency=coin_autocomplete)
    async def create_reward(
            self,
            interaction: discord.Interaction,
            name: str,
            value: str,
            chance: int,
            limit: int,
            color: str,
            image_url: str,
            currency: str = None
    ):
        try:
            currency_id = int(currency) if currency else None
            await self.controller.create_reward(name, value, chance, limit, color, image_url, currency_id)
            await interaction.response.send_message(f"Reward '{name}' created successfully!", ephemeral=True)
        except Exception as e:
            logger.error(f"Error creating reward: {e}")
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="reward_update", description="Update an existing reward.")
    @app_commands.checks.has_permissions(administrator=True)
    async def update_reward(
            self,
            interaction: discord.Interaction,
            name: str,
            value: str = None,
            chance: int = None,
            limit: int = None,
            color: str = None,
            image_url: str = None
    ):
        try:
            await self.controller.update_reward(name, value, chance, limit, color, image_url)
            await interaction.response.send_message(f"Reward '{name}' updated successfully!", ephemeral=True)
        except Exception as e:
            logger.error(f"Error updating reward: {e}")
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="reward_delete", description="Delete a reward.")
    @app_commands.checks.has_permissions(administrator=True)
    async def delete_reward(self, interaction: discord.Interaction, name: str):
        try:
            await self.controller.delete_reward(name)
            await interaction.response.send_message(f"Reward '{name}' deleted successfully!", ephemeral=True)
        except Exception as e:
            logger.error(f"Error deleting reward: {e}")
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="reward_list", description="List all rewards.")
    @app_commands.checks.has_permissions(administrator=True)
    async def list_rewards(self, interaction: discord.Interaction):
        try:
            rewards = await self.controller.list_rewards()
            rewards_list = "\n".join(
                [f"- {reward['name']}: {reward['value']} (Chance: {reward['chance']}%)" for reward in rewards]
            )
            await interaction.response.send_message(f"Rewards:\n{rewards_list}", ephemeral=True)
        except Exception as e:
            logger.error(f"Error listing rewards: {e}")
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
