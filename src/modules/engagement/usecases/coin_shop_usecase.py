from discord import TextChannel
from discord.app_commands import Choice

from src.modules.engagement.services.coin_shop_service import CoinShopService
from src.modules.engagement.views.coin_shop_buyitem_view import ButtonView


class CoinShopUseCase:
    def __init__(self, shop_repository: "ShopRepository", discord_service: "DiscordService", purchase_history_repository: "PurchaseHistoryRepository",
                 shop_item_repository: "ShopItemRepository", currency_repository: "CurrencyRepository", item_repository: "ItemRepository", bot):
        self.shop_repository = shop_repository
        self.shop_item_repository = shop_item_repository
        self.purchase_history_repository = purchase_history_repository
        self.currencies_repository = currency_repository
        self.discord_service = discord_service
        self.item_repository = item_repository
        self.bot = bot

    async def create_shop(self, shop_name: str, shop_description: str, channel: TextChannel) -> str:
        try:
            shop = await self.shop_repository.create_shop(shop_name, shop_description)
            shop_id = shop.id

            embed = await CoinShopService.create_shop_embed(shop, None, None)
            button_view = ButtonView(self.bot, self)
            await button_view.add_button_for_shop(shop_id)
            message = await channel.send(embed=embed, view=button_view)

            await self.shop_repository.update_shop_message_id(shop_id, message.id, channel.id)
            return f"Shop '{shop_name}' successfully created!"
        except Exception as e:
            print(f"Error creating shop: {e}")
            return "Failed to create shop. Please try again."

    async def remove_shop(self, shop_id: int) -> str:
        try:
            message_id, channel_id = await self.shop_repository.get_shop_message_id(shop_id)
            await self.shop_repository.remove_shop(shop_id)

            if message_id and channel_id:
                await self.discord_service.delete_message(channel_id, message_id)
            return f"Shop with ID {shop_id} successfully removed!"
        except Exception as e:
            print(f"Error removing shop: {e}")
            return "Failed to remove shop. Please try again."

    async def add_item_to_shop(self, shop_id: int, item_id: int, price: int, stock: int, allowed_role_id: int = None,
                               user_purchase_limit: int = None) -> str:
        try:
            item_added = await self.shop_item_repository.add_item_to_shop(
                shop_id=shop_id,
                item_id=item_id,
                item_price=price,
                item_stock=stock,
                restricted_role_id=allowed_role_id,
                user_purchase_limit=user_purchase_limit
            )
            if item_added:
                await CoinShopService.update_shop_message(shop_id, self.bot)
                return f"Item successfully added to shop ID {shop_id}!"
            return "Item already exists in this shop."
        except Exception as e:
            print(f"Error adding item to shop: {e}")
            return "Failed to add item to shop. Please try again."

    async def remove_item_from_shop(self, shop_id: int, item_id: int) -> str:
        try:
            await self.shop_item_repository.remove_item_from_shop(shop_id, item_id)
            await CoinShopService.update_shop_message(shop_id, self.bot)
            return f"Item successfully removed from shop ID {shop_id}."
        except Exception as e:
            print(f"Error removing item from shop: {e}")
            return "Failed to remove item from shop. Please try again."

    async def edit_item_in_shop(self, shop_id: int, item_id: int, price: int = None, stock: int = None,
                                allowed_role_id: int = None, user_purchase_limit: int = None) -> str:
        try:
            updated = await self.shop_item_repository.edit_item_in_shop(
                shop_id=shop_id,
                item_id=item_id,
                price=price,
                stock=stock,
                allowed_role=allowed_role_id,
                user_purchase_limit=user_purchase_limit
            )
            if updated:
                await CoinShopService.update_shop_message(shop_id, self.bot)
                return f"Item in shop ID {shop_id} successfully updated!"
            return "Error updating item. Please verify the input."
        except Exception as e:
            print(f"Error editing item in shop: {e}")
            return "Failed to edit item in shop. Please try again."

    async def create_item(self, item_name: str, description: str, category: str = None, role_id: int = None) -> str:
        try:
            await self.item_repository.create_item(item_name, description, category, role_id)
            return f"Item '{item_name}' successfully created in the system!"
        except Exception as e:
            print(f"Error creating item: {e}")
            return "Failed to create item. Please try again."

    async def remove_item(self, item_id: int) -> str:
        try:
            shop_ids = await self.item_repository.remove_item(item_id)
            for shop_id in shop_ids:
                await CoinShopService.update_shop_message(shop_id, self.bot)
            return f"Item with ID {item_id} successfully removed!"
        except Exception as e:
            print(f"Error removing item: {e}")
            return "Failed to remove item. Please try again."

    async def get_all_shops_with_names(self) -> list[Choice]:
        try:
            shops = await self.shop_repository.get_all_shop_names_with_ids()
            return [Choice(name=shop_name, value=str(shop_id)) for shop_name, shop_id in shops.items()]
        except Exception as e:
            print(f"Error fetching shops for autocomplete: {e}")
            return []

    async def get_all_items_with_names(self) -> list[Choice]:
        try:
            items = await self.item_repository.get_all_items_with_names()
            return [Choice(name=item_name, value=str(item_id)) for item_name, item_id in items.items()]
        except Exception as e:
            print(f"Error fetching items for autocomplete: {e}")
            return []

    @staticmethod
    async def _check_purchase_limit_with_data(purchased_quantity: int,
                                              requested_quantity: int,
                                              limit: int) -> bool:
        if limit == 0:
            return True
        return (purchased_quantity + requested_quantity) <= limit

    async def process_quantity_request(self, user, shop_id, item_id, item_name, item_price, item_allowed_role_id, item_user_purchase_limit, item_quantity):
        try:
            purchased_quantity = await self.purchase_history_repository.get_user_purchased_quantity(
                user.id, shop_id, item_id
            )
            if not await self._check_purchase_limit_with_data(
                    purchased_quantity, item_quantity, item_user_purchase_limit
            ):
                remaining = item_user_purchase_limit - purchased_quantity
                return False, f"Limit: {item_user_purchase_limit}. You can still purchase {remaining}"
            result = await self._buy_item(user.id, shop_id, item_id, item_price, item_quantity, item_allowed_role_id)

            if result == "no_stock":
                return False, "There is not enough stock for this item_quantity"
            elif result == "no_money":
                return False, "You don't have enough SNACKS"
            else:
                return True, f"You purchased {item_quantity} units of '{item_name}'! {item_quantity * item_price} SNACKS were debited from your wallet."
        except Exception as e:
            print(f"An error occurred in process_quantity_request: {e}")
            return False, "An error occurred while processing your request"

    async def _buy_item(self, user_id, shop_id, item_id, item_price, quantity, item_allowed_role_id):
        try:
            item_stock = await self.shop_item_repository.get_item_stock_in_shop(shop_id, item_id)
            if item_stock >= quantity:
                if await self.currencies_repository.remove_currencies_user(user_id=user_id, amount=item_price * quantity, currency_type=1):
                    # Update logs, stock, purchase record, and roles
                    await self.shop_item_repository.update_stock_in_shop(shop_id, item_id, -quantity)
                    await CoinShopService.update_shop_message(shop_id, self.bot)
                    await self.purchase_history_repository.record_purchase(user_id, item_id, shop_id, quantity, item_price * quantity)

                    if item_allowed_role_id:
                        await self.discord_service.add_role_to_user(user_id, item_allowed_role_id)
                    return True
                return "no_money"
            return "no_stock"
        except Exception as e:
            print(f"An error occurred in _buy_item: {e}")
            return False
