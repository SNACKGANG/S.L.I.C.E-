from discord import TextChannel
from discord.app_commands import Choice


class CoinShopController:
    def __init__(self, shop_usecase: "CoinShopUseCase"):
        self.shop_usecase = shop_usecase

    async def create_shop(self, shop_name: str, shop_description: str, channel: TextChannel) -> str:
        try:
            response = await self.shop_usecase.create_shop(shop_name, shop_description, channel)
            return response
        except Exception as e:
            print(f"Error creating shop: {e}")
            return "Failed to create shop. Please try again."

    async def remove_shop(self, shop_id: int) -> str:
        try:
            response = await self.shop_usecase.remove_shop(shop_id)
            return response
        except Exception as e:
            print(f"Error removing shop: {e}")
            return "Failed to remove shop. Please try again."

    async def add_item_to_shop(self, shop_id: int, item_id: int, price: int, stock: int,
                               allowed_role_id: int = None, user_purchase_limit: int = None) -> str:
        try:
            response = await self.shop_usecase.add_item_to_shop(
                shop_id=shop_id,
                item_id=item_id,
                price=price,
                stock=stock,
                allowed_role_id=allowed_role_id,
                user_purchase_limit=user_purchase_limit
            )
            return response
        except Exception as e:
            print(f"Error adding item to shop: {e}")
            return "Failed to add item to shop. Please try again."

    async def remove_item_from_shop(self, shop_id: int, item_id: int) -> str:
        try:
            response = await self.shop_usecase.remove_item_from_shop(shop_id, item_id)
            return response
        except Exception as e:
            print(f"Error removing item from shop: {e}")
            return "Failed to remove item from shop. Please try again."

    async def edit_item_in_shop(self, shop_id: int, item_id: int, price: int = None, stock: int = None,
                                allowed_role_id: int = None, user_purchase_limit: int = None) -> str:

        try:
            response = await self.shop_usecase.edit_item_in_shop(
                shop_id=shop_id,
                item_id=item_id,
                price=price,
                stock=stock,
                allowed_role_id=allowed_role_id,
                user_purchase_limit=user_purchase_limit
            )
            return response
        except Exception as e:
            print(f"Error editing item in shop: {e}")
            return "Failed to edit item in shop. Please try again."

    async def create_item(self, item_name: str, description: str, category: str = None,
                          role_id: int = None) -> str:
        try:
            response = await self.shop_usecase.create_item(item_name, description, category, role_id)
            return response
        except Exception as e:
            print(f"Error creating item: {e}")
            return "Failed to create item. Please try again."

    async def remove_item(self, item_id: int) -> str:
        try:
            response = await self.shop_usecase.remove_item(item_id)
            return response
        except Exception as e:
            print(f"Error removing item: {e}")
            return "Failed to remove item. Please try again."

    async def get_all_shops_with_names(self) -> list[Choice]:
        try:
            shops = await self.shop_usecase.get_all_shops_with_names()
            return shops
        except Exception as e:
            print(f"Error fetching shops for autocomplete: {e}")
            return []

    async def get_all_items_with_names(self) -> list[Choice]:
        try:
            items = await self.shop_usecase.get_all_items_with_names()
            return items
        except Exception as e:
            print(f"Error fetching items for autocomplete: {e}")
            return []
