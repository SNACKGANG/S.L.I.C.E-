from discord.ui import Button, View
from discord import ButtonStyle, Interaction, SelectOption

from .coin_shop_select_view import ShopView
from ..repositories import ShopItemRepository, ItemRepository


class BuyItemButton(Button):
    def __init__(self, shop_id: int):
        super().__init__(style=ButtonStyle.grey, label="Buy Item", custom_id=str(shop_id))
        self.shop_id = shop_id

    async def callback(self, interaction: Interaction):
        view: ButtonView = self.view
        await view.handle_button_interaction(interaction, self.shop_id)


class ButtonView(View):
    def __init__(self, bot, usecase: "CoinShopUseCase"):
        super().__init__(timeout=None)
        self.bot = bot
        self.shop_item_options = {}
        self.usecase = usecase

    async def initialize_buttons(self, shop_ids: list[int]):
        for shop_id in shop_ids:
            await self.add_button_for_shop(shop_id)

    async def add_button_for_shop(self, shop_id: int):
        try:
            button = BuyItemButton(shop_id)
            self.shop_item_options[shop_id] = []
            self.add_item(button)
            await self.update_shop_item_options(shop_id)
        except Exception as e:
            print(f"Error adding button for shop ID {shop_id}: {e}")

    async def handle_button_interaction(self, interaction: Interaction, shop_id: int):
        items_available = await ShopItemRepository.get_available_items_by_shop_id(shop_id)

        try:
            if items_available:
                await self.update_shop_item_options(shop_id)
                view = ShopView(
                    bot=self.bot,
                    shop_id=shop_id,
                    items_data=self.shop_item_options,
                    shop_usecase=self.usecase,
                )
                await interaction.response.send_message(
                    "Please select an item from the menu below:",
                    view=view,
                    ephemeral=True
                )

                view.original_message = await interaction.original_response()
            else:
                await interaction.response.send_message(
                    "There are no items available at the moment. Please check back later!",
                    ephemeral=True,
                )
        except Exception as e:
            print(f"{e}")

    async def update_shop_item_options(self, shop_id: int):
        try:
            available_items = await ShopItemRepository.get_available_items_by_shop_id(shop_id)
            items_data = {}

            for shop_item in available_items:
                item = await ItemRepository.get_item_by_id(shop_item.item_id)
                items_data[shop_item.item_id] = {
                    'name': item.name,
                    'price': shop_item.price,
                    'role_id': shop_item.restricted_role_id,
                    'limit': shop_item.user_purchase_limit or 0
                }
                self.shop_item_options[shop_id] = items_data
        except Exception as e:
            print(f"Error updating options for shop ID {shop_id}: {e}")
