import discord
from black import List
from discord.ui import Select, View
from discord import Interaction, SelectOption
from ..repositories.coin_shop_item_repository import ItemRepository
from src.shared.services.discord_service import DiscordService
from typing import Optional, Dict


class BaseSelect(Select):
    def __init__(self, placeholder: str, custom_id: str, options: List[SelectOption]):
        super().__init__(placeholder=placeholder, custom_id=custom_id, options=options)


class ItemSelect(BaseSelect):
    def __init__(self, shop_id: int, options: List[SelectOption]):
        super().__init__(
            placeholder="Choose an item",
            custom_id=f"item_select_{shop_id}",
            options=options
        )

    async def callback(self, interaction: Interaction):
        await self.view.handle_item_selection(interaction, self.values[0])


class QuantitySelect(BaseSelect):
    def __init__(self, max_quantity: int):
        options = [SelectOption(label=str(i), value=str(i)) for i in range(1, max_quantity+1)]
        super().__init__(
            placeholder="Choose item_quantity",
            custom_id="quantity_select",
            options=options
        )

    async def callback(self, interaction: Interaction):
        try:
            await self.view.handle_quantity_selection(interaction, int(self.values[0]))
        except Exception as e:
            print(e)


class ShopView(View):
    def __init__(self, bot, shop_id: int, shop_usecase: "CoinShopUsecase", items_data: Dict):
        super().__init__(timeout=180)
        self.bot = bot
        self.shop_usecase = shop_usecase
        self.shop_id = shop_id
        self.items_data = items_data
        self.selected_item: Optional[dict] = None
        self.original_message: Optional[discord.Message] = None

        self.add_item(self.create_item_select())

    def create_item_select(self) -> ItemSelect:
        """Creates the item selection menu"""
        try:
            shop_items = self.items_data.get(self.shop_id, {})
            options = [
                SelectOption(
                    label=item['name'],
                    value=str(item_id),
                    description=f"Price: {item['price']} coins"
                ) for item_id, item in shop_items.items()
            ]
            return ItemSelect(self.shop_id, options)
        except Exception as e:
            print(e)

    @staticmethod
    def create_quantity_select(max_quantity: int) -> QuantitySelect:
        """Creates the item_quantity selection menu"""
        return QuantitySelect(max_quantity)

    async def handle_item_selection(self, interaction: Interaction, selected_value: str):
        """Processes the selection of an item"""
        try:
            item_id = int(selected_value)
            shop_items = self.items_data.get(self.shop_id, {})
            item_data = shop_items.get(item_id, {}).copy()

            if item_data:
                item_data["id"] = item_id

            self.selected_item = item_data

            if not await self.check_permissions(interaction):
                await interaction.response.send_message(
                    "You do not have permission to purchase this item!",
                    ephemeral=True
                )
                return
            # Check if the role and user already have it
            if await self.check_existing_role(interaction):
                return

            # Show item_quantity selector if needed
            if self.selected_item['limit'] > 1:
                await self.show_quantity_selector(interaction)
            else:
                await self.process_purchase(interaction, 1)
        except Exception as e:
            print(e)

    async def handle_quantity_selection(self, interaction: Interaction, quantity: int):
        """Handle the quantity selection and process the purchase"""
        await self.process_purchase(interaction, quantity)

    async def check_permissions(self, interaction: Interaction) -> bool:
        """Checks if the user has permission to purchase the item"""
        required_role = self.selected_item['role_id']
        if not required_role:
            return True

        return await DiscordService.check_permission_user(
            interaction.user,
            required_role
        )

    async def check_existing_role(self, interaction: Interaction) -> bool:
        """Checks if the user already has the role (if applicable)"""
        role_id = await ItemRepository.get_item_role_id(self.selected_item['role_id'])
        if not role_id:
            return False

        has_role = await DiscordService.member_has_role(
            member_id=interaction.user.id,
            role_id=role_id,
            guild_id=interaction.guild_id
        )

        if has_role:
            await interaction.response.send_message(
                f"You already have this role:<@&{role_id}>",
                ephemeral=True
            )
            return True
        return False

    async def show_quantity_selector(self, interaction: Interaction):
        """Show item_quantity selector"""
        try:
            self.clear_items()
            quantity_select = self.create_quantity_select(self.selected_item['limit'])
            self.add_item(quantity_select)

            await self.original_message.edit(
                content="Select the desired item_quantity:",
                view=self
            )
            await interaction.response.defer()
        except Exception as e:
            print(e)

    async def process_purchase(self, interaction: Interaction, quantity: int):
        """Execute the purchase process"""
        success, message = await self.shop_usecase.process_quantity_request(
            user=interaction.user,
            shop_id=self.shop_id,
            item_id=self.selected_item['id'],
            item_name=self.selected_item['name'],
            item_price=self.selected_item['price'],
            item_user_purchase_limit=self.selected_item['limit'],
            item_allowed_role_id=self.selected_item['role_id'],
            item_quantity=quantity,
        )
        if success:
            self.stop()
            await self.original_message.edit(content=message, view=None)
        else:
            await self.original_message.edit(content=message, view=None)
