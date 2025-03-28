import discord

from discord import app_commands
from discord.ext import commands
from typing_extensions import List


class CoinShopCog(commands.Cog):
    def __init__(self, bot, controller: "CoinShopController"):
        self.bot = bot
        self.controller = controller

    @commands.Cog.listener()
    async def on_ready(self):
        print("Shop Commands Loaded")

    async def shop_autocomplete(self, interaction: discord.Interaction, current: str) -> List[discord.app_commands.Choice[str]]:
        try:
            shop_choices = await self.controller.get_all_shops_with_names()
            return shop_choices
        except Exception as e:
            print(f"Error fetching shop autocomplete options: {e}")
            return []

    async def item_autocomplete(self, interaction: discord.Interaction, current: str) -> List[discord.app_commands.Choice[str]]:
        try:
            item_choices = await self.controller.get_all_items_with_names()
            return item_choices
        except Exception as e:
            print(f"Error fetching item autocomplete options: {e}")
            return []

    @app_commands.command(name="marketplace_add", description="Create a new shop in the system")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def create_shop_command(self, interaction: discord.Interaction, shop_name: str, shop_description: str, channel: discord.TextChannel):
        """
        Adds a new shop to the system.
        """
        try:
            response = await self.controller.create_shop(shop_name, shop_description, channel)
            await interaction.response.send_message(response, ephemeral=True)
        except Exception as e:
            print(f"Error creating shop: {e}")
            await interaction.response.send_message("An error occurred while creating the shop.", ephemeral=True)

    @app_commands.command(name="marketplace_remove", description="Remove a shop from the system")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.autocomplete(shop_id=shop_autocomplete)
    async def remove_shop_command(self, interaction: discord.Interaction, shop_id: str):
        """
        Removes a shop from the system.
        """
        try:
            response = await self.controller.remove_shop(shop_id)
            await interaction.response.send_message(response, ephemeral=True)
        except Exception as e:
            print(f"Error removing shop: {e}")
            await interaction.response.send_message("An error occurred while removing the shop.", ephemeral=True)

    @app_commands.command(name="marketplace_add_item", description="Add an item to a shop")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.autocomplete(shop_id=shop_autocomplete)
    @app_commands.autocomplete(item_id=item_autocomplete)
    async def add_item_command(self, interaction: discord.Interaction, shop_id: str, item_id: str, price: int, stock: int, allowed_role: discord.Role = None, user_purchase_limit: int = None):
        """
        Adds an item to a shop.
        """
        try:
            allowed_role_id = allowed_role.id if allowed_role else None
            response = await self.controller.add_item_to_shop(shop_id, item_id, price, stock, allowed_role_id, user_purchase_limit)
            await interaction.response.send_message(response, ephemeral=True)
        except Exception as e:
            print(f"Error adding item: {e}")
            await interaction.response.send_message("An error occurred while adding the item.", ephemeral=True)

    @app_commands.command(name="marketplace_remove_item", description="Remove an item from a shop")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.autocomplete(shop_id=shop_autocomplete)
    @app_commands.autocomplete(item_id=item_autocomplete)
    async def remove_item_command(self, interaction: discord.Interaction, shop_id: str, item_id: str):
        """
        Removes an item from a shop.
        """
        try:
            response = await self.controller.remove_item_from_shop(shop_id, item_id)
            await interaction.response.send_message(response, ephemeral=True)
        except Exception as e:
            print(f"Error removing item: {e}")
            await interaction.response.send_message("An error occurred while removing the item.", ephemeral=True)

    @app_commands.command(name="marketplace_edit_item", description="Edit an item in a shop")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.autocomplete(shop_id=shop_autocomplete)
    @app_commands.autocomplete(item_id=item_autocomplete)
    async def edit_item_command(self, interaction: discord.Interaction, shop_id: str, item_id: str, price: int = None, stock: int = None, allowed_role: discord.Role = None, user_purchase_limit: int = None):
        """
        Edits an item in a shop.
        """
        try:
            allowed_role_id = allowed_role.id if allowed_role else None
            response = await self.controller.edit_item_in_shop(shop_id, item_id, price, stock, allowed_role_id, user_purchase_limit)
            await interaction.response.send_message(response, ephemeral=True)
        except Exception as e:
            print(f"Error editing item: {e}")
            await interaction.response.send_message("An error occurred while editing the item.", ephemeral=True)

    @app_commands.command(name="add_item", description="Create a new item in the system")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def create_item_command(self, interaction: discord.Interaction, item_name: str, description: str, category: str = None, role: discord.Role = None):
        """
        Creates a new item in the system.
        """
        try:
            role_id = role.id if role else None
            response = await self.controller.create_item(item_name, description, category, role_id)
            await interaction.response.send_message(response, ephemeral=True)
        except Exception as e:
            print(f"Error creating item: {e}")
            await interaction.response.send_message("An error occurred while creating the item.", ephemeral=True)

    @app_commands.command(name="remove_item", description="Remove an item from the system")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.autocomplete(item_id=item_autocomplete)
    async def remove_item_command(self, interaction: discord.Interaction, item_id: str):
        """
        Removes an item from the system.
        """
        try:
            response = await self.controller.remove_item(item_id)
            await interaction.response.send_message(response, ephemeral=True)
        except Exception as e:
            print(f"Error removing item: {e}")
            await interaction.response.send_message("An error occurred while removing the item.", ephemeral=True)