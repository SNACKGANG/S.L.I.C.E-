from typing import List

import discord

from discord.ext import commands
from discord import app_commands
from loguru import logger


class MysteryBoxCog(commands.Cog):
    def __init__(self, bot: commands.Bot, controller: "MysteryBoxController", reward_controller: "RewardController"):
        self.bot = bot
        self.controller = controller
        self.reward_controller = reward_controller

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Mystery Box Cog Loaded")

    async def reward_autocomplete(
            self, interaction: discord.Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        rewards = await self.reward_controller.get_available_rewards()
        return [
            app_commands.Choice(name=reward["name"], value=str(reward["id"]))
            for reward in rewards if current.lower() in reward["name"].lower()
        ]

    @app_commands.command(
        name="mystery_box_create",
        description="Create a Mystery Box and optionally assign up to three rewards."
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.autocomplete(reward_1=reward_autocomplete, reward_2=reward_autocomplete, reward_3=reward_autocomplete)
    async def create_mystery_box(
            self,
            interaction: discord.Interaction,
            name: str,
            channel: discord.TextChannel,
            reward_1: str,
            reward_2: str,
            reward_3: str = None,
            reward_4: str = None,
            reward_5: str = None,
    ):
        try:
            box = await self.controller.create_mystery_box(name, channel.id)
            box_id = box.id

            if reward_1:
                await self.controller.assign_reward_to_box(box_id, int(reward_1))
            if reward_2:
                await self.controller.assign_reward_to_box(box_id, int(reward_2))
            if reward_3:
                await self.controller.assign_reward_to_box(box_id, int(reward_3))
            if reward_4:
                await self.controller.assign_reward_to_box(box_id, int(reward_4))
            if reward_5:
                await self.controller.assign_reward_to_box(box_id, int(reward_5))

            await interaction.response.send_message(
                f"Mystery Box '{name}' created successfully in channel '{channel.name}' "
                f"with assigned rewards.", ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error creating Mystery Box: {e}")
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="mystery_box_update", description="Update an existing Mystery Box.")
    @app_commands.checks.has_permissions(administrator=True)
    async def update_mystery_box(
        self,
        interaction: discord.Interaction,
        box_id: int,
        name: str = None,
        channel_id: int = None,
    ):
        try:
            await self.controller.update_mystery_box(box_id, name=name, channel_id=channel_id)
            await interaction.response.send_message(f"Mystery Box '{box_id}' updated successfully!", ephemeral=True)
        except Exception as e:
            logger.error(f"Error updating Mystery Box: {e}")
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="mystery_box_delete", description="Delete a Mystery Box by its ID.")
    @app_commands.checks.has_permissions(administrator=True)
    async def delete_mystery_box(self, interaction: discord.Interaction, box_id: int):
        try:
            await self.controller.delete_mystery_box(box_id)
            await interaction.response.send_message(f"Mystery Box '{box_id}' deleted successfully!", ephemeral=True)
        except Exception as e:
            logger.error(f"Error deleting Mystery Box: {e}")
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="mystery_box_list_rewards", description="List all rewards in a Mystery Box.")
    @app_commands.checks.has_permissions(administrator=True)
    async def list_rewards_for_box(self, interaction: discord.Interaction, box_id: int):
        try:
            rewards = await self.controller.list_rewards_for_box(box_id)
            rewards_list = "\n".join([f"- {reward['name']}: {reward['value']} - chance: {reward['chance']}" for reward in rewards])
            await interaction.response.send_message(
                f"Rewards for Mystery Box '{box_id}':\n{rewards_list}", ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error listing rewards for Mystery Box: {e}")
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="mystery_box_by_channel", description="Get the Mystery Box configured for the current channel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def config_box_by_channel(self, interaction: discord.Interaction):
        try:
            box = await self.controller.get_mystery_box_by_channel(interaction.channel_id)
            if not box:
                await interaction.response.send_message("No Mystery Box configured for this channel.", ephemeral=True)
            else:
                await interaction.response.send_message(
                    f"Mystery Box '{box['name']}' is configured for this channel!", ephemeral=True
                )
        except Exception as e:
            logger.error(f"Error retrieving Mystery Box by channel: {e}")
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @commands.command(name="open_box", help="Open a Mystery Box in the current channel.")
    async def open_box(self, ctx):
        try:
            reward_data = await self.controller.open_lootbox(ctx.author.id, ctx.channel.id, ctx.author)

            if reward_data:
                embed = reward_data["embed"]
                await ctx.send(embed=embed)
                logger.info(
                    f"User {ctx.author.id} opened box '{reward_data['box_name']}' "
                    f"and received reward '{reward_data['reward']}'."
                )
            else:
                await ctx.send(f"No Mystery Box configured for this channel <#{ctx.channel.id}>.")

        except Exception as e:
            logger.error(f"Error processing open_box command: {e}")
            await ctx.send(f"An error occurred: {e}")
