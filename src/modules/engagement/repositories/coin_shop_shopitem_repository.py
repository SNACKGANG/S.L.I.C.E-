from ..models import ShopItem, Shop, Item


class ShopItemRepository:
    @staticmethod
    async def add_item_to_shop(shop_id, item_id, item_price, item_stock, restricted_role_id=None,
                               user_purchase_limit=None):
        try:
            return await ShopItem.create(
                shop_id=shop_id,
                item_id=item_id,
                price=item_price,
                stock=item_stock,
                restricted_role_id=restricted_role_id,
                user_purchase_limit=user_purchase_limit
            )
        except Exception as e:
            print(f"Error while adding the item to the shop in the database: {e}")
            return False

    @staticmethod
    async def remove_item_from_shop(shop_id, item_id):
        try:
            await ShopItem.filter(shop_id=shop_id, item_id=item_id).delete()
        except Exception as e:
            print(f"Error while removing the item from the shop in the database: {e}")

    @staticmethod
    async def edit_item_in_shop(shop_id, item_id, price=None, stock=None, allowed_role=None, user_purchase_limit=None):
        try:
            item_in_shop = await ShopItem.filter(shop_id=shop_id, item_id=item_id).first()
            if not item_in_shop:
                raise ValueError("Item not found in the shop")
            item_in_shop.price = price if price is not None else item_in_shop.price
            item_in_shop.stock = stock if stock is not None else item_in_shop.stock
            item_in_shop.restricted_role_id = allowed_role if allowed_role is not None else item_in_shop.restricted_role_id
            item_in_shop.user_purchase_limit = user_purchase_limit if user_purchase_limit is not None else item_in_shop.user_purchase_limit
            await item_in_shop.save()
            return True
        except Exception as e:
            print(f"Error while editing the item in the shop in the database: {e}")
            return False

    @staticmethod
    async def get_item_stock_in_shop(shop_id, item_id):
        try:
            shop_item = await ShopItem.filter(shop_id=shop_id, item_id=item_id).first()
            return shop_item.stock if shop_item else 0
        except Exception as e:
            print(f"Error while fetching the stock of the item in the shop: {e}")
            return None

    @staticmethod
    async def update_stock_in_shop(shop_id, item_id, quantity):
        try:
            shop_item = await ShopItem.filter(shop_id=shop_id, item_id=item_id).first()
            if not shop_item:
                return False
            shop_item.stock = max(shop_item.stock + quantity, 0)
            await shop_item.save()
            return True
        except Exception as e:
            print(f"Error while updating the item stock in the shop: {e}")
            return False

    @staticmethod
    async def get_available_items_by_shop_id(shop_id):
        try:
            return await ShopItem.filter(shop_id=shop_id, stock__gt=0).all()
        except Exception as e:
            print(f"Error while fetching available items from the database: {e}")
            return []

    @staticmethod
    async def get_items_by_shop_id(shop_id):
        try:
            return await ShopItem.filter(shop_id=shop_id).all()
        except Exception as e:
            print(f"Error while fetching items from the shop: {e}")
            return []

    @staticmethod
    async def associate_item_with_shop(shop_id, item_id):
        shop = await Shop.filter(id=shop_id).first()
        item = await Item.filter(id=item_id).first()
        if not shop or not item:
            raise ValueError("Store or Item not found")
        return await ShopItem.create(shop=shop, item=item)

    @staticmethod
    async def remove_item_from_shop(shop_id, item_id):
        await ShopItem.filter(shop_id=shop_id, item_id=item_id).delete()

    @staticmethod
    async def get_items_by_shop(shop_id):
        return await ShopItem.filter(shop_id=shop_id).prefetch_related("item")

    @staticmethod
    async def get_shops_by_item(item_id):
        return await ShopItem.filter(item_id=item_id).prefetch_related("shop")
